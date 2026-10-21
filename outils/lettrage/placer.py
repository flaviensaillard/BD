"""Placement automatique des bulles : ordre de lecture, visages évités, queues courtes.

Deux niveaux :
1. placement glouton (placer) : chaque élément, dans l'ordre du scénario, cherche
   par tailles de police décroissantes la position qui ne recouvre aucun visage
   détecté (cascades Haar), ne chevauche aucune bulle posée, reste dans sa
   vignette et respecte l'ordre de lecture (jamais plus haut, jamais à gauche
   sur la même bande) ; à qualité égale, au plus près du locuteur ;
2. réparation de vignette (reparer_panel) : si un élément d'une vignette n'a pas
   trouvé de position parfaite, toute la vignette est ré-agencée (pile verticale,
   deux colonnes, pleine largeur + deux colonnes…) par tailles décroissantes.
"""
import json
import sys
from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTPATH = str(Path(__file__).with_name('Kalam-Bold.ttf'))
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
PROF_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

_MESUREUR = ImageDraw.Draw(Image.new('RGB', (8, 8)))
# (pad horizontal, pad vertical total, taille max, taille min) par type d'élément
# — cohérents avec les zones de texte réelles des rendus de bd_common.
PADS = {
    'bulle': (10, 12, 14, 8),
    'pensee': (10, 12, 13, 8),
    'voix': (8, 10, 12, 8),
    'encadre': (8, 10, 11, 8),
    'cri': (14, 24, 17, 11),
}


def _nbsp(text):
    return (text.replace(' !', '\u00a0!').replace(' ?', '\u00a0?')
            .replace(' :', '\u00a0:').replace(' ;', '\u00a0;'))


def mesurer(text, width, size, pad, vpad):
    """Hauteur nécessaire (trame 864) pour le texte à cette taille et largeur."""
    f = ImageFont.truetype(FONTPATH, size * 3)
    lines, line = [], ''
    for word in _nbsp(text).split(' '):
        cand = (line + ' ' + word).strip()
        if _MESUREUR.textlength(cand, font=f) > (width - 2 * pad) * 3 and line:
            lines.append(line)
            line = word
        else:
            line = cand
    lines.append(line)
    step = round(size * 3 * 1.18)
    import math
    return math.ceil(len(lines) * step / 3) + vpad + 6


def detect_visages(img_rgb):
    gray = cv2.equalizeHist(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY))
    boxes = []
    for cascade in (FACE_CASCADE, PROF_CASCADE):
        for (x, y, w, h) in cascade.detectMultiScale(gray, 1.06, 5, minSize=(26, 26)):
            mx, my = round(w * 0.18), round(h * 0.18)
            boxes.append((int(max(0, x - mx)), int(max(0, y - my)), int(w + 2 * mx), int(h + 2 * my)))
    final = []
    for b in boxes:
        bx1, by1, bw, bh = b
        if any(_inter(b, f) > 0.5 * min(bw * bh, f[2] * f[3]) for f in final):
            continue
        final.append(b)
    return final


def _inter(a, b):
    ix = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return ix * iy


def load_panels():
    """Vignettes (trame 864x1222) depuis le plan de revue validé, ordre de lecture."""
    plan = json.loads((ROOT / 'Planches-dessin/validation/REVUE-COUVERTURE.json').read_text())
    dims = {e['page']: e['dimensions'] for e in plan['fichiers_apres']}
    panels = {}
    for c in plan['corrections'] + plan.get('relectures_sans_retouche', []):
        p = c['page']
        if p == 0:
            continue
        w, h = dims[p]
        r = c['rectangle']
        box = (round(r[0] * 864 / w), round(r[1] * 1222 / h),
               round(r[2] * 864 / w), round(r[3] * 1222 / h))
        panels.setdefault(p, []).append(box)
    for p in panels:
        # rangées tolérantes (deux vignettes voisines peuvent différer de 1 px)
        panels[p].sort(key=lambda b: (round(b[1] / 40), b[0]))
    return panels


def _panel_of(rect, panels):
    cx, cy = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2
    for i, p in enumerate(panels):  # priorité : la vignette qui contient le centre
        if p[0] <= cx <= p[2] and p[1] <= cy <= p[3]:
            return i, p
    best, best_d = None, 1e9
    for i, p in enumerate(panels):
        px, py = (p[0] + p[2]) / 2, (p[1] + p[3]) / 2
        d = (cx - px) ** 2 + (cy - py) ** 2
        if d < best_d:
            best, best_d = (i, p), d
    return best


