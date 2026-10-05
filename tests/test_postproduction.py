import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest
from PIL import ImageFont

spec = importlib.util.spec_from_file_location('postproduction', Path(__file__).parents[1] / 'scripts/postproduce-episode.py')
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)
FONT = Path('/home/mhr/.local/share/fonts/chronostick-arial/Arialbd.TTF')


def word(n, text, start, end):
    return dict(index=n, word=text, start=start, end=end)


def test_highlight_replaces_previous_word_and_is_white_in_gaps():
    words = [word(1, 'one', 0, .7), word(2, 'two', .4, .5), word(3, 'three', .9, 1.1)]
    cue = dict(words=words, lines=[words], start=0, end=1.1)
    events = pp.caption_events([cue], '&H00D7FF&')
    at = lambda cs: next(e for e in events if e['start_cs'] <= cs < e['end_cs'])
    assert at(20)['active_word_index'] == 1
    assert at(45)['active_word_index'] == 2
    assert at(55)['active_word_index'] is None  # No reactivation of overlapped word 1.
    assert at(80)['active_word_index'] is None
    assert at(100)['active_word_index'] == 3
    assert all(e['text'].count('\\1c&H00D7FF&') <= 1 for e in events)
    assert all(a['end_cs'] <= b['start_cs'] for a, b in zip(events, events[1:]))


