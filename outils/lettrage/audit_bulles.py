"""Audit du lettrage : queues de bulles et recouvrement des personnages (v2).

Vérifie les livrables `Planches-dessin/Avec-texte/` contre :
- le manifeste enrichi (`lettrage-manifest.json` : rectangle posé, locuteur
  attendu, texte affiché) ;
- le scénario complet (locuteur attendu de chaque réplique) ;
- une détection indépendante des personnages (têtes Haar ×3 filtrées par peau,
  corps, identités couleur calibrées couverture, nettoyées par la présence
  scénario) via `personnages.py` ;
- la planche lettrée elle-même (couleur de fond échantillonnée).

Le lettrage ne pointe plus les locuteurs : chaque dialogue est préfixé
(« Léon: "…" ») sur fond blanc ; la narration est sur fond jaune/brun.
Verdicts : préfixe locuteur, fond blanc/jaune, tête couverte, corps/peau couvert.

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
             for i in range(1, n) if stats[i, 4] >= 450]
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
    zones_perso = G._zones_persos(persons)   # silhouettes (maillots compris)
    # planche finale lettrée (contrôle des fonds blanc / jaune-brun)
    final = np.asarray(Image.open(ROOT / G.dst_path(page)).convert('RGB'))

    for i, (el, mf) in enumerate(zip(G.PAGES[page], manifest)):
        rect = mf['rect']
        pidx = mf['panel']
        panel = panels[pidx] if pidx is not None and pidx < len(panels) else (20, 20, 844, 1202)
        vig = vigs[pidx] if pidx is not None and pidx < len(vigs) else {'presence': set(), 'match': False}
        px1, py1, px2, py2 = panel
        in_panel = [p for p in persons
                    if PS.zone_tete(p) and px1 - 30 <= PS.zone_tete(p)[0] + PS.zone_tete(p)[2] / 2 <= px2 + 30
                    and py1 - 30 <= PS.zone_tete(p)[1] + PS.zone_tete(p)[3] / 2 <= py2 + 30]
        issue = {'page': page, 'el': i, 'kind': el[0], 'speaker': speakers[i] or None,
                 'text': mf.get('texte', '')[:70], 'rect': rect,
                 'panel': f'{page}-{(pidx or 0) + 1}' if pidx is not None else '-',
                 'personnes': len(in_panel)}

        # --- contrôle 1 : le texte affiché nomme-t-il le bon locuteur ? -----
        spk = speakers[i] if i < len(speakers) else ''
        attendu = G._texte_affiche(el, spk)
        fautes = []
        if (mf.get('speaker') or None) != (spk or None):
            fautes.append(f'locuteur manifeste={mf.get("speaker")!r} vs scénario={spk!r}')
        if mf.get('texte') != attendu:
            fautes.append(f'texte={mf.get("texte", "")[:45]!r} vs attendu={attendu[:45]!r}')
        if fautes:
            issue['prefixe'] = ' ; '.join(fautes)

        # --- contrôle 2 : fond blanc (dialogue) / jaune-brun (narratif) ----
        voulu = ('jaune' if el[0] == 'encadre'
                 else 'blanc' if el[0] in G._KINDS_DIAL else None)
        if voulu:
            couleur = _fond(final, rect)
            if couleur != voulu:
                issue['fond'] = f'{couleur} au lieu de {voulu}'

        # --- contrôle 3 : la boîte cache-t-elle un personnage ? ------------
        rx1, ry1, rx2, ry2 = rect
        cache = []
        visages = list(in_panel)
        for p in in_panel:            # orphelins « forme de tête » = visage probable
            if p['tete'] is None and p.get('corps'):
                bx, by, bw, bh = p['corps']
                if 22 <= bw <= 90 and 22 <= bh <= 90 and bw * bh >= 500 \
                        and 0.55 <= bw / bh <= 1.8:
                    visages.append(p)
        for p in visages:
            x, y, w, h = PS.zone_tete(p)
            gx1, gy1, gx2, gy2 = x - 0.15 * w, y - 0.15 * h, x + 1.15 * w, y + 1.15 * h
            ix = max(0, min(rx2, gx2) - max(rx1, gx1))
            iy = max(0, min(ry2, gy2) - max(ry1, gy1))
            if ix * iy > 0.10 * w * h and ix * iy > 60:
                idp = ids_locale(in_panel, p, vig)
                cache.append(f'tête {idp} ({min(100, ix * iy / (w * h) * 100):.0f}%)')
        for (a, bx, by, bw, bh) in blobs:
            if not (bx < px2 and bx + bw > px1 and by < py2 and by + bh > py1):
                continue
            ix = max(0, min(rx2, bx + bw) - max(rx1, bx))
            iy = max(0, min(ry2, by + bh) - max(ry1, by))
            if ix * iy >= 0.35 * a and a >= 450:
                cache.append(f'corps/peau {min(100, ix * iy / a * 100):.0f}% de {a}px²')
        if cache:
            issue['cache'] = ' ; '.join(cache[:3])

        # --- contrôle 4 : la boîte couvre-t-elle la silhouette d'un personnage ?
        # (torse/jambes présumés sous une tête détectée : un personnage en maillot
        #  n'apparaît pas dans le masque de peau mais ne doit pas être caché)
        if el[0] != 'ono':
            rx1, ry1, rx2, ry2 = rect
            sil = 0.0
            for (zx, zy, zw, zh, za) in zones_perso:
                ix = max(0, min(rx2, zx + zw) - max(rx1, zx))
                iy = max(0, min(ry2, zy + zh) - max(ry1, zy))
                if ix * iy > 0:
                    sil = max(sil, ix * iy / za)
            if sil > 0.45:
                issue['perso'] = f'cache {min(100, sil * 100):.0f}% d\'un personnage'
        report.append(issue)


def ids_locale(in_panel, p, vig):
    """Identité affichable d'une personne pour le message « tête couverte »."""
    ids = PS._nettoyer_ids(in_panel, vig['presence'], vig['match'])
    try:
        return ids[in_panel.index(p)]
    except (ValueError, IndexError):
        return 'visage probable'


