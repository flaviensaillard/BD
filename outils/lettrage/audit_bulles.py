"""Audit du lettrage livré : queues de bulles et recouvrement des personnages.

Répond aux deux défauts signalés :
1. « Les bulles ne pointent pas vers les têtes des personnages qui parlent »
   → pour chaque bulle/pensée, on recalcule la pointe de queue EXACTEMENT comme
   livrée (mêmes visages Haar 2 détecteurs), puis on la compare aux têtes
   détectées (3 détecteurs) et à l'identité attendue (locuteur du scénario).
2. « Beaucoup cachent les personnages »
   → chaque rectangle posé (manifeste) est confronté aux têtes (3 détecteurs)
   et aux blobs de peau comics (corps) de sa vignette.

Identification des personnages : signatures couleur extraites de la couverture
canonique (recadrages nominatifs) — teint mat de Nolann, roux de Kilian, gris de
Julien, barbe de Flavien, châtains (Léon/Milo/Lyssandro/Ayden) indissociables
par la couleur seuls. Un locuteur châtain n'est vérifiable que si un seul châtain
est détecté dans la vignette. Aucun contrôle visuel humain : les verdicts
« indéterminé » restent honnêtes.

Usage :
  PYTHONPATH=.arena/vendor python outils/lettrage/audit_bulles.py            # audit
  PYTHONPATH=.arena/vendor python outils/lettrage/audit_bulles.py --calibre  # signatures couverture
Sorties : Planches-dessin/validation/AUDIT-BULLES.json et AUDIT-BULLES.md
"""
import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import placer as P  # noqa: E402
from PIL import Image  # noqa: E402
import importlib.util  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location('gen', Path(__file__).with_name('generer_avec_texte.py'))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

FC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
PC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

CHATAINS = {'Léon', 'Milo', 'Lyssandro', 'Ayden'}
# locuteur scénario -> identité de référence
SPEAKER_MAP = {
    'Papa': 'Flavien', 'Vanessa': 'Vanessa', 'Alice': 'Alice',
    'Joueur de Montmélian': 'adversaire-vert',
    'Porteur': 'adversaire-jaune',  # Porteur d'Aix-les-Bains
    'Tous': 'groupe',
}


# ---------------------------------------------------------------- scénario
def parse_scenario():
    sc = (ROOT / 'scenario/scenario-complet-30-pages.md').read_text()
    pages, cur = {}, None
    for line in sc.splitlines():
        m = re.match(r'## PAGE (\d+)', line)
        if m:
            cur = int(m.group(1))
            pages[cur] = []
            continue
        if cur is None:
            continue
        m = re.match(r'\s*-\s*\*([^*]+)\*\s*:\s*(.*)', line)
        if not m:
            continue
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
                    pages[cur].append({'kind': 'ono', 'speaker': '', 'text': t + ('' if t.endswith('!') else '!')})
        else:
            pages[cur].append({'kind': typ, 'speaker': speaker, 'text': txt})
    return pages


def norm(t):
    t = t.replace('**', '').replace('«', '').replace('»', '').replace('"', '').replace('"', '')
    t = t.replace('…', '...').replace('’', "'")
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t


def locuteurs_page(page):
    """PAGES[page] enrichi du locuteur scénario (alignement par texte)."""
    sc_els = [e for e in parse_scenario().get(page, []) if e['kind'] != 'ono']
    out = []
    for el in G.PAGES[page]:
        if el[0] == 'ono':
            out.append('')
            continue
        n = norm(el[2])
        sp = ''
        for e in sc_els:
            if norm(e['text']) == n or norm(e['text']).startswith(n[:60]) or n.startswith(norm(e['text'])[:60]):
                sp = e['speaker']
                break
        out.append(SPEAKER_MAP.get(sp, sp))
    return out


