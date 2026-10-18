#!/usr/bin/env python3
"""Localité, protections et intégrité de la troisième passe, pas certification graphique."""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def previous(ref, path):
    data = subprocess.check_output(
        ['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(data)).convert('RGB')


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT3-23-30.json').read_text())
    assert {c['page'] for c in plan['corrections']} == {23, 24, 27, 30}
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        old = previous(plan['base'], path)
        new = Image.open(path).convert('RGB')
        assert old.size == new.size, f'Dimensions : {n}'
        changes = [c for c in plan['corrections'] if c['page'] == n]
        diff = ImageChops.difference(old, new)
        assert bool(diff.getbbox()) == bool(changes), f'Présence de retouche : {n}'
        for c in changes:
            box = tuple(c['rectangle'])
            local = diff.crop(box)
            if c['protege']:
                protected = Image.open(ROOT / c['protege']).convert('L')
                assert protected.size == local.size
                assert Image.composite(local, Image.new('RGB', local.size), protected).getbbox() is None, c['vignette']
            if c['masque']:
                mask = Image.open(ROOT / c['masque']).convert('L')
                assert mask.size == local.size
                outside = mask.point(lambda v: 255 if v == 0 else 0)
                diff.paste(Image.composite(local, Image.new('RGB', local.size), outside), box[:2])
            else:
                diff.paste((0, 0, 0), box)
        assert diff.getbbox() is None, f'Changement hors zones/masques : {n}'
        if not changes:
            data = subprocess.check_output(
                ['git', 'show', f'{plan["base"]}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
            assert data == path.read_bytes(), f'Fichier non concerné réécrit : {n}'
        print(f'OK {n:02} : dimensions, périmètre, pixels protégés')
    for e in plan['fichiers_apres']:
        data = (ROOT / e['fichier']).read_bytes()
        assert len(data) == e['octets']
        assert hashlib.sha256(data).hexdigest() == e['sha256']
        with Image.open(BytesIO(data)) as im:
            assert im.format == 'PNG' and list(im.size) == e['dimensions']
            im.verify()
    for g in plan['geometrie']:
        w, h = g['native']
        rw, rh = g['contenu']
        assert abs(rw/w - rh/h) <= 1/min(w, h), g
        x, y, tw, th = g['cadrage']
        assert 0 <= x <= rw-tw and 0 <= y <= rh-th, g
    # Foregrounds and field below the scenery edits are exact, not regenerated.
    for n, box in [(23, (27, 770, 837, 893)), (24, (439, 1036, 837, 1159))]:
        path = next((ROOT / 'Planches-dessin').glob(f'{n}-*.png'))
        assert ImageChops.difference(previous(plan['base'], path).crop(box), Image.open(path).convert('RGB').crop(box)).getbbox() is None
    count = plan['comptage_30_2']
    assert count['enfants_arriere'] == len(count['reperes']['arriere']) == 14
    assert count['enfants_premier_plan'] == len(count['reperes']['premier_plan']) == 5
    assert count['adultes'] == len(count['reperes']['adultes']) == 3
    print('OK : empreintes, géométrie uniforme, champs protégés et cohérence du comptage manuel')
    print('Réserves actuelles : ' + '; '.join(plan['a_reprendre']))
    print('Ces tests ne reconnaissent pas les personnes et ne certifient ni anatomie ni style.')


if __name__ == '__main__':
    main()
