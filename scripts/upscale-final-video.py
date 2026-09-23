#!/usr/bin/env python3
"""Enhance a 720x1280 or 1080x1920 final-video source to 1080x1920.

The script drives the locally installed FlashVSR 1.1 ComfyUI node in short
segments. FlashVSR only supports 2x or 4x factors, so each segment is enhanced
at 2x (1440x2560 from 720p, or 2160x3840 from 1080p) and then downscaled with
ffmpeg/Lanczos to 1080x1920.
Audio is copied from the original source only after the enhanced segments are
joined, which avoids duplicate audio at segment boundaries.

Examples:
  ./scripts/upscale-final-video.py /path/to/source-720x1280.mp4
  ./scripts/upscale-final-video.py /path/to/soft-1080x1920.mp4
  ./scripts/upscale-final-video.py source.mp4 --profile performance
  COMFYUI_DIR=/opt/ComfyUI ./scripts/upscale-final-video.py source.mp4
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from fractions import Fraction
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMFY_DIR = REPO_ROOT.parents[1] / "AI" / "ComfyUI"
FLASHVSR_MODEL_FILES = (
    "FlashVSR1_1.safetensors",
    "Wan2.1_VAE.safetensors",
    "LQ_proj_in.safetensors",
    "TCDecoder.safetensors",
    "Prompt.safetensors",
)
REQUIRED_NODES = {
    "VHS_LoadVideoFFmpegPath",
    "AILab_FlashVSR_Advanced",
    "VHS_VideoCombine",
}
MIN_FLASHVSR_FRAMES = 21
SUPPORTED_SOURCE_DIMENSIONS = {(720, 1280), (1080, 1920)}
DEFAULT_SEGMENT_SECONDS = {
    (720, 1280): 2.0,
    # A 1080p source produces 2160x3840 intermediate frames. One-second
    # segments keep the tiled result and blending buffers inside 32 GB RAM.
    (1080, 1920): 1.0,
}
FLASHVSR_PROFILES = {
    "safe": {
        "model_version": "Tiny Long (Low VRAM)",
        "tile_size": 384,
        "tile_overlap": 48,
        "unload_model": True,
        "vae_tiling": True,
        "description": "lowest VRAM demand; slowest and safest",
    },
    "performance": {
        "model_version": "Tiny (Fast)",
        "tile_size": 512,
        "tile_overlap": 48,
        "unload_model": False,
        "vae_tiling": True,
        "description": "uses more VRAM; use safe if CUDA runs out of memory",
    },
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        fail(f"Required command is not available: {command}")


def probe_video(video: Path) -> dict[str, Any]:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,width,height,r_frame_rate,nb_frames:format=duration",
            "-of",
            "json",
            str(video),
        ],
        capture=True,
    )
    data = json.loads(result.stdout)
    stream = next((item for item in data.get("streams", []) if item.get("codec_type") == "video"), None)
    if stream is None:
        fail(f"No video stream found: {video}")

    try:
        fps = float(Fraction(stream["r_frame_rate"]))
        duration = float(data["format"]["duration"])
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        fail(f"Could not read frame rate or duration from {video}: {error}")

    if fps <= 0 or duration <= 0:
        fail(f"Invalid frame rate or duration in {video}")

    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "fps": fps,
        "duration": duration,
    }


def revisioned_destination(source: Path, output: str | None) -> Path:
    if output:
        destination = Path(output).expanduser().resolve()
        if destination.exists():
            fail(f"Refusing to overwrite an existing export: {destination}")
        return destination

    destination_dir = source.parent
    for revision in range(1, 1000):
        destination = destination_dir / f"{source.stem}-flashvsr-r{revision:03d}.mp4"
        if not destination.exists():
            return destination
    fail(f"No free revision number available in {destination_dir}")


def segment_plan(duration: float, fps: float, segment_seconds: float) -> list[tuple[float, int]]:
    """Return start-time/frame-count pairs, with no final segment below 21 frames."""
    total_frames = round(duration * fps)
    requested_frames = max(1, round(segment_seconds * fps))
    segments: list[tuple[int, int]] = []
    start = 0
    while start < total_frames:
        count = min(requested_frames, total_frames - start)
        remaining = total_frames - (start + count)
        if 0 < remaining < MIN_FLASHVSR_FRAMES:
            count += remaining
        segments.append((start, count))
        start += count

    if segments and segments[-1][1] < MIN_FLASHVSR_FRAMES:
        if len(segments) == 1:
            fail(
                f"FlashVSR needs at least {MIN_FLASHVSR_FRAMES} frames; "
                f"this source has only {segments[-1][1]}."
            )
        previous_start, previous_count = segments[-2]
        segments[-2] = (previous_start, previous_count + segments[-1][1])
        segments.pop()

    return [(start / fps, count) for start, count in segments]


def http_json(url: str, *, payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json"})
    # The workstation has an HTTP proxy configured. ComfyUI is a loopback-only
    # service, so proxying its API produces a 502 instead of reaching it.
    with build_opener(ProxyHandler({})).open(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def server_available(base_url: str) -> bool:
    try:
        http_json(f"{base_url}/system_stats", timeout=3)
        return True
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return False


def start_comfy_if_needed(base_url: str, comfy_dir: Path) -> tuple[subprocess.Popen[str] | None, Path | None]:
    if server_available(base_url):
        print("Stage 2/5: ComfyUI is already running.", flush=True)
        return None, None

    parsed = urlparse(base_url)
    if parsed.hostname not in {"127.0.0.1", "localhost"} or parsed.port is None:
        fail(f"ComfyUI is not reachable at {base_url}; start that server before running this script.")

    python = comfy_dir / ".venv" / "bin" / "python"
    main = comfy_dir / "main.py"
    if not python.is_file() or not main.is_file():
        fail(f"ComfyUI runtime not found at {comfy_dir}; set COMFYUI_DIR or use --comfy-dir.")

    log_fd, log_name = tempfile.mkstemp(prefix="chronostick-comfy-", suffix=".log")
    os.close(log_fd)
    log = Path(log_name)
    log_handle = log.open("w", encoding="utf-8")
    process = subprocess.Popen(
        [str(python), str(main), "--listen", "127.0.0.1", "--port", str(parsed.port)],
        cwd=comfy_dir,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
    )
    log_handle.close()

    # This ComfyUI installation can take nearly three minutes to initialize on
    # a cold start, before any model is loaded.
    print("Stage 2/5: Starting ComfyUI (cold start can take up to 5 minutes)...", flush=True)
    for _ in range(150):
        if server_available(base_url):
            print("Stage 2/5: ComfyUI is ready.", flush=True)
            return process, log
        if process.poll() is not None:
            fail(f"ComfyUI stopped during startup. See {log}")
        if (_ + 1) % 15 == 0:
            print(f"Stage 2/5: still starting ({(_ + 1) * 2}/300 seconds)...", flush=True)
        time.sleep(2)
    process.terminate()
    fail(f"ComfyUI did not start within 300 seconds. See {log}")


def check_comfy_installation(base_url: str, comfy_dir: Path) -> None:
    missing_models = [name for name in FLASHVSR_MODEL_FILES if not (comfy_dir / "models" / "FlashVSR" / name).is_file()]
    if missing_models:
        fail("FlashVSR model files are missing: " + ", ".join(missing_models))

    info = http_json(f"{base_url}/object_info")
    missing_nodes = sorted(REQUIRED_NODES - set(info))
    if missing_nodes:
        fail("ComfyUI did not load required nodes: " + ", ".join(missing_nodes))


def workflow(
    source: Path,
    start_time: float,
    frame_count: int,
    fps: float,
    prefix: str,
    seed: int,
    profile: dict[str, Any],
) -> dict[str, Any]:
    return {
        "1": {
            "class_type": "VHS_LoadVideoFFmpegPath",
            "inputs": {
                "video": str(source),
                "force_rate": 0,
                "custom_width": 0,
                "custom_height": 0,
                "frame_load_cap": frame_count,
                "start_time": start_time,
            },
        },
        "2": {
            "class_type": "AILab_FlashVSR_Advanced",
            "inputs": {
                "frames": ["1", 0],
                "model_version": profile["model_version"],
                "scale": 2,
                "enable_tiling": True,
                "tile_size": profile["tile_size"],
                "tile_overlap": profile["tile_overlap"],
                "speed_optimization": 2.0,
                "quality_boost": 2.0,
                "stability_level": 11,
                "color_fix": True,
                "vae_tiling": profile["vae_tiling"],
                "unload_model": profile["unload_model"],
                "sageattention": "enable",
                "device": "auto",
                "precision": "fp16",
                "seed": seed,
            },
        },
        "3": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": ["2", 0],
                "frame_rate": fps,
                "loop_count": 0,
                "filename_prefix": prefix,
                "format": "video/h264-mp4",
                "pingpong": False,
                "save_output": True,
                "pix_fmt": "yuv420p",
                "crf": 18,
                "save_metadata": False,
                "trim_to_audio": False,
            },
        },
    }


def wait_for_completion(
    base_url: str,
    prompt_id: str,
    segment_index: int,
    segment_total: int,
    progress_start: float,
    progress_end: float,
) -> dict[str, Any]:
    started = time.monotonic()
    next_update = 15.0
    while True:
        history = http_json(f"{base_url}/history/{prompt_id}")
        record = history.get(prompt_id)
        if record:
            status = record.get("status", {})
            if status.get("status_str") == "error":
                fail("ComfyUI processing failed: " + json.dumps(status.get("messages", []), ensure_ascii=False))
            outputs = record.get("outputs", {})
            if "3" in outputs:
                print(
                    f"Stage 3/5: segment {segment_index}/{segment_total} complete "
                    f"({progress_end:.1f}% overall).",
                    flush=True,
                )
                return outputs["3"]
        elapsed = time.monotonic() - started
        if elapsed >= next_update:
            print(
                f"Stage 3/5: segment {segment_index}/{segment_total} is still running "
                f"({int(elapsed)}s elapsed; overall progress is {progress_start:.1f}%–{progress_end:.1f}%).",
                flush=True,
            )
            next_update += 15.0
        time.sleep(5)


def output_path(comfy_dir: Path, output: dict[str, Any]) -> Path:
    gifs = output.get("gifs", [])
    if not gifs:
        fail("ComfyUI completed but Video Combine returned no MP4 output.")
    item = gifs[0]
    if item.get("type", "output") != "output":
        fail("Unexpected ComfyUI output location: " + json.dumps(item))
    candidate = comfy_dir / "output" / item.get("subfolder", "") / item["filename"]
    if not candidate.is_file():
        fail(f"ComfyUI reported an output that does not exist: {candidate}")
    return candidate


def create_final_export(source: Path, enhanced_segments: list[Path], destination: Path) -> None:
    with tempfile.NamedTemporaryFile("w", prefix="chronostick-flashvsr-", suffix=".txt", delete=False) as handle:
        concat_list = Path(handle.name)
        for segment in enhanced_segments:
            escaped = str(segment).replace("'", r"'\\''")
            handle.write(f"file '{escaped}'\n")

    try:
        run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-i",
                str(source),
                "-map",
                "0:v:0",
                "-map",
                "1:a?",
                "-vf",
                "scale=1080:1920:flags=lanczos",
                "-c:v",
                "libx264",
                "-preset",
                "slow",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
                "-shortest",
                str(destination),
            ]
        )
    finally:
        concat_list.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="FlashVSR 720p/1080p final-video enhancer with 1080x1920 output")
    parser.add_argument("source", type=Path, help="720x1280 or 1080x1920 source video; it is never modified")
    parser.add_argument("--output", help="Destination MP4; must not already exist")
    parser.add_argument("--comfy-dir", default=os.environ.get("COMFYUI_DIR", str(DEFAULT_COMFY_DIR)))
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument(
        "--profile",
        choices=FLASHVSR_PROFILES,
        default="safe",
        help="safe is conservative; performance uses more VRAM and may OOM",
    )
    parser.add_argument(
        "--segment-seconds",
        type=float,
        help="FlashVSR segment length; default: 2 for 720p, 1 for 1080p",
    )
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print the planned work")
    arguments = parser.parse_args()

    try:
        if arguments.segment_seconds is not None and arguments.segment_seconds <= 0:
            fail("--segment-seconds must be greater than zero")
        require_command("ffmpeg")
        require_command("ffprobe")
        source = arguments.source.expanduser().resolve()
        if not source.is_file():
            fail(f"Source video does not exist: {source}")
        metadata = probe_video(source)
        source_dimensions = (metadata["width"], metadata["height"])
        if source_dimensions not in SUPPORTED_SOURCE_DIMENSIONS:
            fail(
                f"This script accepts only 720x1280 or 1080x1920 sources; {source.name} is "
                f"{metadata['width']}x{metadata['height']}. It was left untouched."
            )
        segment_seconds = arguments.segment_seconds or DEFAULT_SEGMENT_SECONDS[source_dimensions]
        segments = segment_plan(metadata["duration"], metadata["fps"], segment_seconds)
        profile = FLASHVSR_PROFILES[arguments.profile]
        destination = revisioned_destination(source, arguments.output)
        comfy_dir = Path(arguments.comfy_dir).expanduser().resolve()
        intermediate_width = metadata["width"] * 2
        intermediate_height = metadata["height"] * 2
        print(
            f"Source: {source}\n"
            f"Plan: {len(segments)} FlashVSR 2x segment(s) at {intermediate_width}x{intermediate_height} "
            f"({segment_seconds:g}s each), then Lanczos downscale to 1080x1920\n"
            f"Profile: {arguments.profile} — {profile['model_version']}, tile {profile['tile_size']}, "
            f"unload_model={profile['unload_model']}\n"
            f"Destination: {destination}",
            flush=True,
        )
        if arguments.dry_run:
            return 0

        print("Stage 1/5: input validated; checking ComfyUI and local model files.", flush=True)
        server, log = start_comfy_if_needed(arguments.comfy_url.rstrip("/"), comfy_dir)
        try:
            check_comfy_installation(arguments.comfy_url.rstrip("/"), comfy_dir)
            print("Stage 2/5: FlashVSR and video nodes are available.", flush=True)
            enhanced_segments: list[Path] = []
            total_frames = sum(frame_count for _, frame_count in segments)
            completed_frames = 0
            for index, (start_time, frame_count) in enumerate(segments, start=1):
                prefix = f"chronostick-flashvsr/{source.stem}-{uuid.uuid4().hex[:8]}-part{index:03d}"
                prompt = workflow(
                    source,
                    start_time,
                    frame_count,
                    metadata["fps"],
                    prefix,
                    arguments.seed + index - 1,
                    profile,
                )
                response = http_json(
                    f"{arguments.comfy_url.rstrip('/')}/prompt",
                    payload={"prompt": prompt, "client_id": str(uuid.uuid4())},
                )
                prompt_id = response.get("prompt_id")
                if not prompt_id:
                    fail("ComfyUI rejected the workflow: " + json.dumps(response, ensure_ascii=False))
                progress_start = completed_frames / total_frames * 100
                progress_end = (completed_frames + frame_count) / total_frames * 100
                print(
                    f"Stage 3/5: processing segment {index}/{len(segments)} "
                    f"({frame_count} frames, {progress_start:.1f}%–{progress_end:.1f}% overall)...",
                    flush=True,
                )
                enhanced_segments.append(
                    output_path(
                        comfy_dir,
                        wait_for_completion(
                            arguments.comfy_url.rstrip("/"),
                            prompt_id,
                            index,
                            len(segments),
                            progress_start,
                            progress_end,
                        ),
                    )
                )
                completed_frames += frame_count

            print("Stage 4/5: joining enhanced segments, restoring audio, and encoding the final MP4...", flush=True)
            create_final_export(source, enhanced_segments, destination)
            print("Stage 5/5: validating final dimensions and duration...", flush=True)
            result = probe_video(destination)
            if (result["width"], result["height"]) != (1080, 1920):
                fail(f"Output validation failed: expected 1080x1920, got {result['width']}x{result['height']}")
            print(f"Created: {destination} ({result['width']}x{result['height']}, {result['duration']:.3f}s)")
        finally:
            if server is not None:
                server.terminate()
                try:
                    server.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    server.kill()
                if log:
                    print(f"ComfyUI startup log: {log}")
        return 0
    except (RuntimeError, subprocess.CalledProcessError, OSError, HTTPError, URLError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
