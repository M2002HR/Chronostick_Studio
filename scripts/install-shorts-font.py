#!/usr/bin/env python3
"""Install the licensed Montserrat Bold Shorts font with source provenance."""
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import ImageFont


BASE = 'https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/'


def main():
    target = Path.home() / '.local/share/fonts/chronostick-montserrat'
    target.mkdir(parents=True, exist_ok=True)
    output = target / 'Montserrat-Bold.ttf'
    if output.exists():
        family, face = ImageFont.truetype(str(output), 80).getname()
        if family != 'Montserrat' or face != 'Bold' or not (target / 'source.json').exists():
            raise ValueError('Existing font does not match the documented Montserrat Bold installation')
        print(output)
        return
    font_bytes = urllib.request.urlopen(BASE + 'Montserrat%5Bwght%5D.ttf', timeout=60).read()
    license_bytes = urllib.request.urlopen(BASE + 'OFL.txt', timeout=60).read()
    source = target / 'Montserrat-variable-source.ttf'
    source.write_bytes(font_bytes)
    (target / 'OFL.txt').write_bytes(license_bytes)
    instance = instantiateVariableFont(TTFont(source), {'wght': 700}, updateFontNames=True)
    instance.save(output)
    family, face = ImageFont.truetype(str(output), 80).getname()
    if family != 'Montserrat' or face != 'Bold':
        raise ValueError(f'Expected Montserrat Bold; actual font is {family} {face}')
    provenance = dict(source=BASE + 'Montserrat%5Bwght%5D.ttf',
                      source_sha256=hashlib.sha256(font_bytes).hexdigest(),
                      license_source=BASE + 'OFL.txt', license='SIL-OFL-1.1',
                      license_sha256=hashlib.sha256(license_bytes).hexdigest(),
                      font_path=str(output), font_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                      family=family, face=face, weight=700,
                      processing='Static700-weight instance of official Google Fonts variable source; no outline or glyph edits')
    (target / 'source.json').write_text(json.dumps(provenance, indent=2) + '\n')
    subprocess.run(['fc-cache', str(target)], check=True)
    print(output)


if __name__ == '__main__':
    main()