def _face_overlap(rect, faces):
    x1, y1, x2, y2 = rect
    box = (x1, y1, x2 - x1, y2 - y1)
    worst = 0.0
    for f in faces:
        inter = _inter(box, f)
        if inter:
            worst = max(worst, inter / min(box[2] * box[3], f[2] * f[3]))
    return worst


def _peau_overlap(rect, zones):
    """Recouvrement d'une zone de peau (x, y, w, h, aire_pixels) : fraction
    de la zone réellement couverte (aire du composant, comme l'audit)."""
    x1, y1, x2, y2 = rect
    box = (x1, y1, x2 - x1, y2 - y1)
    worst = 0.0
    for f in zones:
        inter = _inter(box, f)
        if inter:
            worst = max(worst, inter / f[4])
    return worst


def _placed_overlap(rect, placed):
    x1, y1, x2, y2 = rect
    box = (x1, y1, x2 - x1, y2 - y1)
    worst = 0.0
    for r in placed:
        inter = _inter(box, (r[0], r[1], r[2] - r[0], r[3] - r[1]))
        if inter:
            worst = max(worst, inter / min(box[2] * box[3], (r[2] - r[0]) * (r[3] - r[1])))
    return worst


def _inside_ratio(rect, panel):
    px1, py1, px2, py2 = panel
    ix = max(0, min(rect[2], px2) - max(rect[0], px1))
    iy = max(0, min(rect[3], py2) - max(rect[1], py1))
    return ix * iy / max(1, (rect[2] - rect[0]) * (rect[3] - rect[1]))


def _order_ok(rect, prev):
    if prev is None:
        return True
    below = rect[1] >= prev[1] + 40
    # colonnes disjointes (pas de recouvrement horizontal) : ordre de gauche à droite,
    # une bulle à droite peut monter un peu (disposition en escalier)
    if rect[0] >= prev[2] - 8:
        return rect[1] >= prev[1] - 120
    # à gauche de la précédente : uniquement si c'est la rangée suivante
    if rect[2] <= prev[0] + 8:
        return below
    # même colonne : jamais plus haut que la bulle précédente
    return rect[1] >= prev[1] - 16


def _dist_bord(rect, pt):
    x1, y1, x2, y2 = rect
    dx = max(x1 - pt[0], 0, pt[0] - x2)
    dy = max(y1 - pt[1], 0, pt[1] - y2)
    return (dx * dx + dy * dy) ** 0.5