def test_short_spoken_word_is_visible_on_the_actual_24fps_grid():
    words = [word(1, 'en', 542.28, 542.46), word(2, 'la', 542.46, 542.50),
             word(3, 'misma', 542.50, 542.70)]
    cue = dict(words=words, lines=[words], start=542.28, end=542.70)
    events = pp.snap_events_to_frames(pp.caption_events([cue], '&H00D7FF&'), 24)
    visible = {e['active_word_index'] for e in events
               if ((e['start_cs'] * 24 + 99) // 100) * 100 < e['end_cs'] * 24}
    assert visible == {1, 2, 3}
    assert all(a['end_cs'] <= b['start_cs'] for a, b in zip(events, events[1:]))


def test_timestamp_source_is_preserved_and_export_adjustment_is_separate(tmp_path):
    path = tmp_path / 'words.csv'
    source = b'\xef\xbb\xbfword,start,end\r\nUno,0.12,0.48\r\nDos,0.40,0.70\r\n'
    path.write_bytes(source)
    words = pp.load_words(path, adjustments=[dict(first_word_index=2, offset_seconds=.03628)])
    assert path.read_bytes() == source
    assert words[1]['source_start'] == .4
    assert words[1]['start'] == pytest.approx(.43628)
    path.write_text('word,start,end\nUno,0.2,0.3\nDos,0.1,0.4\n')
    with pytest.raises(ValueError, match='strictly increasing'):
        pp.load_words(path)


def test_duplicate_provider_start_can_use_an_explicit_existing_end_boundary(tmp_path):
    path = tmp_path / 'words.csv'
    source = 'word,start,end\nKhalid,296.340,296.600\nrecibe,296.341,297.040\n'
    path.write_text(source)
    repairs = [dict(word_index=2, method='previous_source_word_end', reason='near-duplicate provider onset')]
    words = pp.load_words(path, boundary_repairs=repairs)
    assert words[1]['start'] == 296.6
    assert words[1]['source_start'] == 296.341
    assert path.read_text() == source
    cue = dict(words=words, lines=[words], start=words[0]['start'], end=words[-1]['end'])
    assert {e['active_word_index'] for e in pp.caption_events([cue], '&H00D7FF&')} == {1, 2}


@pytest.mark.skipif(not FONT.exists(), reason='Arial Bold not installed')
def test_long_caption_wraps_without_losing_any_word():
    font = ImageFont.truetype(str(FONT), 54)
    words = [word(i, 'extraordinariamente', i * .2, (i + 1) * .2) for i in range(1, 20)]
    style = dict(max_width_fraction=.8, max_words=12, max_cue_seconds=4, break_gap_seconds=.45)
    cues = pp.make_cues(words, style, font, 1920)
    assert [w['index'] for c in cues for w in c['words']] == list(range(1, 20))
    assert [w['index'] for c in cues for line in c['lines'] for w in line] == list(range(1, 20))
    assert all(len(c['lines']) <= 2 for c in cues)
    assert all(font.getlength(' '.join(w['word'] for w in line)) <= 1536
               for c in cues for line in c['lines'])


@pytest.mark.skipif(not FONT.exists(), reason='Arial Bold not installed')
def test_single_line_mode_shortens_phrases_without_widening_or_dropping_words():
    font = ImageFont.truetype(str(FONT), 60)
    words = [word(i, 'extraordinariamente', i * .2, (i + 1) * .2) for i in range(1, 30)]
    style = dict(max_width_fraction=.8, max_words=12, max_cue_seconds=4,
                 break_gap_seconds=.45, max_lines=1)
    cues = pp.make_cues(words, style, font, 1920)
    assert [w['index'] for c in cues for line in c['lines'] for w in line] == list(range(1, 30))
    assert all(len(c['lines']) == 1 for c in cues)
    assert all(font.getlength(' '.join(w['word'] for w in c['lines'][0])) <= 1536 for c in cues)
    assert all('\\N' not in e['text'] for e in pp.caption_events(cues, '&H00D7FF&'))


def test_scheduled_beds_duck_but_effects_keep_their_original_cue_time():
    graph = pp.mix_graph([
        dict(duration_seconds=10, start_seconds=2, gain_db=-24, duck_under_narration=True),
        dict(duration_seconds=.3, start_seconds=7.125, source_start_seconds=.5, gain_db=-6),
    ], 20)
    assert '[voice]asplit=2[main][sc0]' in graph
    assert '[t1][sc0]sidechaincompress' in graph
    assert 'adelay=342000S:all=1' in graph
    assert '[main][d1][t2]amix=inputs=3' in graph


@pytest.mark.skipif(not shutil.which('ffmpeg'), reason='FFmpeg required')
def test_real_mix_ducks_music_and_places_sfx_at_the_requested_time(tmp_path):
    voice, bed, sfx = [tmp_path / f'{name}.wav' for name in ('voice', 'bed', 'sfx')]
    for path, source in [
        (voice, "aevalsrc=0.15*sin(2*PI*440*t)*between(t\\,1\\,2):s=48000:d=4"),
        (bed, 'sine=frequency=880:sample_rate=48000:duration=4'),
        (sfx, 'sine=frequency=1300:sample_rate=48000:duration=0.2'),
    ]:
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', source, str(path)], check=True)
    tracks = [dict(duration_seconds=4, start_seconds=0, gain_db=-6, duck_under_narration=True),
              dict(duration_seconds=.2, start_seconds=3.1, gain_db=0)]
    cmd = ['ffmpeg', '-v', 'error', '-i', str(voice), '-i', str(bed), '-i', str(sfx),
           '-filter_complex', pp.mix_graph(tracks, 4), '-map', '[mix]', '-ac', '1', '-ar', '48000',
           '-f', 'f32le', '-']
    audio = np.frombuffer(subprocess.check_output(cmd), dtype=np.float32)

    def amplitude(hz, start, end):
        samples = audio[round(start * 48000):round(end * 48000)]
        time = np.arange(len(samples)) / 48000
        return abs(np.mean(samples * np.exp(-2j * np.pi * hz * time)))

    assert amplitude(880, 1.3, 1.8) < amplitude(880, .3, .8) * .5
    assert amplitude(1300, 3.12, 3.25) > amplitude(1300, .3, .8) * 100
    assert len(audio) == 4 * 48000


@pytest.mark.skipif(not FONT.exists() or not shutil.which('ffmpeg'), reason='FFmpeg and Arial required')
def test_real_render_mutes_native_tone_and_preserves_frames(tmp_path):
    root = tmp_path / "episode with spaces"
    root.mkdir()
    picture, voice, timing = root / 'picture.mp4', root / 'voice.wav', root / 'words.csv'
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=0x304050:s=640x360:r=24:d=2',
                    '-f', 'lavfi', '-i', 'sine=frequency=1100:duration=2:sample_rate=48000',
                    '-c:v', 'libx264', '-c:a', 'aac', '-shortest', str(picture)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1.5:sample_rate=48000',
                    str(voice)], check=True)
    timing.write_text('word,start,end\nUno,0.2,0.6\nDos.,0.6,1.2\n')
    config = dict(schema_version='1.0', picture=str(picture), picture_sha256=pp.digest(picture),
                  narration=dict(path=str(voice), sha256=pp.digest(voice), offset_seconds=0),
                  timing=dict(path=str(timing), sha256=pp.digest(timing), source_voice_sha256=pp.digest(voice)),
                  native_audio=dict(mode='mute'), tracks=[], external_music_allowed=False,
                  captions=dict(font_family='Arial', font_file=str(FONT), font_size=26, max_width_fraction=.8,
                                bottom_margin=24, outline=1.5, shadow=1, highlight_ass_color='&H00D7FF&',
                                max_words=12, max_cue_seconds=4, break_gap_seconds=.45),
                  loudness=dict(integrated_lufs=-16, true_peak_dbtp=-1.5, lra=11),
                  encoding=dict(crf=18, preset='fast', threads=2), audio_language_iso639_2='spa')
    output, package = root / 'master-r001.mp4', root / 'package-r001'
    result = pp.render(root, config, output, package)
    assert result['frame_count'] == 48
    assert result['duration_seconds'] == 2
    assert result['native_audio']['mode'] == 'mute'
    audio = np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(output),
                          '-map', '0:a:0', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-']), dtype=np.float32)
    samples = audio[4800:48000]
    spectrum = np.abs(np.fft.rfft(samples))
    frequencies = np.fft.rfftfreq(len(samples), 1 / 48000)
    band = lambda hz: spectrum[np.abs(frequencies - hz) < 5].max()
    assert band(1100) < band(440) / 1000  # Actual output contains no native 1100Hz tone.
    pixels = np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', '0.4', '-i', str(output),
                           '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']), dtype=np.uint8).reshape(-1, 3)
    assert ((pixels[:, 0] > 180) & (pixels[:, 1] > 130) & (pixels[:, 2] < 100)).sum() > 20
    assert ((pixels.min(axis=1) > 190)).sum() > 20
    with pytest.raises(FileExistsError):
        pp.render(root, config, output, package)
    changed = json.loads(json.dumps(config))
    changed['narration']['sha256'] = '0' * 64
    with pytest.raises(ValueError, match='hash changed'):
        pp.prepare(root, changed)
    changed = json.loads(json.dumps(config))
    changed['narration']['offset_seconds'] = 1
    with pytest.raises(ValueError, match='exceeds'):
        pp.prepare(root, changed)
