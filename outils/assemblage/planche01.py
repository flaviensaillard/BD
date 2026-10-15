"""Assemblage de la planche 1 — « La Légende des U6 » (dessin sans texte, A4 2480x3508 à 300 dpi).

Structure validée : 1 grande case (moitié haute) + 3 cases en bas (action / médailles / gros plan Léon).
Case 1 : décor ensoleillé + 8 personnages détourés placés par calcul (perspective simple).
Case 2 : extrait du même décor (flou de profondeur) + Lyssandro, Ayden et Milo en course.
Case 3 : médailles (image générée, recadrée sous les mentons).
Case 4 : gros plan de Léon (image générée, recadrée).
"""
import sys, random
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
from detourage import detourer

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'planches/travail'
P1, COUV = WORK / 'planche01', WORK / 'couverture'
W, H = 2480, 3508
MARGE, GOUT, BORD = 60, 40, 6

# Cases (x0, y0, x1, y1)
C1 = (MARGE, MARGE, W - MARGE, 2200)
Y2 = C1[3] + GOUT
C2 = (MARGE, Y2, MARGE + 700, H - MARGE)
C3 = (C2[2] + GOUT, Y2, C2[2] + GOUT + 1000, H - MARGE)
C4 = (C3[2] + GOUT, Y2, W - MARGE, H - MARGE)
MEDAILLES_Y0 = 100   # ligne de départ du recadrage de la case 3 (ajustée après contrôle visuel)

_fd = None
def face_box(img_rgba):
    """Boîte du visage (x, y, w, h) via MediaPipe, sur fond gris reconstitué."""
    global _fd
    import mediapipe as mp
    if _fd is None:
        _fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.3)
    bg = Image.new('RGBA', img_rgba.size, (200, 200, 200, 255)); bg.alpha_composite(img_rgba)
    arr = np.asarray(bg.convert('RGB'))
    r = _fd.process(arr)
    if not r.detections:
        return None
    bb = max(r.detections, key=lambda d: d.score[0]).location_data.relative_bounding_box
    w, h = img_rgba.size
    return bb.xmin * w, bb.ymin * h, bb.width * w, bb.height * h

def hauteur_corps(cut):
    """Hauteur en px du corps (sommet du crâne -> pieds), indépendante des bras levés."""
    fb = face_box(cut)
    if fb is None:
        return cut.height
    x, y, w, h = fb
    return cut.height - max(0.0, y - 0.35 * h)

def ensoleiller(rgba, chaleur=1.0):
    """Réchauffe et contraste légèrement les personnages (lumière de printemps), léger flou pour accorder la netteté."""
    arr = np.asarray(rgba).astype(np.float32)
    rgb = arr[..., :3]
    rgb = (rgb - 128) * 1.06 + 128
    rgb[..., 0] += 6 * chaleur; rgb[..., 1] += 2 * chaleur; rgb[..., 2] -= 6 * chaleur
    arr[..., :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(0.8))