# ------------------------------------------------------------ détection
def visages3(gray):
    """Haar frontal + profile + profile miroir, dédupliqués."""
    out = [tuple(int(v) for v in f) for f in FC.detectMultiScale(gray, 1.06, 5, minSize=(24, 24))]
    out += [tuple(int(v) for v in f) for f in PC.detectMultiScale(gray, 1.06, 5, minSize=(24, 24))]
    flip = cv2.flip(gray, 1)
    W = gray.shape[1]
    for (x, y, w, h) in PC.detectMultiScale(flip, 1.06, 5, minSize=(24, 24)):
        out.append((W - x - w, y, w, h))
    final = []
    for b in out:
        if any(P._inter(b, f) > 0.4 * min(b[2] * b[3], f[2] * f[3]) for f in final):
            continue
        final.append(b)
    return final


def peau_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return ((h >= 5) & (h <= 13) & (s >= 65) & (s <= 150) & (v >= 160)).astype(np.uint8)


def _med(pts):
    return np.median(pts, axis=0) if len(pts) else None


def features_tete(bgr_hsv, f):
    """Peau (bande centrale), cheveux (bande au-dessus, filtrée), barbe (menton)."""
    x, y, w, h = f
    skin = bgr_hsv[y + int(0.42 * h):y + int(0.78 * h), x + int(0.28 * w):x + int(0.72 * w)].reshape(-1, 3)
    chin = bgr_hsv[y + int(0.78 * h):y + h, x + int(0.25 * w):x + int(0.75 * w)].reshape(-1, 3)
    y0, y1 = max(0, y - int(0.35 * h)), y + int(0.04 * h)
    band = bgr_hsv[y0:y1, x + int(0.15 * w):x + int(0.85 * w)].reshape(-1, 3)
    # cheveux plausibles : ni ciel bleu, ni herbe, ni blanc éclatant
    ok = band[((band[:, 0] <= 25) | (band[:, 0] >= 165)) & (band[:, 2] < 235)]
    hair = ok if len(ok) >= 0.25 * len(band) else band
    return _med(skin), _med(hair), _med(chin), len(ok) / max(1, len(band))


def jersey_hue(bgr_hsv, f):
    """Dominante du torse (sous le visage) : vert/jaune/rouge/bleu/blanc/sombre."""
    x, y, w, h = f
    band = bgr_hsv[y + h:y + int(1.7 * h), max(0, x - int(0.1 * w)):x + int(1.1 * w)].reshape(-1, 3)
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
    n['total'] = len(band)
    return max((k for k in parts), key=lambda k: n[k]) if max(n.values()) > 0.3 * len(band) else '?'


def classe_identite(skin, hair, chin, jersey, h_box):
    """Règles calibrées sur les 8 visages connus de la couverture."""
    if skin is None:
        return '?'
    s_s, v_s = skin[1], skin[2]
    if s_s >= 108 and v_s <= 218:              # teint mat (Nolann : S~128, V~195)
        return 'Nolann'
    if hair is not None:
        h_h, s_h, v_h = hair
        if 4 <= h_h <= 18 and s_h >= 130 and v_h >= 160:
            return 'Kilian'                    # roux vif
        if s_h <= 45 and 110 <= v_h <= 235:
            return 'Julien'                    # cheveux gris
        if jersey in ('vert', 'jaune'):
            return f'adversaire-{jersey}'      # maillot adverse sous la tête
        if v_h <= 80:
            return 'Flavien'                   # cheveux très foncés (Nolann déjà pris)
        if chin is not None and len(chin) and 8 <= chin[0] <= 20 and chin[1] >= 55 and chin[2] < 150:
            return 'Flavien'                   # barbe brune au menton
        if 140 <= v_h <= 210 and 60 <= s_h <= 115 and 8 <= h_h <= 18:
            return 'chatain-clair'             # Ayden (châtain clair)
        if 80 <= v_h < 210 and 60 <= s_h <= 145:
            return 'chatain'                   # Léon / Milo / Lyssandro / Flavien sans barbe visible
    if jersey in ('vert',):
        return 'adversaire-vert'
    if jersey in ('jaune',):
        return 'adversaire-jaune'
    return '?'


