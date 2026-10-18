#!/usr/bin/env python3
"""Contrôle technique de la seconde passe 23–30 (Pillow).

Contrôle les limites/pixels protégés, pas l'identité ou l'anatomie générées.
"""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def previous(ref, path):
    raw = subprocess.check_output(['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)
    return Image.open(BytesIO(raw)).convert('RGB')


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/AUDIT2-23-30.json').read_text())
    for n in range(31):
        path = next((ROOT / 'Planches-dessin').glob(f'{n:02}-*.png'))
        old, new = previous(plan['base'], path), Image.open(path).convert('RGB')
        assert old.size == new.size, f'Dimensions {n}'
        changes = [c for c in plan['corrections'] if c['page'] == n]
        diff = ImageChops.difference(old, new)
        assert bool(diff.getbbox()) == bool(changes), f'Présence de retouche {n}'
        for c in changes:
            box = tuple(c['rectangle'])
            local = diff.crop(box)
            if c['protege']:
                protected = Image.open(ROOT / c['protege']).convert('L')
                assert Image.composite(local, Image.new('RGB', protected.size), protected).getbbox() is None, f'Région protégée {c["vignette"]}'
            if c['masque']:
                mask = Image.open(ROOT / c['masque']).convert('L')
                assert mask.size == (box[2]-box[0], box[3]-box[1])
                keep = mask.point(lambda v: 255 if v == 0 else 0)
                outside = Image.composite(local, Image.new('RGB', mask.size), keep)
                diff.paste(outside, box[:2])
            else:
                diff.paste((0, 0, 0), box)
        assert diff.getbbox() is None, f'Pixels hors zones/masques {n}'
        print(f'OK {n:02} : dimensions, changements autorisés, régions protégées')
    for e in plan['fichiers_apres']:
        raw = (ROOT / e['fichier']).read_bytes()
        assert len(raw) == e['octets']
        assert hashlib.sha256(raw).hexdigest() == e['sha256']
        with Image.open(BytesIO(raw)) as im:
            assert list(im.size) == e['dimensions']
            im.verify()
    for g in plan['geometrie']:
        w, h = g['native']; rw, rh = g['contenu']
        assert abs(rw/w - rh/h) <= 1/min(w, h), g
    # All other four cases and the restored frame of 30 are unchanged.
    path = next((ROOT / 'Planches-dessin').glob('30-*.png'))
    assert ImageChops.difference(previous(plan['base'], path).crop((0,379,864,1232)), Image.open(path).convert('RGB').crop((0,379,864,1232))).getbbox() is None
    # Portrait candidate's invented coach jacket must not replace the rugby jersey.
    path = next((ROOT / 'Planches-dessin').glob('29-*.png'))
    box = (439, 337, 837, 376)  # local y >=274, below the edited head
    assert ImageChops.difference(previous(plan['base'], path).crop(box), Image.open(path).convert('RGB').crop(box)).getbbox() is None
    print('OK : empreintes, échelle uniforme, autres cases de 30 et bas du maillot de 29 protégés')
    print('Réserve ouverte : ' + '; '.join(plan['a_reprendre']))
    print('Ces tests ne certifient pas le dessin ou les ressemblances.')


if __name__ == '__main__':
    main()
