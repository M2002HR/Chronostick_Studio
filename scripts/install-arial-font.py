#!/usr/bin/env python3
"""Install genuine Arial locally from the unchanged Core Fonts package; never execute its EXE."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request

URL = 'https://downloads.sourceforge.net/project/corefonts/the%20fonts/final/arial32.exe'


def main():
    if not shutil.which('7z'):
        raise SystemExit('7z is required to extract the package (Debian/Ubuntu package: 7zip).')
    target = Path.home() / '.local/share/fonts/chronostick-arial'
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='chronostick-arial-') as temp:
        temp = Path(temp)
        archive = temp / 'arial32.exe'
        urllib.request.urlretrieve(URL, archive)
        subprocess.run(['7z', 'x', '-y', '-o' + str(temp / 'fonts'), str(archive)], check=True, stdout=subprocess.DEVNULL)
        fonts = list((temp / 'fonts').glob('*.TTF'))
        if len(fonts) != 4 or not any(p.name == 'Arialbd.TTF' for p in fonts):
            raise RuntimeError('Arial package did not contain the expected font family')
        for font in fonts:
            dest = target / font.name
            if dest.exists() and dest.read_bytes() != font.read_bytes():
                raise FileExistsError(f'Refusing to replace a different font: {dest}')
            if not dest.exists():
                shutil.copyfile(font, dest)
        provenance = dict(source=URL, archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                          fonts={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in fonts},
                          install_directory=str(target), processing='extract only; installer never executed')
        (target / 'source.json').write_text(json.dumps(provenance, indent=2) + '\n')
    subprocess.run(['fc-cache', str(target)], check=True)
    print(subprocess.check_output(['fc-match', 'Arial:style=Bold'], text=True).strip())


if __name__ == '__main__':
    main()