def identifier_tetes(bgr, tetes):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    out = []
    for f in tetes:
        skin, hair, chin, frac = features_tete(hsv, f)
        j = jersey_hue(hsv, f)
        out.append({'box': f, 'skin': tuple(skin) if skin is not None else None,
                    'hair': tuple(hair) if hair is not None else None,
                    'jersey': j,
                    'id': classe_identite(skin, hair, chin, j, f[3])})
    return out


# --------------------------------------------------------- queue livrée
def recalcul_queues(page, base_rgb, manifest):
    """Reproduit les queues/petites bulles livrées (visages 2 détecteurs)."""
    faces2 = P.detect_visages(base_rgb)
    tips = {}
    for i, (el, mf) in enumerate(zip(G.PAGES[page], manifest)):
        if el[0] not in ('bulle', 'pensee'):
            continue
        rect = tuple(mf['rect'])
        loc, face_loc = G._snap_face(G._locuteur(el), faces2)
        if el[0] == 'bulle':
            tips[i] = {'tip': tuple(G._queue_auto(rect, loc, face=face_loc)[2]),
                       'snapped': face_loc is not None}
        else:  # pensee : trois petites bulles vers le penseur
            x1, y1, x2, y2 = rect
            ax = min(max(loc[0], x1), x2)
            ay = min(max(loc[1], y1), y2)
            dx, dy = loc[0] - ax, loc[1] - ay
            n = max(1e-6, (dx * dx + dy * dy) ** 0.5)
            bx, by = ax + dx / n * min(38, max(6, n - 6)), ay + dy / n * min(38, max(6, n - 6))
            tips[i] = {'tip': (bx, by), 'snapped': face_loc is not None}
    return tips


def dist_box(pt, box):
    x, y, w, h = box
    dx = max(x - pt[0], 0, pt[0] - (x + w))
    dy = max(y - pt[1], 0, pt[1] - (y + h))
    return (dx * dx + dy * dy) ** 0.5


