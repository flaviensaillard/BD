#!/usr/bin/env python3
"""Localité/protections de la sixième passe, sans certification des identités."""
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
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT6-23-30.json').read_text())
    assert {c['vignette'] for c in plan['corrections']} == {'23-1', '23-2', '25-1'}
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        old, new = previous(plan['base'], path), Image.open(path).convert('RGB')
        assert old.size == new.size, f'Dimensions : {n}'
        changes = [c for c in plan['corrections'] if c['page'] == n]
        diff = ImageChops.difference(old, new)
        assert bool(diff.getbbox()) == bool(changes), f'Présence de retouche : {n}'
        for c in changes:
            box = tuple(c['rectangle'])
            before, after = old.crop(box), new.crop(box)
            local = ImageChops.difference(before, after)
            mask = Image.open(ROOT / c['masque']).convert('L')
            protected = Image.open(ROOT / c['protege']).convert('L')
            colors = Image.open(ROOT / c['couleur_masque']).convert('L')
            regions = Image.open(ROOT / c['regions']).convert('L')
            faces = Image.open(ROOT / c['visages_proteges']).convert('L')
            assert mask.size == protected.size == local.size == colors.size
            assert ImageChops.multiply(mask, protected).getbbox() is None
            assert Image.composite(local, Image.new('RGB', local.size), protected).getbbox() is None
            assert ImageChops.subtract(colors, regions).getbbox() is None
            assert ImageChops.multiply(colors, faces).getbbox() is None
            assert colors.histogram()[255] == c['pixels_rouges'] > 0
            assert Image.composite(local, Image.new('RGB', local.size), faces).getbbox() is None
            value_diff = ImageChops.difference(before.convert('HSV').getchannel('V'), after.convert('HSV').getchannel('V'))
            assert ImageChops.multiply(value_diff, colors).getbbox() is None
            bad_red = after.convert('HSV').getchannel('H').point(lambda h: 255 if 2 < h < 249 else 0)
            assert ImageChops.multiply(bad_red, colors).getbbox() is None
            head = Image.open(ROOT / c['tete_masque']).convert('L') if c['tete_masque'] else Image.new('L', local.size)
            assert ImageChops.lighter(head, colors).tobytes() == mask.tobytes()
            # Check low-saturation whites and skin-hued pixels outside the targeted
            # head independently of the authored clothing-region polygons.
            hh, ss, vv = before.convert('HSV').split()
            outside_head = head.point(lambda v: 255 if v == 0 else 0)
            whites = ImageChops.multiply(ss.point(lambda v: 255 if v <= 90 else 0), outside_head)
            assert Image.composite(local, Image.new('RGB', local.size), whites).getbbox() is None
            skin = ImageChops.multiply(hh.point(lambda h: 255 if h < 45 else 0), ss.point(lambda s: 255 if s > 45 else 0))
            skin = ImageChops.multiply(skin, vv.point(lambda v: 255 if v > 40 else 0))
            skin = ImageChops.multiply(skin, outside_head)
            assert Image.composite(local, Image.new('RGB', local.size), skin).getbbox() is None
            if c['vignette'] == '23-2':
                # No regenerated arms or gestures; only central head/neck/collar.
                for keep in [(308,101,393,109), (438,101,506,109)]:
                    assert head.crop(keep).getbbox() is None
                    assert value_diff.crop(keep).getbbox() is None
                allowed = Image.new('L', local.size)
                allowed.paste(255, (390,43,441,105))
                assert ImageChops.subtract(head, allowed).getbbox() is None
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            diff.paste(Image.composite(local, Image.new('RGB', local.size), outside), box[:2])
        assert diff.getbbox() is None, f'Changement hors zones/masques : {n}'
        if not changes:
            raw = subprocess.check_output(
                ['git', 'show', f'{plan["base"]}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
            assert raw == path.read_bytes(), f'Fichier non concerné réécrit : {n}'
        print(f'OK {n:02} : dimensions, masques, protections, fichiers non concernés')
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
    print('OK : empreintes, géométrie uniforme, teintes à V constant, blancs/peaux hors tête protégés')
    print('Réserves actuelles : ' + '; '.join(plan['a_reprendre']))
    print('Les tests ne reconnaissent pas les identités et ne certifient pas le style ou l’anatomie.')


if __name__ == '__main__':
    main()