def _fond(img, rect):
    """Couleur de fond d'une boîte posée : 'blanc', 'jaune' ou 'autre'.

    Médiane des pixels clairs du rectangle (texte/contours exclus)."""
    x1, y1, x2, y2 = [max(0, int(v)) for v in rect]
    x2, y2 = min(x2, img.shape[1]), min(y2, img.shape[0])
    if x2 <= x1 or y2 <= y1:
        return 'autre'
    crop = img[y1:y2, x1:x2].reshape(-1, 3)
    clairs = crop[(crop >= 110).all(axis=1)]
    if len(clairs) < 20:
        return 'autre'
    r, g, b = np.median(clairs, axis=0)
    if r >= 225 and g >= 225 and b >= 225:
        return 'blanc'
    if r >= 195 and r - b >= 30 and g >= b:
        return 'jaune'
    return 'autre'


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

    n_dial = n_enc = 0
    n_prefixe = n_fond = n_cache = n_tete = n_perso = 0
    vignettes = {}
    for r in report:
        if r['kind'] in G._KINDS_DIAL:
            n_dial += 1
        elif r['kind'] == 'encadre':
            n_enc += 1
        if 'prefixe' in r:
            n_prefixe += 1
        if 'fond' in r:
            n_fond += 1
        if 'cache' in r:
            n_cache += 1
            if 'tête' in r['cache']:
                n_tete += 1
        if 'perso' in r:
            n_perso += 1
        if 'prefixe' in r or 'fond' in r or 'cache' in r or 'perso' in r:
            vignettes.setdefault((r['page'], r['panel']), []).append(r)

    lines = [
        '# AUDIT DU LETTRAGE — locuteurs nommés, fonds et recouvrements', '',
        'Audit des 30 planches de `Planches-dessin/Avec-texte/`, par',
        '`outils/lettrage/audit_bulles.py`. Le lettrage ne pointe plus les',
        'locuteurs : chaque dialogue est préfixé du nom du personnage',
        '(« Léon: \"…\" ») sur fond blanc, la narration est sur fond',
        'jaune/brun. Contrôles : préfixe conforme au scénario, fond de la',
        'boîte (échantillonné sur la planche finale), recouvrement des',
        'personnes (têtes et zones de peau, détection indépendante).', '',
        '## Bilan', '',
        f'- Dialogues (bulles, pensées, voix, cris) : **{n_dial}**, '
        f'encadrés narratifs : **{n_enc}**',
        f'- Préfixes de locuteur faux : **{n_prefixe}**',
        f'- Fonds non conformes (blanc/dialogue, jaune-brun/narratif) : **{n_fond}**',
        f'- Éléments recouvrant de la peau (corps nus) : **{n_cache}** '
        f'(dont têtes/visages couverts : {n_tete})',
        f'- Éléments cachant un personnage (silhouette, maillot compris) : **{n_perso}**',
        f'- Vignettes avec au moins un défaut : **{len(vignettes)}** sur 153', '',
    ]
    if vignettes:
        lines += ['## Détail par planche et vignette', '']
        cur = None
        rows = []
        for (page, panel) in sorted(vignettes):
            if page != cur:
                if rows:
                    lines += rows + ['']
                cur, rows = page, []
                stem = G.SRC[page].rsplit('/', 1)[-1].replace('-marvel.png', '')
                lines += [f'### Planche {page:02d} — {stem}', '',
                          '| Vignette | Él. | Type | Locuteur | Défauts |',
                          '|---|---|---|---|---|']
            for r in vignettes[(page, panel)]:
                defauts = ' ; '.join(filter(None, (
                    r.get('prefixe'), r.get('fond'), r.get('cache'),
                    r.get('perso'))))
                rows.append(f'| {panel} | {r["el"]} | {r["kind"]} '
                            f'| {r["speaker"] or "—"} | {defauts} |')
        if rows:
            lines += rows + ['']
    lines.append('Détail chiffré dans `AUDIT-BULLES.json`.')
    (ROOT / 'Planches-dessin/validation/AUDIT-BULLES.md').write_text('\n'.join(lines))
    print(f'dialogues={n_dial} encadrés={n_enc} | préfixes faux={n_prefixe} '
          f'| fonds faux={n_fond} | peau={n_cache} (têtes={n_tete}) '
          f'| silhouettes={n_perso} | vignettes en défaut={len(vignettes)}/153')
    print('JSON :', out)
