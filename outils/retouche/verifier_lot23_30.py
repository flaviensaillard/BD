#!/usr/bin/env python3
"""Vérifications techniques du lot, sans certification de fidélité graphique."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def main():
    report = json.loads((ROOT / 'Planches-dessin/validation/lot-23-30.json').read_text())
    assert [e['planche'] for e in report['fichiers']] == list(range(23, 31))
    # The initial manifest remains a historical inventory. After a local audit,
    # use its current delivery hashes rather than the superseded batch hashes.
    audit = ROOT / 'Planches-dessin/validation/audit-23-30.json'
    entries = json.loads(audit.read_text())['fichiers_apres'] if audit.exists() else report['fichiers']
    for entry in entries:
        data = (ROOT / entry['fichier']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert len(data) == entry['octets']
        with Image.open(BytesIO(data)) as im:
            assert im.format == 'PNG'
            assert list(im.size) == entry['dimensions']
            assert im.height > im.width >= 700
            im.verify()
        print(f"OK {entry['planche']} : PNG, dimensions, empreinte")
    for n in range(23):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        original = subprocess.check_output(
            ['git', 'show', f"{report['base']}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT)
        assert path.read_bytes() == original, f'Page antérieure modifiée : {n}'
    print('OK 00–22 : fichiers principaux inchangés depuis ' + report['base'])
    print('Pas de validation du contenu ou du style par ces tests.')


if __name__ == '__main__':
    main()
