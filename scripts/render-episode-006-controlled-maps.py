#!/usr/bin/env python3
"""Render only the two authorized zero-person geographic inserts, never H3 maps."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
IMAGE = ROOT / 'assets/episodes/006-shortest-war-ever/references/map-world-blank-r001.png'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    records = []
    for number in (14, 118):
        output = EP / f'renders/controlled-maps/clip-{number:03d}-map-r005.mp4'
        if output.exists():
            raise FileExistsError('Immutable output already exists: ' + str(output))
        output.parent.mkdir(parents=True, exist_ok=True)
        zoom = '2.3' if number == 118 else '1+1.3*pow(min(on/84,1),2)*(3-2*min(on/84,1))'
        vf = (f"zoompan=z='{zoom}':x='max(0,min(iw-iw/zoom,iw*.59-iw/zoom/2))':"
              "y='max(0,min(ih-ih/zoom,ih*.55-ih/zoom/2))':d=120:s=1024x576:fps=24,setsar=1")
        route = None
        if number == 118:
            # Geography is broad explanatory direction, not a surveyed itinerary.
            # Coordinates are normalized to the directly inspected zero-person anchor.
            start, end = (.5957, .5844), (.567, .55)
            def position(point):
                return ((point[0] - .59 + .5 / 2.3) * 2.3 * 1024,
                        (point[1] - .55 + .5 / 2.3) * 2.3 * 576)
            a, b = position(start), position(end)
            for step in range(20):
                t = step / 19
                x, y = round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t)
                onset = round(50 + 54 * t)
                vf += f",drawbox=x={x-2}:y={y-2}:w=5:h=5:color=0x6f4e26@0.85:t=fill:enable='gte(n,{onset})'"
                vf += f",drawbox=x={x-1}:y={y-1}:w=3:h=3:color=0xe1b866:t=fill:enable='gte(n,{onset})'"
            route = {'start': start, 'end': end, 'first_frame': 50, 'last_reveal_frame': 104,
                     'meaning': 'broad Zanzibar-to-adjacent-East-African-mainland direction; no exact route, port or political border'}
        command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-loop', '1', '-i', str(IMAGE),
                   '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-map', '0:v:0', '-map', '1:a:0',
                   '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-threads', '4', '-crf', '18',
                   '-pix_fmt', 'yuv420p', '-r', '24', '-frames:v', '120', '-t', '5', '-c:a', 'aac',
                   '-b:a', '96k', '-movflags', '+faststart', str(output)]
        subprocess.run(command, check=True)
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                      'format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames', '-of', 'json', str(output)], text=True))
        assert float(probe['format']['duration']) == 5
        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        assert (video['width'], video['height'], video['r_frame_rate'], video['nb_frames']) == (1024, 576, '24/1', '120')
        assert any(s['codec_type'] == 'audio' for s in probe['streams'])
        records.append({'number': number, 'method': 'controlled_geography', 'revision': 5,
                        'path': str(output.relative_to(ROOT)), 'sha256': sha(output),
                        'source_reference': str(IMAGE.relative_to(ROOT)), 'source_sha256': sha(IMAGE),
                        'duration_seconds': 5, 'fps': 24, 'frames': 120, 'people': 0,
                        'audio': 'silent stereo; no voice or music', 'route': route,
                        'operations': 'crop/affine zoom of reviewed empty chart; only a native graphic dotted line in118',
                        'review_status': 'needs_actual_frame_review', 'command': command})
    (EP / 'renders/controlled-maps/manifest-r005.json').write_text(json.dumps({'schema_version': '1.0', 'clips': records}, indent=2) + '\n')
    print('Rendered two zero-person controlled geography inserts:014 and118.')


if __name__ == '__main__':
    main()
