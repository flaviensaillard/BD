"""Détourage d'un personnage généré sur fond uni (gris clair).

Combine la segmentation « personne » de MediaPipe (modèle embarqué) et un
affinage colorimétrique sur la bande de contour, le fond étant uniforme.
Retourne une image RGBA recadrée sur le sujet.
"""
import numpy as np, cv2
from PIL import Image

_seg = None
def _segmenter():
    global _seg
    if _seg is None:
        import mediapipe as mp
        _seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
    return _seg

def detourer(path, core_thr=0.7, band=4, feather=0.8, sigma_bg=50):
    im = Image.open(path).convert('RGB'); W, H = im.size
    rgb = np.asarray(im).astype(np.float32)
    # 1) segmentation personne (sur image réduite, puis remontée)
    small = cv2.resize(rgb.astype(np.uint8), (W // 2, H // 2))
    seg = _segmenter().process(small).segmentation_mask
    seg = cv2.resize(seg, (W, H), interpolation=cv2.INTER_LINEAR)
    # 2) fond estimé LOCALEMENT (convolution normalisée des pixels hors sujet) : gère dégradés et vignettage
    zone = cv2.dilate((seg > 0.08).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * band + 1, 2 * band + 1)))
    far = cv2.dilate(zone, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))).astype(np.float32)  # on exclut aussi les ombres proches
    wmask = 1.0 - far
    num = cv2.GaussianBlur(rgb * wmask[..., None], (0, 0), sigma_bg)
    den = cv2.GaussianBlur(wmask, (0, 0), sigma_bg)[..., None]
    glob = np.median(rgb[wmask > 0.5].reshape(-1, 3), axis=0)
    bg = np.where(den > 1e-3, num / np.maximum(den, 1e-3), glob)
    dist = np.abs(rgb - bg).sum(axis=2)
    # clé signée : plus clair que le fond (tissu blanc) -> seuil bas ; plus sombre (ombres au sol) -> seuil élevé
    bright = rgb.sum(axis=2) > bg.sum(axis=2)
    ys_seg = np.where((seg > 0.3).any(axis=1))[0]
    y_feet = ys_seg.max() if len(ys_seg) else H
    h_seg = y_feet - (ys_seg.min() if len(ys_seg) else 0)
    near_floor = (np.arange(H) > y_feet - 0.12 * h_seg)[:, None]      # zone des ombres au sol
    thr_dark = np.where(near_floor, 45.0, 22.0)
    inner = seg > 0.3                                                  # silhouette : seuil bas pour le tissu clair
    key_bright = np.where(inner, np.clip((dist - 18) / 32, 0, 1), np.clip((dist - 48) / 62, 0, 1))
    key = np.where(bright, key_bright, np.clip((dist - thr_dark) / (thr_dark + 40), 0, 1))
    segconf = np.clip((seg - 0.5) / 0.3, 0, 1)
    strong = (dist > 95).astype(np.uint8)                    # nettement différent du fond même si la segmentation l'a raté (bras levé)
    zone = np.maximum(zone, strong)
    # 3) cœur opaque = segmentation érodée ; intérieur = clé basse ou confiance seg ; extérieur = clé haute
    core = cv2.erode((seg > core_thr).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    alpha = np.where(core > 0, 1.0, np.where(zone > 0, np.maximum(key, segconf), 0.0)).astype(np.float32)
    # composantes : on garde la principale et les membres détachés (>= 2 % de la principale)
    hard = (alpha > 0.5).astype(np.uint8)
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(hard, 8)
    if n > 2:
        areas = stats[1:, cv2.CC_STAT_AREA]; main = areas.max()
        keep = np.zeros(n, bool); keep[1:] = areas >= 0.02 * main
        alpha = np.where(keep[lab] | (alpha <= 0.5), alpha, 0.0).astype(np.float32)
    # petits trous internes (< 0.4 % du sujet) : remplis (un corps n'est pas ajouré)
    holes = (alpha < 0.5).astype(np.uint8)
    n2, lab2, stats2, _ = cv2.connectedComponentsWithStats(holes, 4)
    subj = float((alpha >= 0.5).sum())
    for i in range(1, n2):
        x, y, w_, h_, a_ = stats2[i]
        touches = x == 0 or y == 0 or x + w_ >= W or y + h_ >= H
        if not touches and a_ < 0.004 * subj:
            alpha[lab2 == i] = 1.0
    if feather:
        alpha = cv2.GaussianBlur(alpha, (0, 0), feather)
    # 4) décontamination du fond sur les bords (évite le liseré gris)
    a = alpha[..., None]
    fg = np.clip((rgb - (1 - a) * bg) / np.maximum(a, 0.35), 0, 255)
    out = np.where(a > 0.98, rgb, fg).astype(np.uint8)
    rgba = np.dstack([out, (alpha * 255).astype(np.uint8)])
    ys, xs = np.where(alpha > 0.5)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    return Image.fromarray(rgba, 'RGBA').crop(box), box

if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        img, box = detourer(p)
        out = p.rsplit('.', 1)[0] + '-detoure.png'
        img.save(out); print(out, img.size, 'boîte', box)