def ombre(canvas, cx, feet_y, width, strength=0.38, dx=-0.25):
    """Ombre de contact + ombre portée douce vers la gauche (soleil haut à droite)."""
    ow, oh = int(width * 1.1), int(width * 0.18)
    pad = int(ow * 0.6)
    cv = np.zeros((oh + 2 * pad, ow + 2 * pad), np.uint8)
    cv2.ellipse(cv, (pad + ow // 2, pad + oh // 2), (ow // 2, oh // 2), 0, 0, 360, 255, -1)
    cv2.ellipse(cv, (pad + ow // 2 + int(dx * ow), pad + oh // 2), (int(ow * 0.45), int(oh * 0.7)), 0, 0, 360, 200, -1)
    cv = cv2.GaussianBlur(cv, (0, 0), ow * 0.06)
    layer = Image.fromarray(cv).point(lambda v: int(v * strength))
    shadow = Image.new('RGBA', layer.size, (15, 35, 10, 0)); shadow.putalpha(layer)
    canvas.alpha_composite(shadow, (int(cx - layer.width / 2), int(feet_y - layer.height / 2 - oh * 0.1)))

def placer(canvas, cut, taille_m, cx, feet_y, y_h, cam_h, chaleur=1.0):
    scale = (feet_y - y_h) / cam_h
    fb = face_box(cut)
    k = taille_m * scale / hauteur_corps(cut)
    cut = cut.resize((max(1, round(cut.width * k)), max(1, round(cut.height * k))), Image.Resampling.LANCZOS)
    cut = ensoleiller(cut, chaleur)
    ombre(canvas, cx, feet_y, cut.width)
    x0, y0 = int(cx - cut.width / 2), int(feet_y - cut.height)
    canvas.alpha_composite(cut, (x0, y0))
    if fb is not None:
        fx, fy, fw, fh = [v * k for v in fb]
        VISAGES.append((x0 + fx - 0.4 * fw, y0 + fy - 0.6 * fh, x0 + fx + 1.4 * fw, y0 + fy + 1.5 * fh))

def nettoyer_ciel(im, frac=0.40):
    """Retire les petits confettis sombres générés dans le ciel (taches noires), sans toucher aux mâts."""
    arr = np.asarray(im.convert('RGB')).copy()
    h, w = arr.shape[:2]
    L = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    med = cv2.medianBlur(L, 41)
    mask = ((med.astype(int) - L.astype(int)) > 35).astype(np.uint8)
    mask[int(h * frac):] = 0
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    keep = np.zeros(n, bool)
    for i in range(1, n):
        x, y, bw, bh, a = stats[i]
        keep[i] = a < 220 and bw < 28 and bh < 28       # petits blobs seulement
    mask = keep[lab].astype(np.uint8)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    out = cv2.inpaint(arr, mask, 4, cv2.INPAINT_TELEA)
    return Image.fromarray(out)

VISAGES = []   # boîtes (x0, y0, x1, y1) des visages placés, pour y éviter les confettis

def confettis(size, n, seed=1, taille=(6, 26), alpha=(120, 230), eviter=()):
    random.seed(seed)
    layer = Image.new('RGBA', size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    cols = [(255, 215, 0), (255, 190, 30), (255, 230, 90), (240, 170, 20), (255, 245, 160)]
    for _ in range(n):
        x, y = random.randrange(size[0]), random.randrange(size[1])
        if any(bx0 <= x <= bx1 and by0 <= y <= by1 for bx0, by0, bx1, by1 in eviter):
            continue
        t = random.randint(*taille); c = random.choice(cols) + (random.randint(*alpha),)
        ang = random.uniform(0, 3.14)
        pts = [(x + t * np.cos(ang + a), y + t * 0.45 * np.sin(ang + a)) for a in (0, 1.1, 3.14, 4.2)]
        d.polygon(pts, fill=c)
    return layer.filter(ImageFilter.GaussianBlur(0.7))

def recadrer_ratio(im, ratio, ancre=0.5, y0=0):
    """Recadre im (à partir de la ligne y0) au ratio largeur/hauteur demandé, ancre horizontale 0..1."""
    w, h = im.size; h = h - y0
    if w / h > ratio:
        nw = round(h * ratio); x0 = round((w - nw) * ancre)
        return im.crop((x0, y0, x0 + nw, y0 + h))
    nh = round(w / ratio)
    return im.crop((0, y0, w, y0 + nh))

def taille(c): return (c[2] - c[0], c[3] - c[1])

def case1():
    tw, th = taille(C1)
    fond = nettoyer_ciel(Image.open(P1 / 'fond-case1.png').convert('RGB'))
    fond = recadrer_ratio(fond, tw / th).resize((tw, th), Image.Resampling.LANCZOS).convert('RGBA')
    VISAGES.clear()
    y_h, cam_h = 0.552 * th, 1.0
    # arrière : confettis lointains (petits, derrière les personnages)
    fond.alpha_composite(confettis((tw, th), 220, seed=3, taille=(4, 12), alpha=(90, 170)))
    persos = [  # fichier, taille réelle, x (fraction), pieds (fraction)
        (COUV / 'perso-julien.png',        1.82, 0.425, 0.800),   # dans l'intervalle Ayden/Léon : visage à gauche du trophée
        (COUV / 'perso-flavien.png',       1.80, 0.270, 0.815),
        (COUV / 'perso-kilian.png',        1.78, 0.730, 0.815),
        (COUV / 'perso-lyssandro.png',     1.24, 0.215, 0.930),
        (COUV / 'perso-milo.png',          1.22, 0.785, 0.930),
        (COUV / 'perso-ayden.png',         1.20, 0.350, 0.935),
        (P1 / 'perso-nolann-joie.png',     1.22, 0.650, 0.935),
        (P1 / 'perso-leon-trophee.png',    1.18, 0.500, 0.972),
    ]
    for f, t, fx, fy in persos:
        cut, _ = detourer(str(f))
        placer(fond, cut, t, fx * tw, fy * th, y_h, cam_h)
    # avant : quelques gros confettis flous devant
    fond.alpha_composite(confettis((tw, th), 70, seed=7, taille=(14, 30), alpha=(110, 200), eviter=list(VISAGES)).filter(ImageFilter.GaussianBlur(2.5)))
    return fond.convert('RGB')

def case2():
    tw, th = taille(C2)
    fond = nettoyer_ciel(Image.open(P1 / 'fond-case1.png').convert('RGB'))
    haut = 0.22                                           # on coupe le haut du ciel : horizon plus bas, enfants plus grands
    fond = fond.crop((0, round(fond.height * haut), fond.width, fond.height))
    fond = recadrer_ratio(fond, tw / th, ancre=0.15).resize((tw, th), Image.Resampling.LANCZOS)
    fond = fond.filter(ImageFilter.GaussianBlur(4)).convert('RGBA')   # profondeur de champ (photo de sport)
    y_h, cam_h = (0.552 - haut) / (1 - haut) * th, 1.0
    persos = [
        (P1 / 'perso-milo-course.png',      1.22, 0.78, 0.80),
        (P1 / 'perso-ayden-course.png',     1.20, 0.22, 0.86),
        (P1 / 'perso-lyssandro-course.png', 1.24, 0.50, 0.975),
    ]
    for f, t, fx, fy in persos:
        cut, _ = detourer(str(f))
        placer(fond, cut, t, fx * tw, fy * th, y_h, cam_h)
    return fond.convert('RGB')

def case3():
    tw, th = taille(C3)
    src = P1 / 'case3-medailles-v2.png'
    im = Image.open(src if src.exists() else P1 / 'case3-medailles.png').convert('RGB')
    im = recadrer_ratio(im, tw / th, ancre=0.5, y0=MEDAILLES_Y0)
    return im.resize((tw, th), Image.Resampling.LANCZOS)

def case4():
    tw, th = taille(C4)
    im = Image.open(P1 / 'case4-leon-regard.png').convert('RGB')
    return recadrer_ratio(im, tw / th, ancre=0.5).resize((tw, th), Image.Resampling.LANCZOS)

def main(out=ROOT / 'planches/01-la-legende-des-u6-dessin.png'):
    page = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(page)
    for c, f in ((C1, case1), (C2, case2), (C3, case3), (C4, case4)):
        page.paste(f(), (c[0], c[1]))
        d.rectangle(c, outline='black', width=BORD)
    page.save(out, dpi=(300, 300))
    page.resize((W // 3, H // 3), Image.Resampling.LANCZOS).save(str(out).replace('.png', '-apercu.jpg'), quality=88)
    print('écrit', out, page.size)

if __name__ == '__main__':
    main()
