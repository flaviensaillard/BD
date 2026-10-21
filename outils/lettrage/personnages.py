"""Détection, identification et résolution des personnages pour le lettrage.

Brique commune de la correction du lettrage :
- têtes : cascades Haar (frontal, profil, profil miroir) filtrées par présence
  réelle de peau comics dans la boîte (élimine les faux positifs du style dessiné) ;
- corps : blobs de peau comics associés aux têtes ou orphelins (personne dont la
  tête n'est pas détectée — la zone « tête » est alors le haut du blob) ;
- identité : signatures couleur calibrées sur les 8 recadrages nominatifs de la
  couverture (8/8 en calibration) — teint mat de Nolann, roux de Kilian, gris de
  Julien, cheveux foncés/barbe de Flavien, maillots adverses vert/jaune ;
- scénario : présences et indices de position par vignette (lignes *Visuel*) ;
- résolution : pour chaque élément de lettrage, la tête (ou le corps orphelin) du
  locuteur attendu — identités uniques d'abord, puis affectation optimale des
  châtains indissociables (Léon/Milo/Lyssandro/Ayden) par indice de position et
  proximité des points d'estimation initiaux.
"""
import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

# détecteur Haar reproductible : detectMultiScale n'est pas déterministe en multi-thread
cv2.setNumThreads(1)

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parents[2]
FC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
PC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

CHATAINS = {'Léon', 'Milo', 'Lyssandro', 'Ayden'}
PERSOS = ['Léon', 'Lyssandro', 'Ayden', 'Nolann', 'Milo', 'Flavien', 'Julien', 'Kilian']
SPEAKER_MAP = {
    'Papa': 'Flavien', 'Vanessa': 'Vanessa', 'Alice': 'Alice',
    'Joueur de Montmélian': 'adversaire-vert',
    'Porteur': 'adversaire-jaune',
    'Tous': 'groupe',
    'Joueur de Rumilly': 'adversaire-rumilly',
}
# ids de détection équivalents à un locuteur donné
ID_EQUIV = {
    'Léon': ('chatain',),
    'Milo': ('chatain',),
    'Lyssandro': ('chatain',),
    'Ayden': ('chatain-clair', 'chatain'),
    'Flavien': ('Flavien', 'chatain'),
    'Nolann': ('Nolann', 'Nolann-corps'),
    'Julien': ('Julien',),
    'Kilian': ('Kilian',),
    'adversaire-vert': ('adversaire-vert',),
    'adversaire-jaune': ('adversaire-jaune',),
    'Arbitre': ('arbitre', '?'),
    'groupe': ('chatain', 'chatain-clair', 'Nolann', 'Flavien'),
    'adversaire-rumilly': ('adversaire-vert', 'adversaire-jaune', '?', 'arbitre'),
}


