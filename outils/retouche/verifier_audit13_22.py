#!/usr/bin/env python3
"""Contrôle des limites des retouches 13–22. Dépendance : Pillow.

Ne certifie pas la qualité graphique ou l'identité des personnes.
"""
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
BASE = '2dc42ff'


def previous(path):
    raw = subprocess.check_output(['git', 'show', f'{BASE}:{path.as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(raw)).convert('RGB')


REVIEW = ROOT / 'Planches-dessin/validation/REVUE-COUVERTURE.json'
HISTORICAL = json.loads(REVIEW.read_text())['base'] if REVIEW.exists() else None


def delivered(path):
    # Freeze this superseded audit at the start of the cover-authoritative
    # review. Current modifications are checked separately, below, not ignored.
    if HISTORICAL:
        raw = subprocess.check_output(
            ['git', 'show', f'{HISTORICAL}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
        return Image.open(BytesIO(raw)).convert('RGB')
    return Image.open(path).convert('RGB')


def main():
    if HISTORICAL:
        print(f'Audit 13–22 HISTORIQUE : {HISTORICAL} ; contrôle courant distinct en fin de script.')
    report = json.loads((ROOT / 'Planches-dessin/validation/audit-13-22.json').read_text())
    entries = {entry['page']: entry for entry in report['corrections']}
    second_path = ROOT / 'Planches-dessin/validation/AUDIT2-13-22.json'
    second = json.loads(second_path.read_text()) if second_path.exists() else {}
    restored = second.get('restauration_lumiere', {}).get('pages', [])
    for n in range(13, 23):
        path = next((ROOT / 'Planches-dessin').glob(f'{n}-*.png'))
        old = previous(path.relative_to(ROOT))
        new = delivered(path)
        assert old.size == new.size, f'Dimensions : {n}'
        difference = ImageChops.difference(old, new)
        if n == 17:
            assert difference.getbbox() is None, '17 devait rester inchangée'
            print('OK 17 : inchangée')
            continue
        if n in restored:
            assert difference.getbbox() is None, f'Restaurer la lumière claire de {BASE} : {n}'
            print(f'OK {n} : relumage sombre annulé, identique à {BASE}')
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
            # Additional repairs from the second audit are allowed only inside
            # their recorded masks (not everywhere in their context panel).
            for correction in second.get('retouches', {}).get(str(n), []):
                box = tuple(correction['rectangle'])
                if correction.get('masque'):
                    mask = Image.open(ROOT / correction['masque']).convert('L')
                    keep = mask.point(lambda v: 255 if v == 0 else 0)
                    local = Image.composite(difference.crop(box), Image.new('RGB', mask.size), keep)
                    difference.paste(local, box[:2])
                else:
                    difference.paste((0, 0, 0), box)
            assert difference.getbbox() is None, f'Changement hors zones : {n}'
        print(f'OK {n} : dimensions et pixels hors zones conservés')


if __name__ == '__main__':
    main()
    if HISTORICAL:
        subprocess.run([sys.executable, str(ROOT / 'outils/retouche/verifier_revue_couverture.py')], check=True, cwd=ROOT)
