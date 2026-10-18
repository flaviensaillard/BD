#!/usr/bin/env python3
"""Localité/protections de l'audit 5 ; pas une certification artistique."""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def previous(ref, path):
    raw = subprocess.check_output(
        ['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(raw)).convert('RGB')


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT5-23-30.json').read_text())
    assert {(c['page'], c['vignette']) for c in plan['corrections']} == {(27, '27-3'), (30, '30-4')}
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        old, new = previous(plan['base'], path), Image.open(path).convert('RGB')
        assert old.size == new.size, f'Dimensions : {n}'
        changes = [c for c in plan['corrections'] if c['page'] == n]
        diff = ImageChops.difference(old, new)
        assert bool(diff.getbbox()) == bool(changes), f'Présence de retouche : {n}'
        for c in changes:
            box = tuple(c['rectangle'])
            local = diff.crop(box)
            mask = Image.open(ROOT / c['masque']).convert('L')
            protected = Image.open(ROOT / c['protege']).convert('L')
            assert mask.size == protected.size == local.size
            assert ImageChops.multiply(mask, protected).getbbox() is None
            assert Image.composite(local, Image.new('RGB', local.size), protected).getbbox() is None, c['vignette']
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            diff.paste(Image.composite(local, Image.new('RGB', local.size), outside), box[:2])
            if n == 27:
                before, after = old.crop(box), new.crop(box)
                # HSV V = max(R,G,B): exact preservation, not a brightness boost.
                assert ImageChops.difference(before.convert('HSV').getchannel('V'), after.convert('HSV').getchannel('V')).getbbox() is None
                regions = Image.open(ROOT / c['regions']).convert('L')
                assert ImageChops.subtract(mask, regions).getbbox() is None
                folder = (ROOT / c['masque']).parent
                red = Image.open(folder / '27-3-rouge.png').convert('L')
                blue = Image.open(folder / '27-3-bleu.png').convert('L')
                assert ImageChops.lighter(red, blue).tobytes() == mask.tobytes()
                assert red.histogram()[255] == c['pixels_rouges'] > 0
                assert blue.histogram()[255] == c['pixels_bleus'] > 0
                hue = after.convert('HSV').getchannel('H')
                bad_red = hue.point(lambda h: 255 if 2 < h < 249 else 0)
                bad_blue = hue.point(lambda h: 255 if not 151 <= h <= 160 else 0)
                assert ImageChops.multiply(red, bad_red).getbbox() is None
                assert ImageChops.multiply(blue, bad_blue).getbbox() is None
                # Face boxes are independent of the authored clothing color mask.
                for face in [(198,156,211,169), (231,171,243,189), (287,170,300,184), (342,169,357,185)]:
                    assert ImageChops.difference(before.crop(face), after.crop(face)).getbbox() is None
                saturation = before.convert('HSV').getchannel('S')
                whites = saturation.point(lambda v: 255 if v <= 90 else 0)
                assert Image.composite(local, Image.new('RGB', local.size), whites).getbbox() is None
            if n == 30:
                before, after = old.crop(box), new.crop(box)
                for keep in plan['protections_rectangles_locaux'] + [[244,102,270,139]]:
                    assert ImageChops.difference(before.crop(tuple(keep)), after.crop(tuple(keep))).getbbox() is None, keep
        assert diff.getbbox() is None, f'Changement hors zones/masques : {n}'
        if not changes:
            data = subprocess.check_output(
                ['git', 'show', f'{plan["base"]}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
            assert data == path.read_bytes(), f'Fichier non concerné réécrit : {n}'
        print(f'OK {n:02} : dimensions, localité, protections, autres fichiers inchangés')
    for e in plan['fichiers_apres']:
        raw = (ROOT / e['fichier']).read_bytes()
        assert len(raw) == e['octets'] and hashlib.sha256(raw).hexdigest() == e['sha256']
        with Image.open(BytesIO(raw)) as im:
            assert im.format == 'PNG' and list(im.size) == e['dimensions']
            im.verify()
    for g in plan['geometrie']:
        w, h = g['native']
        rw, rh = g['contenu']
        assert abs(rw/w - rh/h) <= 1/min(w, h), g
        x, y, tw, th = g['cadrage']
        assert 0 <= x <= rw-tw and 0 <= y <= rh-th
    print('OK : inventaire, géométrie uniforme, couleurs à V constant, visages et éléments conservés')
    print('Réserves actuelles : ' + '; '.join(plan['a_reprendre']))
    print('Pas de certification automatique des identités, de l’architecture ou du style.')


if __name__ == '__main__':
    main()