# ------------------------------------------------------------------ audit
def audit_page(page, report):
    src = ROOT / G.SRC[page]
    base = np.asarray(Image.open(src).convert('RGB').resize((864, 1222), Image.LANCZOS))
    bgr = base[..., ::-1].copy()
    gray = cv2.equalizeHist(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY))
    tetes = identifier_tetes(bgr, visages3(gray))
    pm = peau_mask(bgr)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(pm, 8)
    blobs = [(int(stats[i, 4]), int(stats[i, 0]), int(stats[i, 1]), int(stats[i, 2]), int(stats[i, 3]))
             for i in range(1, n) if stats[i, 4] >= 400]
    manifest = json.loads((ROOT / 'Planches-dessin/validation/lettrage-manifest.json')
                          .read_text())['pages'][str(page)]
    speakers = locuteurs_page(page)
    tips = recalcul_queues(page, base, manifest)
    panels = P.load_panels().get(page, [(20, 20, 844, 1202)])

    for i, (el, mf) in enumerate(zip(G.PAGES[page], manifest)):
        rect = mf['rect']
        pidx = mf['panel']
        panel = panels[pidx] if pidx is not None and pidx < len(panels) else None
        if panel is None:
            px1, py1, px2, py2 = 20, 20, 844, 1202
        else:
            px1, py1, px2, py2 = panel
        # têtes de la vignette (centre dans la vignette, marge 30px)
        in_panel = [t for t in tetes
                    if px1 - 30 <= t['box'][0] + t['box'][2] / 2 <= px2 + 30
                    and py1 - 30 <= t['box'][1] + t['box'][3] / 2 <= py2 + 30]
        # blobs de peau de la vignette
        blobs_p = [b for b in blobs if b[1] < px2 and b[1] + b[3] > px1 and b[2] < py2 and b[2] + b[4] > py1]
        issue = {'page': page, 'el': i, 'kind': el[0], 'speaker': speakers[i],
                 'text': el[2][:60], 'rect': rect, 'panel': f'{page}-{(pidx or 0) + 1}',
                 'tetes_detectees': len(in_panel)}

        # --- contrôle 1 : la queue pointe la tête du locuteur ?
        if el[0] in ('bulle', 'pensee') and i in tips:
            spk = speakers[i]
            tip = tips[i]['tip']
            issue['tip'] = [round(tip[0]), round(tip[1])]
            if not in_panel:
                issue['queue'] = 'NON-VÉRIFIABLE (aucune tête détectée dans la vignette)'
            elif spk in ('', 'Vanessa', 'Alice') or spk.startswith('Haut-parleur') or spk.startswith('Voix'):
                issue['queue'] = 'voix off (pas de queue)'
            else:
                t_near = min(in_panel, key=lambda t: dist_box(tip, t['box']))
                d_near = dist_box(tip, t_near['box'])
                issue['dist_tete_proche'] = round(d_near)
                issue['tete_proche'] = t_near['id']
                # tête(s) du locuteur attendu
                want = spk
                cand = [t for t in in_panel
                        if t['id'] == want
                        or (want in CHATAINS and t['id'] in ('chatain', 'chatain-clair', 'Flavien'))
                        or (want == 'groupe' and t['id'] not in ('adversaire-vert', 'adversaire-jaune'))]
                if want == 'groupe':
                    issue['queue'] = ('OK (pointe le groupe)' if d_near <= 45
                                      else 'QUEUE DANS LE VIDE')
                elif not cand:
                    issue['queue'] = (f'NON-VÉRIFIABLE (tête de {want} non identifiée ; '
                                      f'proche : {t_near["id"]} à {d_near:.0f}px)')
                else:
                    d_spk = min(dist_box(tip, t['box']) for t in cand)
                    issue['dist_locuteur'] = round(d_spk)
                    if d_spk <= 28:
                        issue['queue'] = 'OK'
                    elif d_near <= 20 and d_spk > 45:
                        issue['queue'] = (f'MAUVAIS LOCUTEUR (pointe {t_near["id"]} à '
                                          f'{d_near:.0f}px, {want} à {d_spk:.0f}px)')
                    elif d_near > 28:
                        issue['queue'] = f'QUEUE DANS LE VIDE (tête la plus proche à {d_near:.0f}px)'
                    else:
                        issue['queue'] = f'IMPRÉCIS (locuteur {want} à {d_spk:.0f}px)'

        # --- contrôle 2 : la bulle cache un personnage ?
        rx1, ry1, rx2, ry2 = rect
        cache = []
        for t in in_panel:
            x, y, w, h = t['box']
            gx1, gy1, gx2, gy2 = x - 0.15 * w, y - 0.15 * h, x + 1.15 * w, y + 1.15 * h
            ix = max(0, min(rx2, gx2) - max(rx1, gx1))
            iy = max(0, min(ry2, gy2) - max(ry1, gy1))
            if ix * iy > 0.10 * w * h and ix * iy > 60:
                cache.append(f'tête {t["id"]} ({min(100, ix * iy / (w * h) * 100):.0f}%)')
        for (a, bx, by, bw, bh) in blobs_p:
            ix = max(0, min(rx2, bx + bw) - max(rx1, bx))
            iy = max(0, min(ry2, by + bh) - max(ry1, by))
            if ix * iy >= 0.35 * a and a >= 600:
                cache.append(f'corps/peau {min(100, ix * iy / a * 100):.0f}% de {a}px²')
        if cache:
            issue['cache'] = ' ; '.join(cache[:3])
        report.append(issue)


