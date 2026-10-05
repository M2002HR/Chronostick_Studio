#!/usr/bin/env python3
"""Render exact five-second 16:9 map/clock editorial clips from reviewed stills."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    parser.add_argument("--revision", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ep = args.episode.resolve()
    timing = json.loads((ep / "timestamps/timing-map.json").read_text())
    plan = json.loads((ep / "automation/job-plan.json").read_text())
    texts = {e["clip"]: e for e in json.loads((ep / "plan/text-events.json").read_text())["events"]}
    transitions = {93: 1.2, 99: 2.8, 105: 2.0}
    graphics = []
    for slot in plan["slots"]:
        n = slot["number"]
        final = Path(slot["references"][-1]).name
        if not final.startswith(("map-", "clock-")):
            continue
        refs = [(REPO / value).resolve() for value in slot["references"]]
        for ref in refs:
            if not ref.is_file(): raise FileNotFoundError(ref)
        onset = texts[n]["onset_seconds"] if n in texts and len(refs) == 2 else transitions.get(n)
        if len(refs) == 2 and onset is None: raise ValueError(f"clip {n}: missing transition time")
        if len(refs) == 1 and onset is not None: raise ValueError(f"clip {n}: transition without two references")
        dest = ep / f"renders/graphics/clip-{n:03d}-graphic-r{args.revision:03d}.mp4"
        if dest.exists(): raise FileExistsError(dest)
        graphics.append((n, refs, onset, dest))
    if args.dry_run:
        print(f"Validated {len(graphics)} map/clock graphics clips; no media written")
        return
    outputs=[]
    for i,(n,refs,onset,dest) in enumerate(graphics,1):
        dest.parent.mkdir(parents=True,exist_ok=True)
        cmd=["ffmpeg","-hide_banner","-loglevel","error","-n"]
        for ref in refs: cmd += ["-loop","1","-framerate","24","-i",str(ref)]
        cmd += ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo"]
        if len(refs)==1:
            vf="scale=1024:576:flags=lanczos,format=yuv420p"
            cmd += ["-map","0:v:0","-map","1:a:0","-vf",vf]
            cut_frame=None
        else:
            cut_frame=max(1,min(119,round(onset*24)))
            graph=(f"[0:v]scale=1024:576:flags=lanczos,format=yuv420p,trim=end_frame={cut_frame},setpts=PTS-STARTPTS[v0];"
                   f"[1:v]scale=1024:576:flags=lanczos,format=yuv420p,trim=end_frame={120-cut_frame},setpts=PTS-STARTPTS[v1];"
                   "[v0][v1]concat=n=2:v=1:a=0[v]")
            cmd += ["-filter_complex",graph,"-map","[v]","-map","2:a:0"]
        cmd += ["-c:v","libx264","-preset","veryfast","-crf","18","-r","24","-frames:v","120",
                "-c:a","aac","-b:a","96k","-t","5","-movflags","+faststart",str(dest)]
        subprocess.run(cmd,check=True)
        probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,width,height,nb_frames,r_frame_rate","-of","json",str(dest)],text=True))
        streams=probe["streams"]
        if round(float(probe["format"]["duration"]),3)!=5.0 or not any(s.get("codec_type")=="video" and s.get("width")==1024 and s.get("height")==576 and s.get("nb_frames")=="120" for s in streams) or not any(s.get("codec_type")=="audio" for s in streams):
            raise ValueError(f"invalid graphic output: {dest}")
        outputs.append({"clip":n,"path":str(dest.relative_to(REPO)),"sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
                        "source_references":[str(ref.relative_to(REPO)) for ref in refs],
                        "transition_frame":cut_frame,"duration_seconds":5,"fps":24,"method":"deterministic code-native map/clock picture with silent SFX-only audio"})
        print(f"{i:02d}/{len(graphics):02d} clip-{n:03d}",flush=True)
    out=ep/"renders/graphics/manifest-r001.json"
    out.write_text(json.dumps({"schema_version":"1.0","episode_id":ep.name,"clips":outputs},ensure_ascii=False,indent=2)+"\n")
    print(out)


if __name__=="__main__":main()