def placer(kind, text, prefer, faces, placed, panel, speaker=None, prev=None, bodies=(), persos=()):
    """Retourne (rect, taille_police, repli) pour un élément de lettrage."""
    px1, py1, px2, py2 = panel
    pw = px2 - px1
    pad, vpad, smax, smin = PADS[kind]
    w_pref = prefer[2] - prefer[0]
    if kind == 'bulle':
        widths = [min(pw - 12, max(w_pref, 330)), round(0.62 * (pw - 12)), round(0.45 * (pw - 12))]
    elif kind == 'encadre':
        w0 = min(w_pref, pw - 12)
        widths = [w0, round(0.8 * w0)]
    elif kind == 'cri':
        widths = [min(max(w_pref, 220), pw - 12), round(0.6 * (pw - 12))]
    elif kind == 'voix':
        widths = [min(max(round(w_pref * 0.9), 300), pw - 12), round(0.7 * (pw - 12))]
    else:  # pensee
        widths = [min(max(w_pref, 320), pw - 12), round(0.62 * (pw - 12))]
    widths = [max(140, w) for w in widths if w >= 120]

    lo_x, hi_x = px1 - 8, px2 + 8
    lo_y, hi_y = py1 - 8, py2 + 10
    best = None      # (score, rect, size)
    soft = None
    for size in range(smax, smin - 1, -1):
        cands = []
        for w in widths:
            h = mesurer(text, w, size, pad, vpad)
            if h > hi_y - lo_y:
                continue
            for ax, x in (('left', lo_x), ('center', px1 + (pw - w) // 2), ('right', hi_x - w)):
                x = int(max(lo_x, min(x, hi_x - w)))
                for y in range(int(lo_y), int(hi_y - h) + 1, 6):
                    rect = (x, y, x + w, y + h)
                    if _face_overlap(rect, faces) > 0.015:
                        continue
                    if _peau_overlap(rect, bodies) > 0.30:
                        continue   # ne pas cacher un corps entier
                    if _peau_overlap(rect, persos) > 0.45:
                        continue   # ni la silhouette d'un personnage (maillot)
                    if _placed_overlap(rect, placed) > 0.015:
                        continue
                    if _inside_ratio(rect, panel) < 0.8:
                        continue
                    if not _order_ok(rect, prev):
                        continue
                    if speaker is not None:
                        score = _dist_bord(rect, speaker) / 50
                    elif kind == 'encadre':
                        score = (rect[1] - py1) / 12 + (rect[0] - px1) / 30
                    else:
                        score = (rect[1] - py1) / 25 + abs((rect[0] + rect[2]) / 2 - (px1 + px2) / 2) / 40
                    score += abs(rect[1] - prefer[1]) / 500
                    score += (_peau_overlap(rect, bodies) * 25      # ne pas cacher les corps
                              + _peau_overlap(rect, persos) * 12)    # ni les silhouettes
                    if speaker is not None:
                        score += 60 * _blocage_vers(rect, speaker, placed)
                    cands.append((score, rect, size))
        if cands:
            cands.sort(key=lambda c: c[0])
            best = cands[0]
            break
        # mémoriser le moins mauvais (contraintes molles) pour cette taille
        for w in widths:
            h = mesurer(text, w, size, pad, vpad)
            for ax, x in (('left', lo_x), ('center', px1 + (pw - w) // 2), ('right', hi_x - w)):
                x = int(max(lo_x, min(x, hi_x - w)))
                for y in range(int(lo_y), int(hi_y - h) + 1, 12):
                    rect = (x, y, x + w, y + h)
                    pen = (_face_overlap(rect, faces) * 3000
                           + _peau_overlap(rect, bodies) * 1200
                           + _peau_overlap(rect, persos) * 700
                           + _placed_overlap(rect, placed) * 2600
                           + (1 - _inside_ratio(rect, panel)) * 500
                           + (0 if _order_ok(rect, prev) else 400))
                    if speaker is not None:
                        pen += 2500 * _blocage_vers(rect, speaker, placed)
                    if speaker is not None:
                        pen += _dist_bord(rect, speaker) / 80
                    if soft is None or pen < soft[0]:
                        soft = (pen, rect, size)
    if best is not None:
        return best[1], best[2], False
    if soft is not None:
        print(f'  [repli] {kind} : aucune position parfaite, choix le moins mauvais {soft[1]} '
              f'(taille {soft[2]})', file=sys.stderr)
        return soft[1], soft[2], True
    # ultime recours : rectangle préféré
    return tuple(prefer), smin, True


def _blocage_vers(rect, spk, placed):
    """Fraction du trajet rect->locuteur passant à travers des éléments posés."""
    if spk is None or not placed:
        return 0.0
    ax = min(max(spk[0], rect[0]), rect[2])
    ay = min(max(spk[1], rect[1]), rect[3])
    dedans = 0
    for t in range(21):
        t /= 20
        px, py = ax + (spk[0] - ax) * t, ay + (spk[1] - ay) * t
        if any(r[0] <= px <= r[2] and r[1] <= py <= r[3] for r in placed):
            dedans += 1
    return dedans / 21


def _eviter_visages_lignes(x, y, w, h, faces, y_max, tol=0.015):
    """Premier y >= y tel que le rectangle évite les visages (None sinon)."""
    while y + h <= y_max:
        if _face_overlap((x, y, x + w, y + h), faces) <= tol:
            return y
        y += 6
    return None


def reparer_panel(panel, els, faces, placed_other, bodies=(), persos=()):
    """Ré-agence tous les éléments d'une vignette après un repli du placement glouton.

    els : liste ordonnée de dicts {kind, text}. Retourne (rects, taille)
    ou None si aucun agencement ne convient.

    Plus de queues de bulle : le score ne mesure que le recouvrement.
    Les échelons de tolérance sur les têtes sont essayés du plus strict au
    plus souple et le PREMIER qui réussit gagne (jamais au-dessus de 0.058,
    soit ~9,8% de la boîte brute de tête — sous le seuil d'audit de 10%).
    Chaque rangée cherche, parmi les positions sans visage, celle qui couvre
    le moins (peau + silhouette), avec un léger bonus pour rester haute et
    large : on ne prend plus la première place libre au-dessus des têtes.
    Dernier recours sans plafond de peau : mieux vaut un recouvrement
    (avertissement d'audit) qu'un chevauchement de boîtes (bloquant).
    """
    px1, py1, px2, py2 = panel
    pw, ph = px2 - px1, py2 - py1
    n = len(els)
    full = pw - 12
    col = (pw - 24) // 2
    y_max = py2 + 10
    w62 = round(0.62 * full)

    def _cout_couverture(rect, steps):
        """Coût d'une rangée : peau + silhouette + malus de descente."""
        return (_peau_overlap(rect, bodies)
                + 0.5 * _peau_overlap(rect, persos)
                + 0.02 * steps - 0.001 * (rect[2] - rect[0]) / max(full, 1))

    def _meilleure_rangee_seule(i, y, size):
        """Meilleure (x, ty, w, h) pour la rangée i en balayant toutes les
        positions sans visage (plusieurs largeurs, plusieurs x)."""
        meilleur = None
        for w in dict.fromkeys((wof[i], w62)):
            if w < 120:
                continue
            h = mesurer(els[i]['text'], w, size, *PADS[els[i]['kind']][:2])
            cands_x = [px1 + 6]
            if w < pw - 40:
                cands_x += [px1 + (pw - w) // 2, px2 - 6 - w, px1 - 8]
            for x in cands_x:
                ty = y
                while ty + h <= y_max:
                    rect = (x, ty, x + w, ty + h)
                    if _face_overlap(rect, faces) <= tol:
                        cout = _cout_couverture(rect, (ty - y) // 6)
                        if meilleur is None or cout < meilleur[0]:
                            meilleur = (cout, x, ty, w, h)
                    ty += 6
        return meilleur

    for peau_cap in (0.55, None):
        for tol in (0.015, 0.05, 0.058):
            meilleur = None
            for size in range(13, 7, -1):   # plancher 8 : textfit sous 8 impossible
                for arr in ('stack', '2col', 'full+2col', '2col+full'):
                    if arr == 'stack' or n == 1:
                        rows = [[j] for j in range(n)]
                        wof = [full] * n
                    elif arr == '2col':
                        rows = [[j, j + 1] for j in range(0, n, 2)]
                        wof = [col] * n
                    elif arr == 'full+2col':
                        rows = [[0]] + [[j, j + 1] for j in range(1, n, 2)]
                        wof = [full] + [col] * (n - 1)
                    else:  # 2col+full
                        rows = [[j, j + 1] for j in range(0, n - 1, 2)] + [[n - 1]]
                        wof = [col] * (n - 1) + [full]
                    if any(len(r) == 2 and r[1] >= n for r in rows):
                        continue
                    rects = [None] * n
                    y = py1 + 6
                    ok = True
                    for row in rows:
                        row = [j for j in row if j < n]
                        if len(row) == 2:
                            a, b = row
                            ha = mesurer(els[a]['text'], wof[a], size,
                                         *PADS[els[a]['kind']][:2])
                            hb = mesurer(els[b]['text'], wof[b], size,
                                         *PADS[els[b]['kind']][:2])
                            h = max(ha, hb)
                            xa, xb = px1 + 6, px1 + 6 + col + 12
                            meilleur_2c = None
                            ty = y
                            while ty + h <= y_max:
                                ra = (xa, ty, xa + col, ty + ha)
                                rb = (xb, ty, xb + col, ty + hb)
                                if (_face_overlap(ra, faces) <= tol
                                        and _face_overlap(rb, faces) <= tol):
                                    cout = (_cout_couverture(ra, (ty - y) // 6)
                                            + _cout_couverture(rb, 0))
                                    if meilleur_2c is None or cout < meilleur_2c[0]:
                                        meilleur_2c = (cout, ty)
                                ty += 6
                            if meilleur_2c is None:
                                ok = False
                                break
                            yy = meilleur_2c[1]
                            rects[a] = (xa, yy, xa + col, yy + ha)
                            rects[b] = (xb, yy, xb + col, yy + hb)
                            y = yy + h + 6
                        else:
                            i = row[0]
                            choix = _meilleure_rangee_seule(i, y, size)
                            if choix is None:
                                ok = False
                                break
                            _, x, ty, w, h = choix
                            rects[i] = (x, ty, x + w, ty + h)
                            y = ty + h + 6
                    if not ok:
                        continue
                    if any(_placed_overlap(r, placed_other) > 0.015 for r in rects):
                        continue
                    corps = sum(_peau_overlap(r, bodies) for r in rects)
                    sil = sum(_peau_overlap(r, persos) for r in rects)
                    if peau_cap is not None and (
                            any(_peau_overlap(r, bodies) > peau_cap for r in rects)
                            or any(_peau_overlap(r, persos) > 0.45 for r in rects)):
                        continue      # pas de bulle sur un corps ni une silhouette
                    score = corps + 0.5 * sil + 0.15 * (13 - size)
                    if meilleur is None or score < meilleur[0]:
                        meilleur = (score, rects, size)
            if meilleur is not None:
                return meilleur[1], meilleur[2]
    return None
