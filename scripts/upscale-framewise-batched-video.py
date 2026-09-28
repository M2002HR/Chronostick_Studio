#!/usr/bin/env python3
"""Frame-preserving Spandrel video upscale with adaptive GPU tile batching.

The standard framewise wrapper sends one tile to the model at a time.  This
runner preserves its output contract, but can send same-shaped tiles from a
frame as a tensor batch.  Batching is opt-in: its throughput is hardware- and
model-dependent, so the stable default remains one tile per inference.
``--batch-size`` is an upper bound: CUDA OOM reduces the batch size by half and
retries the same tiles, so a run can use spare VRAM without failing merely
because its requested batch is too large.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path

import cv2
import numpy as np
import torch
from spandrel import ModelLoader


def probe(path: Path, *, count_frames: bool = False) -> dict:
    command = ["ffprobe", "-v", "error"]
    if count_frames:
        command.append("-count_frames")
    command += ["-show_streams", "-show_format", "-of", "json", str(path)]
    data = json.loads(subprocess.run(command, capture_output=True, text=True, check=True).stdout)
    video = next(item for item in data["streams"] if item["codec_type"] == "video")
    audio = next((item for item in data["streams"] if item["codec_type"] == "audio"), None)
    fps = float(Fraction(video.get("avg_frame_rate") or video["r_frame_rate"]))
    frames = video.get("nb_read_frames") or video.get("nb_frames")
    duration = float(data["format"].get("duration") or video.get("duration") or 0)
    return {
        "width": int(video["width"]),
        "height": int(video["height"]),
        "fps": fps,
        "frames": int(frames) if frames not in (None, "N/A") else round(duration * fps),
        "duration": duration,
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name") if audio else None,
        "has_audio": audio is not None,
        "size": int(data["format"].get("size") or path.stat().st_size),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def fit_frame(image: np.ndarray, width: int, height: int, mode: str) -> np.ndarray:
    source_h, source_w = image.shape[:2]
    if mode == "stretch":
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    scale = max(width / source_w, height / source_h) if mode == "cover" else min(width / source_w, height / source_h)
    resized_w, resized_h = round(source_w * scale), round(source_h * scale)
    resized = cv2.resize(image, (resized_w, resized_h), interpolation=cv2.INTER_AREA)
    if mode == "cover":
        x = max(0, (resized_w - width) // 2)
        y = max(0, (resized_h - height) // 2)
        return resized[y:y + height, x:x + width]
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    x, y = (width - resized_w) // 2, (height - resized_h) // 2
    canvas[y:y + resized_h, x:x + resized_w] = resized
    return canvas


def gpu_sample() -> dict | None:
    try:
        values = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu,memory.used,power.draw,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            text=True,
        ).splitlines()[0]
        utilization, memory, power, temperature = (float(item.strip()) for item in values.split(","))
        return {
            "utilization_percent": utilization,
            "memory_used_mib": memory,
            "power_w": power,
            "temperature_c": temperature,
        }
    except Exception:
        return None


def load_model(path: Path, device: torch.device, precision: str):
    state = torch.load(path, map_location="cpu", weights_only=True)
    state = state.get("params_ema", state.get("params", state))
    descriptor = ModelLoader().load_from_state_dict(state).eval()
    dtype = torch.float16 if precision == "fp16" else torch.float32
    descriptor.model.to(device=device, dtype=dtype).eval()
    return descriptor, dtype


def is_cuda_oom(error: RuntimeError) -> bool:
    return "out of memory" in str(error).lower()


def tile_positions(height: int, width: int, tile: int, overlap: int) -> list[tuple[int, int]]:
    stride = tile - overlap
    ys = list(range(0, max(1, height - overlap), stride))
    xs = list(range(0, max(1, width - overlap), stride))
    positions: list[tuple[int, int]] = []
    for y in ys:
        for x in xs:
            position = (min(y, max(0, height - tile)), min(x, max(0, width - tile)))
            if position not in positions:
                positions.append(position)
    return positions


def blend_tile(
    output: torch.Tensor,
    weights: torch.Tensor,
    result: torch.Tensor,
    *,
    y0: int,
    x0: int,
    tile: int,
    overlap: int,
    height: int,
    width: int,
    scale: int,
) -> None:
    mask = torch.ones((1, result.shape[1], result.shape[2]), dtype=torch.float32)
    feather = min(overlap * scale, result.shape[1] // 4, result.shape[2] // 4)
    if feather:
        ramp = torch.linspace(0, 1, feather)
        if y0 > 0:
            mask[:, :feather, :] *= ramp.view(1, -1, 1)
        if y0 + tile < height:
            mask[:, -feather:, :] *= ramp.flip(0).view(1, -1, 1)
        if x0 > 0:
            mask[:, :, :feather] *= ramp.view(1, 1, -1)
        if x0 + tile < width:
            mask[:, :, -feather:] *= ramp.flip(0).view(1, 1, -1)
    oy, ox = y0 * scale, x0 * scale
    output[:, oy:oy + result.shape[1], ox:ox + result.shape[2]] += result * mask
    weights[:, oy:oy + result.shape[1], ox:ox + result.shape[2]] += mask


def upscale_tiled_batched(
    frame: np.ndarray,
    descriptor,
    dtype: torch.dtype,
    device: torch.device,
    *,
    tile: int,
    overlap: int,
    requested_batch_size: int,
    batch_state: dict,
) -> tuple[np.ndarray, int]:
    height, width = frame.shape[:2]
    scale = int(descriptor.scale)
    source = torch.from_numpy(frame.copy()).permute(2, 0, 1).float().div_(255)
    output = torch.zeros((3, height * scale, width * scale), dtype=torch.float32)
    weights = torch.zeros((1, height * scale, width * scale), dtype=torch.float32)
    records = [
        (y0, x0, source[:, y0:min(y0 + tile, height), x0:min(x0 + tile, width)])
        for y0, x0 in tile_positions(height, width, tile, overlap)
    ]
    active_batch_size = min(requested_batch_size, batch_state["effective_batch_size"])
    offset = 0
    while offset < len(records):
        batch_records = records[offset:offset + active_batch_size]
        try:
            patches = torch.stack([record[2] for record in batch_records]).to(device=device, dtype=dtype)
            with torch.inference_mode(), torch.autocast(
                device_type=device.type,
                dtype=dtype,
                enabled=(device.type == "cuda" and dtype == torch.float16),
            ):
                results = descriptor(patches).float().cpu().clamp_(0, 1)
        except RuntimeError as error:
            if not is_cuda_oom(error) or active_batch_size == 1:
                raise
            torch.cuda.empty_cache()
            previous = active_batch_size
            active_batch_size = max(1, active_batch_size // 2)
            batch_state["effective_batch_size"] = active_batch_size
            batch_state["fallbacks"].append({"from": previous, "to": active_batch_size})
            print(f"CUDA OOM: reducing tile batch from {previous} to {active_batch_size}; retrying.", flush=True)
            continue
        batch_state["largest_successful_batch"] = max(batch_state["largest_successful_batch"], len(batch_records))
        for (y0, x0, _), result in zip(batch_records, results, strict=True):
            blend_tile(
                output,
                weights,
                result,
                y0=y0,
                x0=x0,
                tile=tile,
                overlap=overlap,
                height=height,
                width=width,
                scale=scale,
            )
        offset += len(batch_records)
    output.div_(weights.clamp_min_(1e-6))
    return output.permute(1, 2, 0).mul_(255).round_().byte().numpy(), active_batch_size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", type=Path, default=Path("/home/mhr/AI/ComfyUI/models/upscale_models/RealESRGAN_x4plus_anime_6B.pth"))
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fit", choices=("cover", "contain", "stretch"), default="cover")
    parser.add_argument("--tile", type=int, default=256)
    parser.add_argument("--overlap", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=1, help="maximum same-shaped tiles per GPU inference")
    parser.add_argument("--precision", choices=("fp16", "fp32"), default="fp16")
    parser.add_argument("--blend", type=float, default=1.0)
    parser.add_argument("--crf", type=int, default=16)
    parser.add_argument("--preset", default="medium")
    parser.add_argument("--progress-every", type=int, default=12)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source, output, model_path = args.input.expanduser().resolve(), args.output.expanduser().resolve(), args.model.expanduser().resolve()
    if not source.is_file() or not model_path.is_file():
        raise SystemExit("input or model does not exist")
    if output.exists() and not args.overwrite:
        raise SystemExit(f"output exists; pass --overwrite to replace it: {output}")
    if args.tile <= args.overlap or args.batch_size <= 0:
        raise SystemExit("tile must exceed overlap and batch-size must be positive")
    if not 0 <= args.blend <= 1:
        raise SystemExit("blend must be between 0 and 1")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.stem}.partial{output.suffix}")
    temporary.unlink(missing_ok=True)
    source_info = probe(source, count_frames=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    descriptor, dtype = load_model(model_path, device, args.precision)
    fps_text = f"{source_info['fps']:.12g}"
    decode = subprocess.Popen(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(source), "-map", "0:v:0", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    encode = subprocess.Popen(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-video_size", f"{args.width}x{args.height}", "-framerate", fps_text, "-i", "pipe:0", "-i", str(source), "-map", "0:v:0", "-map", "1:a:0?", "-map", "1:s?", "-map_metadata", "1", "-c:v", "libx264", "-preset", args.preset, "-crf", str(args.crf), "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-c:s", "copy", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(temporary)],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    frame_bytes = source_info["width"] * source_info["height"] * 3
    batch_state = {"effective_batch_size": args.batch_size, "largest_successful_batch": 0, "fallbacks": []}
    started, started_at, samples, processed = time.monotonic(), datetime.now(UTC), [], 0
    try:
        while True:
            raw = decode.stdout.read(frame_bytes)
            if not raw:
                break
            if len(raw) != frame_bytes:
                raise RuntimeError(f"short decoded frame: {len(raw)} of {frame_bytes} bytes")
            frame = np.frombuffer(raw, np.uint8).reshape(source_info["height"], source_info["width"], 3)
            enlarged, effective_batch = upscale_tiled_batched(
                frame,
                descriptor,
                dtype,
                device,
                tile=args.tile,
                overlap=args.overlap,
                requested_batch_size=args.batch_size,
                batch_state=batch_state,
            )
            fitted = fit_frame(enlarged, args.width, args.height, args.fit)
            if args.blend < 1:
                source_fitted = fit_frame(frame, args.width, args.height, args.fit)
                fitted = cv2.addWeighted(fitted, args.blend, source_fitted, 1 - args.blend, 0)
            encode.stdin.write(fitted.tobytes())
            processed += 1
            if processed == 1 or processed % args.progress_every == 0 or processed == source_info["frames"]:
                elapsed = time.monotonic() - started
                rate = processed / elapsed
                eta = (source_info["frames"] - processed) / rate if rate else 0
                sample = gpu_sample()
                if sample:
                    samples.append(sample)
                resource = f" vram={sample['memory_used_mib']:.0f}MiB gpu={sample['utilization_percent']:.0f}%" if sample else ""
                print(
                    f"FRAME {processed}/{source_info['frames']} overall={processed/source_info['frames']*100:.1f}% fps={rate:.2f} "
                    f"eta={eta:.1f}s batch={effective_batch}{resource}",
                    flush=True,
                )
        encode.stdin.close()
        decode_error = decode.stderr.read().decode(errors="replace")
        encode_error = encode.stderr.read().decode(errors="replace")
        decode_code, encode_code = decode.wait(), encode.wait()
        if decode_code or encode_code:
            raise RuntimeError(f"ffmpeg failed: decode={decode_code} {decode_error[-2000:]} encode={encode_code} {encode_error[-2000:]}")
    except Exception:
        for process in (decode, encode):
            if process.poll() is None:
                process.kill()
        temporary.unlink(missing_ok=True)
        raise

    temporary.replace(output)
    final_info = probe(output, count_frames=True)
    if final_info["frames"] != source_info["frames"] or final_info["fps"] != source_info["fps"]:
        raise RuntimeError(f"timing validation failed: source={source_info} output={final_info}")
    if (final_info["width"], final_info["height"]) != (args.width, args.height):
        raise RuntimeError(f"dimension validation failed: {final_info['width']}x{final_info['height']}")
    completed_at, elapsed = datetime.now(UTC), time.monotonic() - started
    report = {
        "schema_version": "1.0",
        "engine": "framewise-spandrel-batched",
        "model": {"path": str(model_path), "sha256": sha256(model_path), "scale": descriptor.scale},
        "input": str(source),
        "output": str(output),
        "source": source_info,
        "final": final_info,
        "settings": vars(args) | {"input": str(source), "output": str(output), "model": str(model_path)},
        "batching": batch_state,
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "elapsed_seconds": round(elapsed, 3),
        "processing_fps": round(processed / elapsed, 3),
        "resources": {
            "sample_count": len(samples),
            "gpu_memory_used_mib_peak": max((sample["memory_used_mib"] for sample in samples), default=None),
            "gpu_utilization_percent_average": round(sum(sample["utilization_percent"] for sample in samples) / len(samples), 3) if samples else None,
            "gpu_power_w_peak": max((sample["power_w"] for sample in samples), default=None),
            "gpu_temperature_c_peak": max((sample["temperature_c"] for sample in samples), default=None),
        },
    }
    report_path = output.with_suffix(".framewise-upscale.json")
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"SUCCESS output={output} report={report_path} elapsed={elapsed:.1f}s frames={processed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
