#!/usr/bin/env python3
"""Contrôle technique final ; les décisions visuelles ne sont pas automatisées."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def previous(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT-FINAL-23-30.json').read_text())
    expected = {f'{n}-{i}' for n, count in [(23, 4), (24, 5), (25, 5), (26, 6), (27, 5), (28, 6), (29, 4), (30, 5)] for i in range(1, count+1)}
    assert len(plan['vignettes']) == 40
    assert {c['vignette'] for c in plan['vignettes']} == expected
    assert not plan['reprise_identifiee_non_traitee']
    assert len(plan['corrections']) == 30
    assert sum(c['type'] == 'teinte_vetements' for c in plan['corrections']) == 29
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        raw = previous(plan['base'], path)
        old = Image.open(BytesIO(raw)).convert('RGB')
        new = Image.open(path).convert('RGB')
        assert old.size == new.size
        diff = ImageChops.difference(old, new)
        changes = [c for c in plan['corrections'] if c['page'] == n]
        assert bool(diff.getbbox()) == bool(changes), n
        for c in changes:
            box = tuple(c['rectangle'])
            before, after = old.crop(box), new.crop(box)
            local = ImageChops.difference(before, after)
            mask = Image.open(ROOT / c['masque']).convert('L')
            regions = Image.open(ROOT / c['regions']).convert('L')
            assert mask.size == local.size == regions.size
            assert mask.histogram()[255] == c['pixels'] > 0
            assert ImageChops.subtract(mask, regions).getbbox() is None
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            assert Image.composite(local, Image.new('RGB', local.size), outside).getbbox() is None
            assert ImageChops.difference(before.convert('HSV').getchannel('V'), after.convert('HSV').getchannel('V')).getbbox() is None
            if c['type'] == 'teinte_vetements':
                faces = Image.open(ROOT / c['visages']).convert('L')
                assert ImageChops.multiply(mask, faces).getbbox() is None
                assert Image.composite(local, Image.new('RGB', local.size), faces).getbbox() is None
                hue, saturation, value = before.convert('HSV').split()
                # Independently check hue family, whites and skin preservation.
                eligible_hue = hue.point(lambda h: 255 if 210 <= h <= 247 else 0)
                assert ImageChops.subtract(mask, eligible_hue).getbbox() is None
                whites = saturation.point(lambda s: 255 if s <= 90 else 0)
                skin = ImageChops.multiply(hue.point(lambda h: 255 if h < 45 else 0), saturation.point(lambda s: 255 if s > 45 else 0))
                skin = ImageChops.multiply(skin, value.point(lambda v: 255 if v > 40 else 0))
                for keep in [whites, skin]:
                    assert Image.composite(local, Image.new('RGB', local.size), keep).getbbox() is None
                bad_hue = after.convert('HSV').getchannel('H').point(lambda h: 255 if 2 < h < 249 else 0)
                assert ImageChops.multiply(mask, bad_hue).getbbox() is None
            else:
                assert c['vignette'] == '30-5'
                hand = Image.open(ROOT / c['main']).convert('L')
                assert ImageChops.multiply(mask, hand).getbbox() is None
                assert Image.composite(local, Image.new('RGB', local.size), hand).getbbox() is None
                cream = Image.open(ROOT / c['creme']).convert('L')
                seam = Image.open(ROOT / c['lisere']).convert('L')
                assert ImageChops.lighter(cream, seam).tobytes() == mask.tobytes()
                hh, ss, vv = after.convert('HSV').split()
                bad_cream = hh.point(lambda h: 255 if not 26 <= h <= 33 else 0)
                bad_red = hh.point(lambda h: 255 if 2 < h < 249 else 0)
                assert ImageChops.multiply(cream, bad_cream).getbbox() is None
                assert ImageChops.multiply(seam, bad_red).getbbox() is None
                dark_ink = before.convert('HSV').getchannel('V').point(lambda v: 255 if v <= 85 else 0)
                assert Image.composite(local, Image.new('RGB', local.size), dark_ink).getbbox() is None
            diff.paste(Image.new('RGB', local.size), box[:2])
        assert diff.getbbox() is None, f'Hors vignettes : {n}'
        if not changes:
            assert raw == path.read_bytes(), f'Fichier non concerné réécrit : {n}'
        print(f'OK {n:02} : dimensions, localité, protections, V constant ; non concernés inchangés')
    for e in plan['fichiers_apres']:
        raw = (ROOT / e['fichier']).read_bytes()
        assert len(raw) == e['octets'] and hashlib.sha256(raw).hexdigest() == e['sha256']
        with Image.open(BytesIO(raw)) as im:
            assert im.format == 'PNG' and list(im.size) == e['dimensions']
            im.verify()
    # Source-crop provenance and the complete forty-case comparison inventory.
    source_case = next(c for c in plan['vignettes'] if c['vignette'] == '30-5')
    page = ROOT / next(e['fichier'] for e in plan['fichiers_apres'] if e['planche'] == 30)
    source = Image.open(BytesIO(previous(plan['source'], page))).convert('RGB')
    expected_crop = source.crop(tuple(source_case['source_rectangle']))
    actual = Image.open(ROOT / 'Planches-dessin/validation/corrections-vignettes/audit23-final/30-5-source.png').convert('RGB')
    assert ImageChops.difference(expected_crop, actual).getbbox() is None
    for n in range(23, 31):
        with Image.open(ROOT / f'Planches-dessin/validation/AUDIT-FINAL-{n}-VIGNETTES.jpg') as im:
            im.verify()
    print('OK : 40 décisions, 30 retouches locales, 8 empreintes, source du ballon et comparaisons')
    print('Contrôle actif terminé. Pas de certification automatique des identités, de l’anatomie ou du style.')


if __name__ == '__main__':
    main()
