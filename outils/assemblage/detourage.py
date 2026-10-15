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

def detourer(path, t0=38, t1=110, core_thr=0.7, band=4, feather=0.8, sigma_bg=50):
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
    key = np.clip((dist - t0) / (t1 - t0), 0, 1)
    # 3) cœur opaque = segmentation érodée ; bande de contour = clé couleur ; extérieur = 0
    core = cv2.erode((seg > core_thr).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    segconf = np.clip((seg - 0.5) / 0.3, 0, 1)  # confiance de la segmentation (comble les zones claires type manches blanches)
    alpha = np.where(core > 0, 1.0, np.where(zone > 0, np.maximum(key, segconf), 0.0)).astype(np.float32)
    # suppression des petites îles isolées
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0.5).astype(np.uint8), 8)
    if n > 2:
        keep = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        alpha = np.where((lab == keep) | (alpha <= 0.5), alpha, 0.0).astype(np.float32)
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
