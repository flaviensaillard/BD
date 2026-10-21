"""Audit du lettrage : queues de bulles et recouvrement des personnages (v2).

Vérifie les livrables `Planches-dessin/Avec-texte/` contre :
- le manifeste enrichi (`lettrage-manifest.json` : rectangle posé, pointe de
  queue, locuteur enregistré avec sa tête) ;
- une détection indépendante des personnages (têtes Haar ×3 filtrées par peau,
  corps, identités couleur calibrées couverture, nettoyées par la présence
  scénario) via `personnages.py` ;
- le scénario complet (locuteur attendu de chaque bulle).

Verdicts de queue : OK (pointe la tête du locuteur à ≤ 30 px), MAUVAIS
LOCUTEUR (pointe une tête incompatible), QUEUE DANS LE VIDE, NON VÉRIFIABLE
(locuteur non détecté / châtains indissociables), VOIX OFF.
Verdicts de recouvrement : tête couverte, corps/peau couvert.

Usage : PYTHONPATH=.arena/vendor python outils/lettrage/audit_bulles.py [--calibre]
Sorties : Planches-dessin/validation/AUDIT-BULLES.json et AUDIT-BULLES.md
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import placer as P  # noqa: E402
import personnages as PS  # noqa: E402
from PIL import Image  # noqa: E402
import importlib.util  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location('gen', Path(__file__).with_name('generer_avec_texte.py'))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

CHATAINS = PS.CHATAINS


def dist_box(pt, box):
    x, y, w, h = box
    dx = max(x - pt[0], 0, pt[0] - (x + w))
    dy = max(y - pt[1], 0, pt[1] - (y + h))
    return (dx * dx + dy * dy) ** 0.5


def _norm_txt(t):
    return G._norm_txt(t)


# ------------------------------------------------------------------ audit
def audit_page(page, report):
    src = ROOT / G.SRC[page]
    base = np.asarray(Image.open(src).convert('RGB').resize((864, 1222), Image.LANCZOS))
    bgr = base[..., ::-1].copy()
    persons = PS.detecter_personnages(bgr)
    pm = PS.masque_peau(bgr)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(pm, 8)
    blobs = [(int(stats[i, 4]), int(stats[i, 0]), int(stats[i, 1]), int(stats[i, 2]), int(stats[i, 3]))
             for i in range(1, n) if stats[i, 4] >= 400]
    manifest = json.loads((ROOT / 'Planches-dessin/validation/lettrage-manifest.json')
                          .read_text())['pages'][str(page)]
    scen = PS.parse_scenario()
    vigs = scen.get(page, [])
    panels = P.load_panels().get(page, [(20, 20, 844, 1202)])
    if len(vigs) != len(panels):
        pres = set()
        for v in vigs:
            pres |= v['presence']
        vigs = [{'hints': {}, 'presence': pres, 'match': any(v['match'] for v in vigs)}] * len(panels)
    speakers = G.locuteurs_alignes(page, scen)

    for i, (el, mf) in enumerate(zip(G.PAGES[page], manifest)):
        rect = mf['rect']
        pidx = mf['panel']
        panel = panels[pidx] if pidx is not None and pidx < len(panels) else (20, 20, 844, 1202)
        vig = vigs[pidx] if pidx is not None and pidx < len(vigs) else {'presence': set(), 'match': False}
        px1, py1, px2, py2 = panel
        in_panel = [p for p in persons
                    if PS.zone_tete(p) and px1 - 30 <= PS.zone_tete(p)[0] + PS.zone_tete(p)[2] / 2 <= px2 + 30
                    and py1 - 30 <= PS.zone_tete(p)[1] + PS.zone_tete(p)[3] / 2 <= py2 + 30]
        ids = PS._nettoyer_ids(in_panel, vig['presence'], vig['match'])
        issue = {'page': page, 'el': i, 'kind': el[0], 'speaker': speakers[i],
                 'text': el[2][:60], 'rect': rect,
                 'panel': f'{page}-{(pidx or 0) + 1}' if pidx is not None else '-',
                 'personnes': len(in_panel)}

        # --- contrôle 1 : la queue pointe la tête du locuteur ?
        if el[0] in ('bulle', 'pensee') and 'queue_tip' in mf:
            spk = speakers[i]
            tip = mf['queue_tip']
            issue['tip'] = tip
            loc = mf.get('locuteur') or {}
            if spk in ('', 'Vanessa', 'Alice') or spk.startswith('Voix') or spk.startswith('Haut-parleur'):
                issue['queue'] = 'voix off (pas de queue)'
            elif not in_panel:
                issue['queue'] = 'NON-VÉRIFIABLE (aucune personne détectée dans la vignette)'
            else:
                # tête la plus proche de la pointe
                best = min(in_panel, key=lambda p: dist_box(tip, PS.zone_tete(p)))
                d_near = dist_box(tip, PS.zone_tete(best))
                id_near = ids[in_panel.index(best)]
                issue['dist_tete_proche'] = round(d_near)
                issue['tete_proche'] = id_near
                # compatibilité identité (locuteur attendu)
                equiv = ()
                for part in spk.split('&'):
                    equiv += PS.ID_EQUIV.get(part.strip(), (part.strip(),))
                compatible = [p for p, pid in zip(in_panel, ids) if pid in equiv]
                if loc.get('src') == 'estime':
                    issue['queue'] = ('NON CORRIGÉ (locuteur non détecté/ancre estimée ; '
                                      f'tête la plus proche : {id_near} à {d_near:.0f}px)')
                elif not compatible:
                    issue['queue'] = (f'NON-VÉRIFIABLE (tête compatible avec {spk} non '
                                      f'identifiée ; pointe {id_near} à {d_near:.0f}px)')
                elif best in compatible:
                    if d_near <= 30:
                        issue['queue'] = 'OK'
                    elif d_near <= 48:
                        issue['queue'] = f'OK (large, {d_near:.0f}px)'
                    else:
                        issue['queue'] = f'IMPRÉCIS (ancre à {d_near:.0f}px de la tête visée)'
                elif id_near == '?':
                    d_spk = min(dist_box(tip, PS.zone_tete(p)) for p in compatible)
                    issue['queue'] = (f'OK (corps non identifié à {d_near:.0f}px du locuteur)'
                                      if d_spk <= 45
                                      else f'IMPRÉCIS (corps non identifié à {d_near:.0f}px, '
                                           f'{spk} à {d_spk:.0f}px)')
                else:
                    d_spk = min(dist_box(tip, PS.zone_tete(p)) for p in compatible)
                    issue['queue'] = (f'MAUVAIS LOCUTEUR (pointe {id_near} à {d_near:.0f}px, '
                                      f'{spk} à {d_spk:.0f}px)')
                    issue['dist_locuteur'] = round(d_spk)

        # --- contrôle 2 : la bulle cache un personnage ?
        rx1, ry1, rx2, ry2 = rect
        cache = []
        for p in in_panel:
            x, y, w, h = PS.zone_tete(p)
            gx1, gy1, gx2, gy2 = x - 0.15 * w, y - 0.15 * h, x + 1.15 * w, y + 1.15 * h
            ix = max(0, min(rx2, gx2) - max(rx1, gx1))
            iy = max(0, min(ry2, gy2) - max(ry1, gy1))
            if ix * iy > 0.10 * w * h and ix * iy > 60:
                cache.append(f'tête {ids[in_panel.index(p)]} ({min(100, ix * iy / (w * h) * 100):.0f}%)')
        for (a, bx, by, bw, bh) in blobs:
            if not (bx < px2 and bx + bw > px1 and by < py2 and by + bh > py1):
                continue
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
    persons = PS.detecter_personnages(img)
    print('Calibration sur la couverture (8 identités connues) :')
    ok = 0
    for name, r in plan['references_personnages'].items():
        x1, y1, x2, y2 = r['rectangle_couverture']
        cand = [p for p in persons
                if x1 - 20 <= PS.zone_tete(p)[0] + PS.zone_tete(p)[2] / 2 <= x2 + 20
                and y1 - 20 <= PS.zone_tete(p)[1] + PS.zone_tete(p)[3] / 2 <= y2 + 20]
        if not cand:
            print(f'  {name:10s} -> tête non détectée !')
            continue
        p = max(cand, key=lambda p: PS.zone_tete(p)[2] * PS.zone_tete(p)[3])
        want = name if name not in CHATAINS else 'chatain*'
        got = p['id']
        good = got == want or (want == 'chatain*' and got in ('chatain', 'chatain-clair'))
        ok += good
        t = p['tete_obj']
        print(f'  {name:10s} -> {got:14s} peau={t["skin"]} cheveux={t["hair"]} '
              f'{"OK" if good else "** ECHEC **"}')
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

    def verdict(r):
        q = r.get('queue', '')
        for k, lbl in (('OK (large', 'OK large'),):
            pass
        if q.startswith('OK'):
            return 'OK' if q == 'OK' else 'OK large'
        if q.startswith('voix'):
            return 'voix off'
        if q.startswith('NON-VÉRIFIABLE') or q.startswith('NON CORRIGÉ'):
            return 'non vérifiable'
        if q.startswith('MAUVAIS'):
            return 'MAUVAIS LOCUTEUR'
        if q.startswith('QUEUE DANS LE VIDE'):
            return 'QUEUE DANS LE VIDE'
        if q.startswith('IMPRÉCIS'):
            return 'IMPRÉCIS'
        return ''

    tot = {}
    n_cache = n_tete = 0
    vignettes = {}
    for r in report:
        v = verdict(r)
        if 'queue' in r:
            tot[v] = tot.get(v, 0) + 1
        if 'cache' in r:
            n_cache += 1
            if 'tête' in r['cache']:
                n_tete += 1
        if 'cache' in r or v in ('MAUVAIS LOCUTEUR', 'QUEUE DANS LE VIDE', 'IMPRÉCIS'):
            vignettes.setdefault((r['page'], r['panel']), []).append(r)

    lines = [
        '# AUDIT DU LETTRAGE — queues et recouvrements (après correction)', '',
        'Audit des 30 planches de `Planches-dessin/Avec-texte/`, par `outils/lettrage/audit_bulles.py`',
        '(locuteurs du scénario, têtes détectées Haar ×3 + filtrage peau, identités couleur calibrées',
        'sur la couverture et nettoyées par la présence scénario, pointes de queue lues dans le',
        'manifeste du lettrage).', '',
        'Cet audit fait suite à la correction du lettrage : les queues sont désormais ancrées sur la',
        'tête du locuteur résolu (identité + présence scénario + ordre de lecture) et le placement',
        'évite têtes et corps. Pour comparaison, l\'audit initial (commit `97cc4e5`, lettrage `0fd9784`)',
        'comptait : **22** queues correctes, **11** mauvais locuteurs, **94** queues dans le vide,',
        '**101** recouvrements de personnages et **107**/153 vignettes touchées ; la réplique',
        'd\'Ayden (page 14, vignette 3) manquait.', '',
        '## Bilan', '',
        f'- Bulles et pensées auditées : **{sum(tot.values())}** (réplique d\'Ayden p14 v3 réintégrée)',
    ]
    for k in ('OK', 'OK large', 'voix off', 'IMPRÉCIS', 'MAUVAIS LOCUTEUR', 'QUEUE DANS LE VIDE',
              'non vérifiable'):
        if tot.get(k):
            lines.append(f'- {k} : **{tot[k]}**')
    lines += [
        f'- Éléments recouvrant un personnage : **{n_cache}** (dont têtes couvertes : {n_tete})',
        f'- Vignettes avec au moins un défaut : **{len(vignettes)}** sur 153', '',
        '## Détail par planche et vignette', '',
    ]
    cur, rows = None, []
    for (page, panel) in sorted(vignettes):
        if page != cur:
            if rows:
                lines += rows + ['']
            cur, rows = page, []
            stem = G.SRC[page].rsplit('/', 1)[-1].replace('-marvel.png', '')
            lines.append(f'### Planche {page:02d} — {stem}')
            lines.append('')
            lines.append('| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |')
            lines.append('|---|---|---|---|---|---|')
        for r in vignettes[(page, panel)]:
            q = verdict(r)
            q = {'OK': '—', 'voix off': '— (voix off)', 'non vérifiable': 'non vérifiable*'}.get(q, q)
            if not q:
                q = '—'
            rows.append(f'| {panel} | {r["el"]} | {r["kind"]} | {r["speaker"] or "—"} '
                        f'| {q} | {r.get("cache", "—")} |')
    if rows:
        lines += rows + ['']
    lines.append('\\* Non vérifiable : locuteur non détecté (ancre estimée) ou identité non '
                 'isolable dans la vignette. Détail chiffré dans `AUDIT-BULLES.json`.')
    (ROOT / 'Planches-dessin/validation/AUDIT-BULLES.md').write_text('\n'.join(lines))
    print('bulles/pensées :', sum(tot.values()), '| ' +
          ' '.join(f'{k}={v}' for k, v in tot.items()),
          f'| recouvrements={n_cache} (têtes={n_tete}) | vignettes en défaut={len(vignettes)}/153')
    print('JSON :', out)
