#!/usr/bin/env python3
"""Contrôle des limites des retouches 13–22. Dépendance : Pillow.

Ne certifie pas la qualité graphique ou l'identité des personnes.
"""
from io import BytesIO
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
BASE = '2dc42ff'


def previous(path):
    raw = subprocess.check_output(['git', 'show', f'{BASE}:{path.as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(raw)).convert('RGB')


def main():
    report = json.loads((ROOT / 'Planches-dessin/validation/audit-13-22.json').read_text())
    entries = {entry['page']: entry for entry in report['corrections']}
    for n in range(13, 23):
        path = next((ROOT / 'Planches-dessin').glob(f'{n}-*.png'))
        old = previous(path.relative_to(ROOT))
        new = Image.open(path).convert('RGB')
        assert old.size == new.size, f'Dimensions : {n}'
        difference = ImageChops.difference(old, new)
        if n == 17:
            assert difference.getbbox() is None, '17 devait rester inchangée'
            print('OK 17 : inchangée')
            continue
        assert difference.getbbox() is not None, f'Aucune correction sur {n}'
        item = entries[n]
        if n == 15:
            mask = Image.open(ROOT / 'Planches-dessin/validation/corrections-vignettes/15-masque-cheveux.png').convert('L')
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            assert Image.composite(difference, Image.new('RGB', old.size), outside).getbbox() is None
        elif n == 20:
            box = tuple(item['zone'])
            mask = Image.open(ROOT / 'Planches-dessin/validation/corrections-vignettes/20-3-masque-suppression.png').convert('L')
            local = difference.crop(box)
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            assert Image.composite(local, Image.new('RGB', mask.size), outside).getbbox() is None
            difference.paste((0, 0, 0), box)
            assert difference.getbbox() is None
        else:
            boxes = item.get('zones') or [item['zone']]
            for box in boxes:
                difference.paste((0, 0, 0), tuple(box))
            assert difference.getbbox() is None, f'Changement hors zones : {n}'
        print(f'OK {n} : dimensions et pixels hors zones conservés')


if __name__ == '__main__':
    main()
