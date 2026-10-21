"""Contrôle du lettrage final : bulles jamais sur les visages, ordre de lecture, livrables.

Vérifie le manifeste produit par generer_avec_texte.py (rectangles réellement posés)
contre une détection de visages indépendante (cascades Haar OpenCV 4.x).

Contrôle aussi l'audit via `AUDIT-BULLES.json` : le lettrage ne pointe plus
les locuteurs, chaque dialogue est préfixé du nom du personnage
(« Léon: "…" ») sur fond blanc, la narration sur fond jaune/brun. Sont exigés :
0 préfixe faux, 0 fond non conforme, 0 tête couverte ; les recouvrements de
corps résiduels en planches denses sont listés en avertissements.

Dépendances : OpenCV 4.x avec cascades (`.arena/vendor`), Pillow, NumPy.
Usage : PYTHONPATH=.arena/vendor python outils/lettrage/verifier_lettrage.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from generer_avec_texte import PAGES, SRC, dst_path  # noqa: E402
from bd_common import ROOT  # noqa: E402
import personnages as PS  # noqa: E402


def rect_overlap(rect, face):
    fx, fy, fw, fh = face
    ix = max(0, min(rect[2], fx + fw) - max(rect[0], fx))
    iy = max(0, min(rect[3], fy + fh) - max(rect[1], fy))
    inter = ix * iy
    if inter <= 0:
        return 0.0
    return inter / min((rect[2] - rect[0]) * (rect[3] - rect[1]), fw * fh)


def main():
    manifest = json.loads((ROOT / 'Planches-dessin/validation/lettrage-manifest.json').read_text())
    errors = 0

    print('--- Contrôle têtes (détection 3 cascades + filtrage peau, rectangles posés) ---')
    total = 0
    for page in sorted(PAGES, key=int):
        base = np.asarray(Image.open(ROOT / SRC[int(page)]).convert('RGB')
                          .resize((864, 1222), Image.LANCZOS))
        pers = PS.detecter_personnages(base[..., ::-1].copy())
        tetes = []
        for q in pers:
            z = PS.zone_tete(q)
            if z is not None:
                x, y, w, h = z
                tetes.append((x - 0.15 * w, y - 0.15 * h, 1.3 * w, 1.3 * h))
        for i, el in enumerate(manifest['pages'][str(page)]):
            rect = el['rect']
            total += 1
            worst = max((rect_overlap(rect, f) for f in tetes), default=0.0)
            if worst > 0.10:
                errors += 1
                print(f'  ATTENTION page {page} élément {i} ({el["kind"]}) rect={rect} '
                      f'chevauche une tête (pire {worst * 100:.0f}%)')
    if errors == 0:
        print(f'  OK : {total} éléments de lettrage, aucun ne chevauche une tête détectée.')

    print('--- Contrôle ordre de lecture (jamais plus haut, jamais à gauche sur la bande) ---')
    ordre_ok = True
    for page in sorted(PAGES, key=int):
        prev = None
        for i, el in enumerate(manifest['pages'][str(page)]):
            if el['kind'] == 'ono' or 'panel' not in el:
                continue
            rect = el['rect']
            if prev is not None:
                if el['panel'] < prev['panel']:
                    print(f'  ATTENTION page {page} élément {i} ({el["kind"]}) : vignette '
                          f'{el["panel"]} après {prev["panel"]}')
                    ordre_ok = False
                elif el['panel'] == prev['panel']:
                    pr = prev['rect']
                    below = rect[1] >= pr[1] + 40
                    if rect[0] >= pr[2] - 8:      # colonne à droite : escalier toléré
                        ok = rect[1] >= pr[1] - 120
                    elif rect[2] <= pr[0] + 8:    # à gauche : seulement rangée suivante
                        ok = below
                    else:                          # même colonne : jamais plus haut
                        ok = rect[1] >= pr[1] - 16
                    if not ok:
                        print(f'  ATTENTION page {page} élément {i} ({el["kind"]}) hors ordre : '
                              f'{rect} après {pr}')
                        ordre_ok = False
            prev = el
    if ordre_ok:
        print('  OK : ordre de lecture respecté sur toutes les planches.')

    print('--- Contrôle chevauchements entre bulles ---')
    overlap_ok = True
    for page in sorted(PAGES, key=int):
        rects = [el['rect'] for el in manifest['pages'][str(page)]]
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]
                ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
                iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
                if ix * iy > 0.02 * min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])):
                    print(f'  ATTENTION page {page} : éléments {i} et {j} se chevauchent.')
                    overlap_ok = False
    if overlap_ok:
        print('  OK : aucune bulle ne se chevauche.')

    print('--- Contrôle locuteurs nommés et fonds (audit) ---')
    audit = json.loads((ROOT / 'Planches-dessin/validation/AUDIT-BULLES.json').read_text())
    bloquant = 0
    ncorps = 0
    for r in audit:
        if 'prefixe' in r:
            bloquant += 1
            print(f'  BLOQUANT page {r["page"]:02d} élément {r["el"]} '
                  f'({r["speaker"]}) : préfixe locuteur faux — {r["prefixe"]}')
        if 'fond' in r:
            bloquant += 1
            print(f'  BLOQUANT page {r["page"]:02d} élément {r["el"]} '
                  f'({r["kind"]}) : fond {r["fond"]}')
        if 'cache' in r:
            if 'tête' in r['cache']:
                bloquant += 1
                print(f'  BLOQUANT page {r["page"]:02d} élément {r["el"]} couvre une tête : {r["cache"]}')
            else:
                ncorps += 1
    if bloquant == 0:
        print('  OK : chaque dialogue nomme son locuteur (préfixe conforme au scénario), '
              'fonds conformes (blanc/dialogue, jaune-brun/narration), aucune tête couverte.')
    print(f'  avertissements : {ncorps} recouvrements de corps résiduels '
          f'(planche dense, sans position libre).')
    errors += bloquant

    print('--- Contrôle livrables ---')
    missing = [p for p in sorted(PAGES, key=int) if not (ROOT / dst_path(int(p))).exists()]
    if missing:
        errors += len(missing)
        print(f'  MANQUANT : pages {missing}')
    else:
        print(f'  OK : {len(PAGES)} planches lettrées dans Planches-dessin/Avec-texte/.')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
