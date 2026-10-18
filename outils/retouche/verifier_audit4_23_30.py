#!/usr/bin/env python3
"""Contrôle technique de la quatrième passe ; pas de reconnaissance des personnes."""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def previous(ref, path):
    data = subprocess.check_output(
        ['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(data)).convert('RGB')


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT4-23-30.json').read_text())
    fifth = ROOT / 'Planches-dessin/validation/AUDIT5-23-30.json'
    historical = json.loads(fifth.read_text())['base'] if fifth.exists() else None
    def delivered(path):
        return previous(historical, path) if historical else Image.open(path).convert('RGB')
    if historical:
        print(f'Vérification historique quatrième passe : {historical}')
    assert [c['vignette'] for c in plan['corrections']] == ['24-5', '24-2']
    assert {c['page'] for c in plan['corrections']} == {24}
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        old, new = previous(plan['base'], path), delivered(path)
        assert old.size == new.size, f'Dimensions : {n}'
        changes = [c for c in plan['corrections'] if c['page'] == n]
        diff = ImageChops.difference(old, new)
        assert bool(diff.getbbox()) == bool(changes), f'Présence de retouche : {n}'
        for c in changes:
            box = tuple(c['rectangle'])
            local = diff.crop(box)
            protected = Image.open(ROOT / c['protege']).convert('L')
            mask = Image.open(ROOT / c['masque']).convert('L')
            assert mask.size == protected.size == local.size
            assert ImageChops.multiply(mask, protected).getbbox() is None
            assert Image.composite(local, Image.new('RGB', local.size), protected).getbbox() is None, c['vignette']
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            diff.paste(Image.composite(local, Image.new('RGB', local.size), outside), box[:2])
        assert diff.getbbox() is None, f'Changement hors zones/masques : {n}'
        if not changes:
            data = subprocess.check_output(
                ['git', 'show', f'{plan["base"]}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
            actual = subprocess.check_output(['git', 'show', f'{historical}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT) if historical else path.read_bytes()
            assert data == actual, f'Fichier non concerné réécrit : {n}'
        print(f'OK {n:02} : dimensions, zones, protections et fichiers non concernés')
    for e in plan['fichiers_apres']:
        data = subprocess.check_output(['git', 'show', f"{historical}:{e['fichier']}"], cwd=ROOT) if historical else (ROOT / e['fichier']).read_bytes()
        assert len(data) == e['octets'] and hashlib.sha256(data).hexdigest() == e['sha256']
        with Image.open(BytesIO(data)) as im:
            assert im.format == 'PNG' and list(im.size) == e['dimensions']
            im.verify()
    for g in plan['geometrie']:
        w, h = g['native']
        rw, rh = g['contenu']
        assert abs(rw/w - rh/h) <= 1/min(w, h), g
        x, y, tw, th = g['cadrage']
        assert 0 <= x <= rw-tw and 0 <= y <= rh-th
    path = next((ROOT / 'Planches-dessin').glob('24-*.png'))
    old = previous(plan['base'], path)
    new = delivered(path)
    # The upper scenery of 24/5 is deliberately not regenerated this time.
    box = (439, 836, 837, 1036)
    assert ImageChops.difference(old.crop(box), new.crop(box)).getbbox() is None
    # Independently check pale road/floor pixels, not only the authored edit mask.
    box = (439, 836, 837, 1159)
    before = old.crop(box)
    _, saturation, value = before.convert('HSV').split()
    pale = ImageChops.multiply(saturation.point(lambda v: 255 if v <= 45 else 0),
                               value.point(lambda v: 255 if v >= 150 else 0))
    pale.paste(0, (0, 0, 398, 200))
    assert pale.histogram()[255] > 1000
    local = ImageChops.difference(before, new.crop(box))
    assert Image.composite(local, Image.new('RGB', local.size), pale).getbbox() is None
    print('OK : inventaire, échelles uniformes, fond haut 24/5 et pixels clairs du chemin conservés')
    print(('Réserves historiques de cette passe : ' if historical else 'Réserves actuelles : ') + '; '.join(plan['a_reprendre']))
    print('Ces tests ne certifient ni identité, ni anatomie, ni homogénéité graphique intégrale.')
    if historical:
        sys.stdout.flush()
        subprocess.run([sys.executable, str(ROOT / 'outils/retouche/verifier_audit5_23_30.py')], check=True)


if __name__ == '__main__':
    main()
