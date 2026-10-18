#!/usr/bin/env python3
"""Contrôle technique cumulatif de la revue, jamais certification des ressemblances."""
from collections import Counter
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
    frames = plan['vignettes']
    assert len(frames) == plan['nombre_vignettes'] == 153
    assert {v['page'] for v in frames} == set(range(1, 31))
    assert len({v['vignette'] for v in frames}) == 153
    assert not any(v['validation_definitive'] for v in frames)
    changes = plan['corrections']
    ids = {c['vignette'] for c in changes}
    assert len(ids) == len(changes), 'Correction dupliquée'
    assert ids == {v['vignette'] for v in frames if v['etat'] != 'a_controler_individuellement'}
    assert {e['page'] for e in plan['fichiers_apres']} == set(range(31))
    assert len(plan['fichiers_apres']) == 31
    for c in changes:
        assert c['page'] == int(c['vignette'].split('-')[0])
        assert c['type'] in {'reprise_graphique', 'correction_partielle'}
    for e in plan['fichiers_apres']:
        path = ROOT / e['fichier']
        raw = path.read_bytes()
        assert len(raw) == e['octets']
        assert hashlib.sha256(raw).hexdigest() == e['sha256']
        with Image.open(BytesIO(raw)) as im:
            assert im.format == 'PNG' and list(im.size) == e['dimensions']
            im.verify()
        oldraw = original(plan['base'], path)
        before = Image.open(BytesIO(oldraw)).convert('RGB')
        after = Image.open(BytesIO(raw)).convert('RGB')
        assert before.size == after.size
        diff = ImageChops.difference(before, after)
        page_changes = [c for c in changes if c['page'] == e['page']]
        for c in page_changes:
            box = tuple(c['rectangle'])
            assert 0 <= box[0] < box[2] <= after.width
            assert 0 <= box[1] < box[3] <= after.height
            local = diff.crop(box)
            mask = Image.open(ROOT / c['masque']).convert('L')
            assert mask.size == local.size and local.getbbox() is not None, c['vignette']
            outside = mask.point(lambda v: 255 if v == 0 else 0)
            assert Image.composite(local, Image.new('RGB', local.size), outside).getbbox() is None, c['vignette']
            diff.paste(Image.new('RGB', local.size), box[:2])
        assert diff.getbbox() is None, f'Hors corrections : {e["page"]}'
        if not page_changes:
            assert raw == oldraw, f'Fichier non concerné réécrit : {e["page"]}'
    counts = Counter(c['type'] for c in changes)
    pending = sum(v['etat'] == 'a_controler_individuellement' for v in frames)
    partial_ids = {c['vignette'] for c in changes if c['type'] == 'correction_partielle'}
    assert partial_ids == {v['vignette'] for v in frames if v['etat'] == 'correction_partielle_reste_a_reprendre'}
    bilan = plan['bilan']
    assert bilan['vignettes_inventoriees'] == len(frames)
    assert bilan['vignettes_corrigees_premiere_passe'] == counts['reprise_graphique']
    assert bilan['vignettes_correction_partielle'] == counts['correction_partielle']
    assert bilan['vignettes_a_controler_individuellement'] == pending
    assert bilan['validations_definitives'] == 0
    print('OK : couverture inchangée, 31 empreintes/dimensions, seules les corrections déclarées ont changé, localité par masques.')
    print(f"Inventaire : 153 vignettes ; {counts['reprise_graphique']} premières reprises, {counts['correction_partielle']} corrections partielles, {pending} contrôles individuels encore à faire.")
    print('EN COURS. Aucune validation définitive de ressemblance ou de style par ces tests.')


if __name__ == '__main__':
    main()