# ------------------------------------------------------------------ peau
def masque_peau(bgr):
    """Peau comics : claire (H 5-13, S 65-150, V 160+) ou mate (Nolann)."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    claire = (h >= 5) & (h <= 13) & (s >= 65) & (s <= 150) & (v >= 160)
    mate = (h >= 6) & (h <= 14) & (s >= 108) & (s <= 165) & (v >= 140) & (v <= 220)
    return ((claire | mate)).astype(np.uint8)


def _med(pts):
    return np.median(pts, axis=0) if len(pts) else None


# ------------------------------------------------------------------ têtes
def _boites_brutes(gray):
    out = [tuple(int(v) for v in f) for f in FC.detectMultiScale(gray, 1.06, 5, minSize=(24, 24))]
    out += [tuple(int(v) for v in f) for f in PC.detectMultiScale(gray, 1.06, 5, minSize=(24, 24))]
    flip = cv2.flip(gray, 1)
    W = gray.shape[1]
    for (x, y, w, h) in PC.detectMultiScale(flip, 1.06, 5, minSize=(24, 24)):
        out.append((W - x - w, y, w, h))
    return out


def _inter(a, b):
    ix = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return ix * iy


def detecter_tetes(bgr):
    """Têtes Haar 3 détecteurs, dédupliquées et filtrées (peau au centre)."""
    gray = cv2.equalizeHist(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY))
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    pm = masque_peau(bgr)
    boxes = []
    for b in _boites_brutes(gray):
        if any(_inter(b, f) > 0.4 * min(b[2] * b[3], f[2] * f[3]) for f in boxes):
            continue
        boxes.append(b)
    tetes = []
    for (x, y, w, h) in boxes:
        # la bande centrale doit contenir de la peau (visage réel, pas un nuage/un fond)
        cx1, cx2 = x + int(0.25 * w), x + int(0.75 * w)
        cy1, cy2 = y + int(0.35 * h), y + int(0.85 * h)
        frac = pm[cy1:cy2, cx1:cx2].mean() if cy2 > cy1 and cx2 > cx1 else 0.0
        if frac < 0.22:
            continue
        skin = hsv[y + int(0.42 * h):y + int(0.78 * h),
                   x + int(0.28 * w):x + int(0.72 * w)].reshape(-1, 3)
        chin = hsv[y + int(0.78 * h):y + h,
                   x + int(0.25 * w):x + int(0.75 * w)].reshape(-1, 3)
        y0, y1 = max(0, y - int(0.35 * h)), y + int(0.04 * h)
        band = hsv[y0:y1, x + int(0.15 * w):x + int(0.85 * w)].reshape(-1, 3)
        ok = band[((band[:, 0] <= 25) | (band[:, 0] >= 165)) & (band[:, 2] < 235)]
        hair = ok if len(ok) >= 0.25 * len(band) else band
        tetes.append({'box': (x, y, w, h),
                      'skin_frac': round(float(frac), 2),
                      'skin': tuple(_med(skin)) if _med(skin) is not None else None,
                      'hair': tuple(_med(hair)) if _med(hair) is not None else None,
                      'chin': tuple(_med(chin)) if _med(chin) is not None else None})
    return tetes


def jersey_sous_tete(hsv, f):
    x, y, w, h = f
    band = hsv[y + h:y + int(1.7 * h), max(0, x - int(0.1 * w)):x + int(1.1 * w)].reshape(-1, 3)
    if not len(band):
        return '?'
    hh, ss, vv = band[:, 0], band[:, 1], band[:, 2]
    parts = {
        'vert': (hh >= 35) & (hh < 85) & (ss > 60),
        'jaune': (hh >= 18) & (hh < 35) & (ss > 80) & (vv > 140),
        'rouge': ((hh < 10) | (hh >= 165)) & (ss > 80) & (vv > 90),
        'bleu': (hh >= 90) & (hh < 135) & (ss > 60),
        'blanc': (ss < 40) & (vv > 180),
        'sombre': vv < 70,
    }
    n = {k: int(v.sum()) for k, v in parts.items()}
    return max(parts, key=lambda k: n[k]) if max(n.values()) > 0.3 * len(band) else '?'


def classe_identite(skin, hair, chin, jersey):
    """Règles calibrées sur les 8 visages connus de la couverture (8/8)."""
    if skin is not None:
        if skin[1] >= 108 and skin[2] <= 218:
            return 'Nolann'
    if hair is not None:
        h_h, s_h, v_h = hair
        if 4 <= h_h <= 18 and s_h >= 130 and v_h >= 160:
            return 'Kilian'
        if s_h <= 45 and 110 <= v_h <= 235:
            return 'Julien'
        if jersey in ('vert', 'jaune'):
            return f'adversaire-{jersey}'
        if v_h <= 80:
            return 'Flavien'
        if chin is not None and 8 <= chin[0] <= 20 and chin[1] >= 55 and chin[2] < 150:
            return 'Flavien'
        if 140 <= v_h <= 210 and 60 <= s_h <= 115 and 8 <= h_h <= 18:
            return 'chatain-clair'
        if 80 <= v_h < 210 and 60 <= s_h <= 145:
            return 'chatain'
    if jersey == 'vert':
        return 'adversaire-vert'
    if jersey == 'jaune':
        return 'adversaire-jaune'
    if jersey == 'sombre':
        return 'arbitre'
    return '?'


# ------------------------------------------------------------- personnages
def detecter_personnages(bgr):
    """Têtes identifiées + corps (blobs de peau), orphelins inclus."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    tetes = detecter_tetes(bgr)
    for t in tetes:
        t['id'] = classe_identite(t['skin'], t['hair'], t['chin'], jersey_sous_tete(hsv, t['box']))
    pm = masque_peau(bgr)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(pm, 8)
    blobs = []
    for i in range(1, n):
        a, bx, by, bw, bh = (int(stats[i, 4]), int(stats[i, 0]), int(stats[i, 1]),
                             int(stats[i, 2]), int(stats[i, 3]))
        if a < 400 or bw > 500 or bh > 500:
            continue
        # blob mat (Nolann) ?
        pix = hsv[by:by + bh, bx:bx + bw][pm[by:by + bh, bx:bx + bw].astype(bool)]
        mat = bool(len(pix)) and float(np.median(pix[:, 1])) >= 108 and float(np.median(pix[:, 2])) <= 220
        blobs.append({'box': (bx, by, bw, bh), 'aire': a, 'mat': mat})
    personnes = []
    for t in tetes:
        x, y, w, h = t['box']
        # corps associé : blob chevauchant la zone sous la tête (torse, bras nus)
        best = None
        for b in blobs:
            zone = (x - int(0.3 * w), y + h, int(1.6 * w), int(1.6 * h) + 30)
            if _inter(zone, b['box']) > 0.25 * b['aire']:
                if best is None or b['aire'] > best['aire']:
                    best = b
        pid = t['id']
        # torse/bras nus au teint mat DIRECTEMENT sous la tête (bande cou)
        # => la tête est celle de Nolann ; le bras mat d'un voisin ne compte pas
        if best is not None and best['mat'] and pid in ('chatain', 'chatain-clair', 'Flavien', '?'):
            bande = (x + int(0.15 * w), y + h, int(0.7 * w), int(0.5 * h) + 10)
            if _inter(bande, best['box']) >= 0.35 * bande[2] * bande[3]:
                pid = 'Nolann'
        personnes.append({'tete': t['box'], 'id': pid, 'tete_obj': t,
                          'corps': best['box'] if best else None})
    prises = [p['corps'] for p in personnes if p['corps']]
    for b in blobs:
        if any(b['box'] is c for c in prises):
            continue
        if any(_inter(b['box'], zone_tete(p)) > 0.3 * b['aire'] for p in personnes if zone_tete(p)):
            continue
        bx, by, bw, bh = b['box']
        personnes.append({'tete': None, 'id': 'Nolann-corps' if b['mat'] else '?',
                          'tete_obj': None, 'corps': b['box'],
                          'zone_tete': (bx + bw // 2 - max(10, bw // 3),
                                        by - max(6, bh // 6),
                                        2 * max(10, bw // 3), int(1.4 * max(10, bh // 3)))})
    return personnes


def zone_tete(personne):
    """Boîte « tête » effective : la tête détectée, ou le haut du corps orphelin."""
    if personne['tete'] is not None:
        return personne['tete']
    return personne.get('zone_tete')


def point_bouche(personne):
    z = zone_tete(personne)
    return (z[0] + z[2] / 2, z[1] + z[3] * 0.62)


def dist_box(pt, box):
    x, y, w, h = box
    dx = max(x - pt[0], 0, pt[0] - (x + w))
    dy = max(y - pt[1], 0, pt[1] - (y + h))
    return (dx * dx + dy * dy) ** 0.5


# ---------------------------------------------------------------- scénario
def parse_scenario():
    """{page: [vignettes]} — chaque vignette : visuel, présence, indices, éléments."""
    sc = (ROOT / 'scenario/scenario-complet-30-pages.md').read_text()
    pages, cur, vig = {}, None, None
    for line in sc.splitlines():
        m = re.match(r'## PAGE (\d+)', line)
        if m:
            cur = int(m.group(1))
            pages[cur] = []
            vig = None
            continue
        if cur is None:
            continue
        mv = re.match(r'\s*-\s*\*\*(?:Vignette|Bande) (\d+)', line)
        if mv:
            vig = {'num': int(mv.group(1)), 'visuel': '', 'elements': []}
            pages[cur].append(vig)
            continue
        m = re.match(r'\s*-\s*\*Visuel\*\s*:\s*(.*)', line)
        if m and vig is not None:
            vig['visuel'] += ' ' + m.group(1)
            continue
        m = re.match(r'\s*-\s*\*([^*]+)\*\s*:\s*(.*)', line)
        if m and vig is not None:
            label, rest = m.group(1).strip(), m.group(2).strip()
            txts = re.findall(r'[«"](.+?)[»"]', rest)
            txt = txts[0].strip() if txts else rest
            mq = re.match(r'^(Bulle de pensée|Bulle|Encadré narratif|Encadré score|'
                          r'Encadré final doré|Encadré|Onomatopée)\s*(?:\((.*)\))?$', label)
            if not mq:
                continue
            typ, qual = mq.group(1), (mq.group(2) or '').strip()
            speaker = qual.split(',')[0].strip() if qual else ''
            if typ == 'Onomatopée':
                for t in re.split(r'!\s+', txt):
                    t = t.strip()
                    if t:
                        vig['elements'].append({'kind': 'ono', 'speaker': '',
                                                'text': t + ('' if t.endswith('!') else '!')})
            else:
                vig['elements'].append({'kind': typ, 'speaker': speaker, 'text': txt})
    # présence + indices de position par vignette
    for p, vigs in pages.items():
        for v in vigs:
            vis = v['visuel']
            pres = [n for n in PERSOS if re.search(rf'\*\*{n}\*\*|\b{n}\b', vis)]
            v['presence'] = set(pres)
            v['match'] = bool(re.search(
                r'tenue|Montmélian|Chambéry|Albertville|Rumilly|Thonon|Le Môle|Aix-les-Bains'
                r'|advers|défenseur|porteur|joueur de|match', vis, re.IGNORECASE))
            hints = {}
            for n in pres:
                if re.search(rf'{n}[^,.;)]*?\bà gauche\b', vis):
                    hints[n] = 'gauche'
                elif re.search(rf'{n}[^,.;)]*?\bà droite\b', vis):
                    hints[n] = 'droite'
                elif re.search(rf'{n}[^,.;)]*?\bcentre\b', vis):
                    hints[n] = 'centre'
            v['hints'] = hints
    return pages


def locuteur_reference(speaker):
    return SPEAKER_MAP.get(speaker, speaker)


# -------------------------------------------------------------- résolution
def _dans_bande(box, bande, panel):
    """bande 'gauche'/'droite'/'centre' sur l'axe x de la vignette."""
    x, y, w, h = box
    cx = x + w / 2
    px1, py1, px2, py2 = panel
    t = (cx - px1) / max(1, px2 - px1)
    if bande == 'gauche':
        return t <= 0.45
    if bande == 'droite':
        return t >= 0.55
    return 0.25 <= t <= 0.75


def _nettoyer_ids(personnes_panel, presence, match=False):
    """Filtre les identités impossibles au vu de la présence scénario.

    Lumière chaude (intérieurs) : un « Nolann » sans Nolann présent devient
    Flavien (adulte) ou châtain ; un roux/gris sans son propriétaire devient
    châtain-clair/châtain. Ne touche pas les adversaires ni les « ? ».
    """
    ids = []
    for p in personnes_panel:
        pid = p['id']
        if pid == 'Nolann' and 'Nolann' not in presence:
            pid = 'Flavien' if 'Flavien' in presence else 'chatain'
        elif pid == 'Nolann-corps' and 'Nolann' not in presence:
            pid = '?'
        elif pid == 'Kilian' and 'Kilian' not in presence:
            pid = 'chatain-clair' if 'Ayden' in presence else 'chatain'
        elif pid == 'Julien' and 'Julien' not in presence:
            pid = 'chatain'
        elif pid == 'Flavien' and 'Flavien' not in presence:
            pid = 'chatain'
        elif pid in ('adversaire-vert', 'adversaire-jaune') and not match:
            pid = 'chatain'
        ids.append(pid)
    return ids


def resoudre_panel(elements, personnes, panel, hints=None, priors=None, presence=None,
                    match=False, x_attendu=None):
    """Associe chaque élément (bulle/pensée) à la personne du locuteur attendu.

    elements : [{idx, speaker}] ; priors : {idx: (x, y)} points d'estimation.
    Retourne {idx: personne ou None}.
    """
    hints = hints or {}
    priors = priors or {}
    presence = presence or set()
    px1, py1, px2, py2 = panel
    dans = []
    for p in personnes:
        z = zone_tete(p)
        if z is None:
            continue
        cx, cy = z[0] + z[2] / 2, z[1] + z[3] / 2
        if px1 - 30 <= cx <= px2 + 30 and py1 - 30 <= cy <= py2 + 30:
            dans.append(p)
    ids = _nettoyer_ids(dans, presence, match=bool(match))
    res = {}
    a_traiter = []
    for e in elements:
        spk = locuteur_reference(e['speaker'])
        e['ref'] = spk
        if spk in ('', 'Vanessa', 'Alice') or spk.startswith('Voix') or spk.startswith('Haut-parleur'):
            res[e['idx']] = None       # voix off : pas de queue
            continue
        equiv = ()
        for part in spk.split('&'):
            part = part.strip()
            equiv += ID_EQUIV.get(part, (part,))
        if spk == 'Arbitre':
            cand = [p for p, i in zip(dans, ids) if i == 'arbitre']
            if not cand:               # arbitre non identifié : personne « ? » proche
                cand = [p for p, i in zip(dans, ids) if i == '?']
                prior = priors.get(e['idx'])
                if cand and prior is not None:
                    cand = sorted(cand, key=lambda q: dist_box(prior, zone_tete(q)))[:1]
        else:
            cand = [p for p, i in zip(dans, ids) if i in equiv]
            # chez les châtains, l'adulte est dessiné plus grand :
            # Flavien garde les grandes têtes, les enfants les petites
            tailles = [zone_tete(p)[3] for p in cand] if cand else []
            if tailles and max(tailles) >= 1.4 * min(tailles):
                if spk == 'Flavien' and not any(i == 'Flavien' for i in ids):
                    cand = [p for p in cand if zone_tete(p)[3] >= 0.8 * max(tailles)]
                elif spk in CHATAINS:
                    cand = [p for p in cand if zone_tete(p)[3] <= 1.25 * min(tailles)]
        if spk in hints and len(cand) > 1:
            filt = [p for p in cand if _dans_bande(zone_tete(p), hints[spk], panel)]
            if filt:
                cand = filt
        if len(cand) == 1:
            res[e['idx']] = cand[0]
            k = dans.index(cand[0])
            dans.pop(k)
            ids.pop(k)
        elif not cand:
            a_traiter.append((e, equiv))   # repli en passe 2 (personne proche de l'estimation)
        else:
            a_traiter.append((e, equiv))
    # 2. châtains restants : proximité des estimations, sinon x attendu (cohérence
    #    de mise en scène), puis biais de taille adulte pour Flavien
    for e, equiv in a_traiter:
        cand = [p for p, i in zip(dans, ids) if i in equiv]
        if not cand:
            # locuteur non identifié : personne la plus proche de l'estimation,
            # si la vignette est peu peuplée ou si une tête est vraiment proche
            prior = priors.get(e['idx'])
            if prior is None:
                res[e['idx']] = None
                continue
            # seules les identités compatibles (ou « ? ») peuvent servir d'ancre
            permis = set(equiv) | {'?'}
            proches = [q for j, q in enumerate(dans) if ids[j] in permis]
            proches = sorted(proches,
                             key=lambda q: dist_box(prior, zone_tete(q))
                             + (0 if q['tete'] is not None else 45))
            d0 = dist_box(prior, zone_tete(proches[0])) if proches else 1e9
            if proches and (len(dans) <= 3 or d0 <= 90):
                res[e['idx']] = proches[0]
            else:
                res[e['idx']] = None
            continue
        prior = priors.get(e['idx'])
        xa = (x_attendu or {}).get(e['ref'])
        if cand:
            if prior is not None:
                cand = sorted(cand, key=lambda p: dist_box(prior, zone_tete(p))
                              + (0 if p['tete'] is not None else 45))
            elif xa is not None:
                cand = sorted(cand, key=lambda p: abs(zone_tete(p)[0] + zone_tete(p)[2] / 2 - xa)
                              + (0 if p['tete'] is not None else 45))
            if e['ref'] == 'Flavien':
                cand = sorted(cand, key=lambda p: (dist_box(prior, zone_tete(p)) if prior else 0)
                                                   - 0.8 * zone_tete(p)[3])
        if cand:
            res[e['idx']] = cand[0]
            k = dans.index(cand[0])
            dans.pop(k)
            ids.pop(k)
        else:
            res[e['idx']] = None
    return res


def resoudre_page(elements_page, personnes, panels, vigs, priors=None):
    """Résolution en deux passes : d'abord les cas certains, puis les châtains
    ambigus en réutilisant la position x du même personnage dans les autres
    vignettes de la page (cohérence de mise en scène)."""
    priors = priors or {}
    par_panel = {}
    for e in elements_page:
        pidx = e['panel']
        par_panel.setdefault(pidx, []).append(e)
    # passe 1 : résolution naïve, mémorisation des ancres certaines
    res = {}
    ancres = {}      # personnage -> liste des x du centre de tête
    for pidx, els in par_panel.items():
        panel = panels[pidx]
        vig = vigs[pidx] if pidx < len(vigs) else {}
        r = resoudre_panel(els, personnes, panel, vig.get('hints'),
                           {e['idx']: priors[e['idx']] for e in els if e['idx'] in priors},
                           vig.get('presence', set()), vig.get('match', False))
        res.update(r)
        for e in els:
            p = r.get(e['idx'])
            if p is not None:
                z = zone_tete(p)
                ancres.setdefault(e['ref'], []).append(z[0] + z[2] / 2)
    # passe 2 : éléments sans ancre + ambiguïtés, avec x attendu par personnage
    attendu = {k: sum(v) / len(v) for k, v in ancres.items() if v}
    res2 = {}
    for pidx, els in par_panel.items():
        panel = panels[pidx]
        vig = vigs[pidx] if pidx < len(vigs) else {}
        if not any(res.get(e['idx']) is None for e in els):
            continue
        # si un personnage a une ancre certaine dans une AUTRE vignette de la page,
        # on réessaie en filtrant ses candidats par proximité de ce x attendu
        r = resoudre_panel(els, personnes, panel, vig.get('hints'),
                           {e['idx']: priors[e['idx']] for e in els if e['idx'] in priors},
                           vig.get('presence', set()), vig.get('match', False), attendu)
        res2.update(r)
    for k, v in res2.items():
        if res.get(k) is None:
            res[k] = v
    return res