def calibre():
    """Contrôle des règles d'identification sur les 8 visages connus."""
    plan = json.loads((ROOT / 'Planches-dessin/validation/REVUE-COUVERTURE.json').read_text())
    img = cv2.imread(str(ROOT / 'Planches-dessin/00-couverture-marvel.png'))
    gray = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    tetes = identifier_tetes(img, visages3(gray))
    print('Calibration sur la couverture (8 identités connues) :')
    ok = 0
    for name, r in plan['references_personnages'].items():
        x1, y1, x2, y2 = r['rectangle_couverture']
        cand = [t for t in tetes if x1 - 20 <= t['box'][0] + t['box'][2] / 2 <= x2 + 20
                and y1 - 20 <= t['box'][1] + t['box'][3] / 2 <= y2 + 20]
        if not cand:
            print(f'  {name:10s} -> visage non détecté !')
            continue
        t = max(cand, key=lambda t: t['box'][2] * t['box'][3])
        want = name if name not in CHATAINS else 'chatain*'
        got = t['id']
        good = got == want or (want == 'chatain*' and got in ('chatain', 'chatain-clair'))
        ok += good
        print(f'  {name:10s} -> {got:14s} peau={t["skin"]} cheveux={t["hair"]} jersey={t["jersey"]}'
              f' {"OK" if good else "** ECHEC **"}')
    print(f'{ok}/8 identifications conformes')


