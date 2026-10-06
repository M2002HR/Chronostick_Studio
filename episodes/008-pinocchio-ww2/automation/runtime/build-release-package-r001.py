from pathlib import Path
import json,hashlib,zipfile,datetime
EP=Path('/home/mhr/Code/chronostick-studio/episodes/008-pinocchio-ww2');QC=json.loads((EP/'delivery/final-qc-r001.json').read_text());assert QC['status']=='approved_for_local_delivery'
episode=json.loads((EP/'episode.json').read_text());video=EP/episode['distribution_master'];picture=EP/episode['picture_master'];manifest=json.loads(video.with_suffix('.postproduction.json').read_text());assert manifest['full_decode']=='passed';assert manifest['frame_count']==773
package=Path(manifest['package']);metadata=json.loads((EP/'delivery/youtube/metadata.json').read_text());assert metadata['status']=='delivery_ready'
files=[(video,video.name),(picture,'editable/'+picture.name),(EP/'audio/narration-es-r001.wav','editable/narration-es-r001.wav'),(EP/'delivery/youtube/thumbnail-episode-008-r004.png','thumbnail-episode-008-r004.png'),(EP/'delivery/release/pinocchio-stick-r005.png','pinocchio-stick-r005.png'),(package/'captions.srt','captions-es.srt'),(package/'captions.vtt','captions-es.vtt'),(package/'captions.ass','editable/active-word-captions.ass'),(package/'fonts/caption.ttf','editable/Montserrat-Bold.ttf'),(package/'edit-snapshot.json','editable/edit-snapshot.json'),(EP/'timestamps/word-timestamps-source.csv','editable/word-timestamps-es.csv'),(EP/'audio/sfx/selected-full-stem-r001.wav','editable/selected-sfx-stem-r001.wav'),(EP/'delivery/youtube/metadata.json','youtube/metadata.json'),(EP/'delivery/youtube/metadata.md','youtube/metadata.md'),(EP/'delivery/youtube/description.txt','youtube/description.txt'),(EP/'script/narration-es.md','script/narration-es.md'),(EP/'script/voiceover-google-vids-es.md','script/voiceover-google-vids-es.md'),(EP/'delivery/release/README.md','README.md'),(EP/'delivery/release/CREDITS.md','CREDITS.md'),(EP/'delivery/release/Montserrat-OFL.txt','Montserrat-OFL.txt'),(EP/'delivery/source-fidelity-final-r001.json','provenance/source-fidelity-final-r001.json'),(EP/'delivery/final-qc-r001.json','provenance/final-qc-r001.json'),(video.with_suffix('.postproduction.json'),'provenance/distribution-postproduction.json'),(picture.with_suffix('.framewise-upscale.json'),'provenance/picture-framewise-upscale.json'),(EP/'renders/selection-manifest.json','provenance/selection-manifest.json'),(EP/'audio/sfx/selected-full-stem-r001.json','provenance/selected-sfx-stem.json'),(EP/'audio/sfx/reusable-recordings-r001/manifest.json','provenance/recorded-sfx-sources.json')]
rows=[]
for src,name in files:
 assert src.is_file() and src.stat().st_size>0,(src,name)
 rows.append(dict(archive_path=name,source=str(src.relative_to(EP)),bytes=src.stat().st_size,sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
release=dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),episode_id=EP.name,language='es',status='complete_local_delivery',video=video.name,frame_count=773,fps=24,duration_seconds=773/24,dimensions=[1080,1920],files=rows,published=False,new_human_release_approval=False)
m=EP/'delivery/release/release-manifest-r001.json';assert not m.exists();m.write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n')
out=EP/'delivery/release/episode-008-es-release-r001.zip';assert not out.exists()
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for src,name in files:z.write(src,name)
 z.write(m,'release-manifest-r001.json')
with zipfile.ZipFile(out) as z:assert z.testzip() is None
(EP/'delivery/release/zip-qc-r001.json').write_text(json.dumps(dict(path=str(out.relative_to(EP)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size,entries=len(files)+1,archive_crc_check='passed'),indent=2)+'\n')
print(out)
