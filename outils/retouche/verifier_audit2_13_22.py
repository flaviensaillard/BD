#!/usr/bin/env python3
"""Vérifie la seconde passe contre ce33346 ; Pillow requis.

Prouve les limites des montages, pas l'exactitude des dessins générés.
"""
from io import BytesIO
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def from_git(ref, path):
    raw = subprocess.check_output(['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(raw)).convert('RGB')


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT2-13-22.json').read_text())
    for n in range(13, 23):
        path = next((ROOT / 'Planches-dessin').glob(f'{n}-*.png'))
        old, new = from_git(plan['base'], path), Image.open(path).convert('RGB')
        assert new.size == old.size, f'Dimensions modifiées : {n}'
        diff = ImageChops.difference(old, new)
        changes = plan['retouches'].get(str(n), [])
        assert (diff.getbbox() is not None) == bool(changes), f'Changements attendus : {n}'
        for item in changes:
            box = tuple(item['rectangle'])
            if item['masque']:
                mask = Image.open(ROOT / item['masque']).convert('L')
                assert mask.size == (box[2] - box[0], box[3] - box[1])
                outside = mask.point(lambda v: 255 if v == 0 else 0)
                local = Image.composite(diff.crop(box), Image.new('RGB', mask.size), outside)
                diff.paste(local, box[:2])
            else:
                diff.paste((0, 0, 0), box)
        assert diff.getbbox() is None, f'Pixels modifiés hors zones/masques : {n}'
        if n in plan['restauration_lumiere']['pages']:
            clear = from_git(plan['restauration_lumiere']['base'], path)
            assert ImageChops.difference(clear, new).getbbox() is None, f'Lumière non restaurée : {n}'
        print(f'OK {n} : dimensions, limites et restauration contrôlées')
    # Explicit face/jersey protection in context panels used for local repairs.
    protected = [
        (13, (573, 589, 825, 817)),   # other foreground faces and ball
        (14, (158, 626, 442, 842)),   # three other children, including downward gaze
        (14, (25, 784, 442, 842)),   # jersey badges/lettering
        (16, (26, 551, 837, 776)),   # five heads in hand-stack scene
        (21, (625, 27, 837, 481)),   # coach in top panel
        (21, (27, 495, 425, 670)),   # faces above assistance grip
        (21, (309, 575, 425, 715)),  # seated child's face beside grip
    ]
    for n, box in protected:
        path = next((ROOT / 'Planches-dessin').glob(f'{n}-*.png'))
        old, new = from_git(plan['base'], path), Image.open(path).convert('RGB')
        assert ImageChops.difference(old.crop(box), new.crop(box)).getbbox() is None, f'Protection {n}: {box}'
    for g in plan['geometrie']:
        w, h = g['native']; rw, rh = g['contenu_redimensionne']
        # Integer rounding only; less than one target pixel of scale discrepancy.
        assert abs(rw / w - rh / h) <= 1 / min(w, h), g
    print('OK : régions protégées et redimensionnements à échelle uniforme')


if __name__ == '__main__':
    main()