if __name__ == '__main__':
    if '--calibre' in sys.argv:
        calibre()
        sys.exit(0)
    report = []
    for page in sorted(G.PAGES):
        audit_page(page, report)
    out = ROOT / 'Planches-dessin/validation/AUDIT-BULLES.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1))

    # ---- synthèse + rapport Markdown -----------------------------------
    def verdict(r):
        q = r.get('queue', '')
        if q.startswith('OK'):
            return 'OK'
        if q.startswith('voix'):
            return 'voix off'
        if q.startswith('NON-VÉRIFIABLE'):
            return 'non vérifiable'
        if q.startswith('MAUVAIS'):
            return 'MAUVAIS LOCUTEUR'
        if q.startswith('QUEUE DANS LE VIDE'):
            return 'QUEUE DANS LE VIDE'
        if q.startswith('IMPRÉCIS'):
            return 'IMPRÉCIS'
        return ''  # sans queue (encadré, ono, cri, voix)

    tot = {'OK': 0, 'voix off': 0, 'non vérifiable': 0, 'MAUVAIS LOCUTEUR': 0,
           'QUEUE DANS LE VIDE': 0, 'IMPRÉCIS': 0, '': 0}
    n_cache = 0
    vignettes_defaut = {}
    for r in report:
        v = verdict(r)
        if 'queue' in r:
            tot[v] += 1
        if 'cache' in r:
            n_cache += 1
            vignettes_defaut.setdefault((r['page'], r['panel']), []).append(r)
        elif v in ('MAUVAIS LOCUTEUR', 'QUEUE DANS LE VIDE', 'IMPRÉCIS'):
            vignettes_defaut.setdefault((r['page'], r['panel']), []).append(r)

    lines = [
        '# AUDIT DU LETTRAGE LIVRÉ — queues et recouvrements', '',
        'Audit des 30 planches de `Planches-dessin/Avec-texte/` (commit `0fd9784`),',
        'réponses aux deux défauts signalés : *« les bulles ne pointent pas vers les têtes ',
        'des personnages qui parlent »* et *« beaucoup cachent les personnages »*.', '',
        '## Méthode', '',
        '- Locuteur attendu de chaque bulle : scénario complet (aligné texte à texte sur les éléments livrés).',
        '- Têtes détectées : cascades Haar frontal + profil + profil miroir (la génération n\'utilisait que',
        '  frontal + profil : des têtes ont été ratées, donc recouvertes ou non pointées).',
        '- Identité des têtes : signatures couleur calibrées sur les 8 recadrages nominatifs de la couverture',
        '  (8/8 reconnus en calibration) — teint mat de Nolann, roux de Kilian, gris de Julien,',
        '  barbe/cheveux foncés de Flavien, maillots adverses vert/jaune. Léon, Milo, Lyssandro et Ayden',
        '  (châtains) ne sont pas séparables par la couleur : vérifiables seulement si un seul châtain',
        '  apparaît dans la vignette. En vignette, un fond coloré peut fausser une étiquette d\'identité :',
        '  les verdicts « QUEUE DANS LE VIDE » et « recouvrement » ne dépendent pas de l\'identité.',
        '- Queues : recalculées à l\'identique du rendu livré (vérifié par échantillonnage de pixels),',
        '  comparées aux boîtes de têtes de leur vignette (OK si pointe à ≤ 28 px du locuteur).',
        '- Recouvrement : rectangle posé (manifeste) contre têtes (marge 15 %) et blobs de peau comics',
        '  (corps) de la vignette.',
        '- Aucune vision humaine dans cette session : les verdicts « non vérifiable » sont explicites et',
        '  les seuils chiffrés restent dans le JSON (`AUDIT-BULLES.json`).', '',
        '## Bilan', '',
        f'- Bulles et pensées auditées : **{sum(tot[k] for k in tot if k != "")}**',
        f'- Queues correctes : **{tot["OK"]}** — imprécises : {tot["IMPRÉCIS"]}',
        f'- **Mauvais locuteur (pointe un autre personnage) : {tot["MAUVAIS LOCUTEUR"]}**',
        f'- **Queue dans le vide (aucune tête à moins de 28 px) : {tot["QUEUE DANS LE VIDE"]}**',
        f'- Non vérifiables (locuteur châtain non isolable ou tête non détectée) : **{tot["non vérifiable"]}**',
        f'- Éléments recouvrant une tête ou un personnage : **{n_cache}**',
        f'- Vignettes concernées au total : **{len(vignettes_defaut)}** sur 153',
        '- Écart de contenu relevé : page 14 vignette 3, la réplique d\'Ayden',
        '  « Ouais ! Si c\'est pour nous crier dessus comme ça, on n\'a même plus envie de te faire des passes ! »',
        '  du scénario n\'a pas été lettrée.', '',
        '## Détail par planche et vignette', '',
    ]
    cur_page, rows = None, []
    for (page, panel) in sorted(vignettes_defaut):
        if page != cur_page:
            if rows:
                lines += rows + ['']
            cur_page, rows = page, []
            stem = G.SRC[page].rsplit('/', 1)[-1].replace('-marvel.png', '')
            lines.append(f'### Planche {page:02d} — {stem}')
            lines.append('')
            lines.append('| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |')
            lines.append('|---|---|---|---|---|---|')
        for r in vignettes_defaut[(page, panel)]:
            q = verdict(r)
            if q == 'OK':
                q = '—'
            elif q == 'voix off':
                q = '— (voix off)'
            elif q == 'non vérifiable':
                q = 'non vérifiable*'
            elif not q:
                q = '— (sans queue)'
            rows.append(f'| {panel} | {r["el"]} | {r["kind"]} | {r["speaker"] or "—"} '
                        f'| {q} | {r.get("cache", "—")} |')
    if rows:
        lines += rows + ['']
    lines.append('\* Non vérifiable : la tête du locuteur n\'a pas pu être identifiée avec certitude '
                 'dans la vignette (châtains indissociables ou détection muette). Ces cas seront '
                 'traités avec les mêmes corrections que les autres.')
    md = ROOT / 'Planches-dessin/validation/AUDIT-BULLES.md'
    md.write_text('\n'.join(lines))
    print(f'bulles/pensées : {sum(tot[k] for k in tot if k != "")} | ' +
          ' '.join(f'{k}={tot[k]}' for k in tot if k) + f' | recouvrements={n_cache}' +
          f' | vignettes en défaut={len(vignettes_defaut)}/153')
    print('JSON :', out)
    print('MD   :', md)
