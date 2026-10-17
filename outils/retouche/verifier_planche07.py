#!/usr/bin/env python3
"""Vérifie les invariants des retouches masquées de la planche 07.

Dépendance : Pillow. À lancer depuis n'importe quel répertoire du dépôt.
Compare les pixels décodés, pas les octets PNG (la compression peut changer).
Ne démontre pas à lui seul la qualité graphique ni l'exactitude du détourage.
"""
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'Planches-dessin/validation/corrections-vignettes/controle-passe-3.json'


def main():
    report = json.loads(REPORT.read_text())
    data = subprocess.check_output(
        ['git', 'show', f"{report['commit_avant']}:{report['fichier']}"], cwd=ROOT
    )
    before = Image.open(BytesIO(data)).convert('RGB')
    after = Image.open(ROOT / report['fichier']).convert('RGB')
    assert before.size == after.size, 'Dimensions modifiées'
    outside = ImageChops.difference(before, after)
    for item in report['controles']:
        box = tuple(item['rectangle'])
        old = before.crop(box)
        new = after.crop(box)
        mask = Image.open(ROOT / item['masque']).convert('L')
        assert mask.size == old.size
        protected_diff = Image.composite(
            ImageChops.difference(old, new), Image.new('RGB', old.size), mask
        )
        assert protected_diff.getbbox() is None, f"Pixels protégés modifiés : {item['vignette']}"
        assert ImageChops.difference(old, new).getbbox() is not None, 'Aucune retouche'
        outside.paste((0, 0, 0), box)
        print(f"OK {item['vignette']} : pixels protégés identiques")
    assert outside.getbbox() is None, 'Pixels modifiés hors des cases autorisées'
    print('OK : dimensions et pixels hors cases inchangés')


if __name__ == '__main__':
    main()
