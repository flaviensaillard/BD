#!/usr/bin/env python3
"""Contrôle localité/dimensions de l'audit 23–30, pas la fidélité graphique."""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def old_image(ref, path):
    raw = subprocess.check_output(['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(raw)).convert('RGB')


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/audit-23-30.json').read_text())
    second = ROOT / 'Planches-dessin/validation/AUDIT2-23-30.json'
    historical = json.loads(second.read_text())['base'] if second.exists() else None
    def delivered(path):
        if historical:
            return old_image(historical, path)
        return Image.open(path).convert('RGB')
    if historical:
        print(f'Vérification historique première passe : {historical} ; puis seconde passe actuelle.')
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        old, new = old_image(plan['base'], path), delivered(path)
        assert old.size == new.size, f'Dimensions : {n}'
        diff = ImageChops.difference(old, new)
        changes = [c for c in plan['corrections'] if c['page'] == n]
        if n == plan['page_reconstruite']:
            assert diff.getbbox() is not None
            # White page outside the five source-layout frames, not a deformed grid.
            for item in changes:
                x0, y0, x1, y1 = item['rectangle']
                diff.paste((0, 0, 0), (x0-2, y0-2, x1+2, y1+2))
            white = new.copy()
            for item in changes:
                x0, y0, x1, y1 = item['rectangle']
                white.paste('white', (x0-2, y0-2, x1+2, y1+2))
            assert ImageChops.difference(white, Image.new('RGB', new.size, 'white')).getbbox() is None
        else:
            assert bool(diff.getbbox()) == bool(changes), f'Changement attendu : {n}'
            for item in changes:
                box = tuple(item['rectangle'])
                mask = Image.open(ROOT / item['masque']).convert('L')
                assert mask.size == (box[2]-box[0], box[3]-box[1])
                outside = mask.point(lambda v: 255 if v == 0 else 0)
                local = Image.composite(diff.crop(box), Image.new('RGB', mask.size), outside)
                diff.paste(local, box[:2])
            assert diff.getbbox() is None, f'Pixels hors masques : {n}'
        print(f'OK {n:02} : dimensions et périmètre de correction')
    for entry in plan['fichiers_apres']:
        data = subprocess.check_output(['git', 'show', f"{historical}:{entry['fichier']}"], cwd=ROOT) if historical else (ROOT / entry['fichier']).read_bytes()
        assert len(data) == entry['octets']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
    for g in plan['geometrie']:
        w, h = g['native']; nw, nh = g['redimensionne']
        assert abs(nw/w - nh/h) <= 1/min(w, h), g
    # Explicitly protect every actor, ball and jersey in 23/1.
    path = next((ROOT / 'Planches-dessin').glob('23-*.png'))
    old = old_image(plan['base'], path)
    new = delivered(path)
    assert ImageChops.difference(old.crop((27,151,837,326)), new.crop((27,151,837,326))).getbbox() is None
    # Centre and right child in 26/3 have not been regenerated.
    path = next((ROOT / 'Planches-dessin').glob('26-*.png'))
    assert ImageChops.difference(old_image(plan['base'], path).crop((215,675,425,918)), delivered(path).crop((215,675,425,918))).getbbox() is None
    print('OK : empreintes, échelle uniforme et personnages protégés')
    if historical:
        sys.stdout.flush()
        subprocess.run([sys.executable, str(ROOT / 'outils/retouche/verifier_audit2_23_30.py')], check=True)
    else:
        print(f"ATTENTION : {len(plan['a_reprendre'])} vignettes restent à reprendre ; aucune validation graphique globale.")


if __name__ == '__main__':
    main()
