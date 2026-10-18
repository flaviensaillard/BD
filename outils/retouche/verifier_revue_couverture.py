#!/usr/bin/env python3
"""Localité de la nouvelle revue ; aucun test ne certifie la ressemblance."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def original(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)


def main():
    plan = json.loads((ROOT / 'Planches-dessin/validation/REVUE-COUVERTURE.json').read_text())
    cover = ROOT / plan['reference_style_et_identites']
    assert hashlib.sha256(cover.read_bytes()).hexdigest() == plan['reference_sha256']
    assert original(plan['base'], cover) == cover.read_bytes(), 'Couverture modifiée'
    assert len(plan['vignettes']) == plan['nombre_vignettes'] == 153
    assert {v['page'] for v in plan['vignettes']} == set(range(1, 31))
    assert len({v['vignette'] for v in plan['vignettes']}) == 153
    assert not any(v['validation_definitive'] for v in plan['vignettes'])
    assert {c['vignette'] for c in plan['corrections']} == {'26-3', '26-6'}
    for e in plan['fichiers_apres']:
        path = ROOT / e['fichier']
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == e['sha256']
        with Image.open(BytesIO(raw)) as im:
            assert im.format == 'PNG' and list(im.size) == e['dimensions']
            im.verify()
        oldraw = original(plan['base'], path)
        before = Image.open(BytesIO(oldraw)).convert('RGB')
        after = Image.open(BytesIO(raw)).convert('RGB')
        assert before.size == after.size
        diff = ImageChops.difference(before, after)
        changes = plan['corrections'] if e['page'] == 26 else []
        for c in changes:
            box = tuple(c['rectangle'])
            local = diff.crop(box)
            mask = Image.open(ROOT / c['masque']).convert('L')
            assert mask.size == local.size and local.getbbox() is not None
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            assert Image.composite(local, Image.new('RGB', local.size), outside).getbbox() is None
            diff.paste(Image.new('RGB', local.size), box[:2])
        assert diff.getbbox() is None, f'Hors corrections : {e["page"]}'
        if not changes:
            assert raw == oldraw, f'Fichier non concerné réécrit : {e["page"]}'
    print('OK : couverture inchangée, 31 empreintes, seulement 26/3 et 26/6 modifiées, localité par masques.')
    print('Inventaire : 153 vignettes ; 2 premières corrections, 151 contrôles individuels encore à faire.')
    print('EN COURS. Aucune validation définitive de ressemblance ou de style par ces tests.')


if __name__ == '__main__':
    main()
