"""Assemblage de la couverture réaliste (A4 2480x3508 à 300 dpi).

Décor généré + 8 personnages générés individuellement, détourés et placés
par calcul (perspective simple : caméra à hauteur CAM_H, horizon Y_H).
Taille à l'image d'une personne = (pieds_y - horizon) * taille_réelle / CAM_H.
"""
import sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
from detourage import detourer

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'planches/travail/couverture'
W, H = 2480, 3508
Y_H = 0.578 * H          # ligne d'horizon (clôture / début de pelouse) dans le décor
CAM_H = 1.10             # hauteur de la caméra (m)

# nom, fichier, taille réelle (m), x centre (fraction de W), pieds y (fraction de H)
VARIANTES = {
    # A : deux rangées classiques (coachs derrière, garçons devant, Léon un pas en avant)
    'A': [
        ('Julien',    'perso-julien.png',    1.82, 0.500, 0.815),
        ('Flavien',   'perso-flavien.png',   1.80, 0.330, 0.830),
        ('Kilian',    'perso-kilian.png',    1.78, 0.670, 0.830),
        ('Lyssandro', 'perso-lyssandro.png', 1.24, 0.200, 0.905),
        ('Milo',      'perso-milo.png',      1.22, 0.800, 0.905),
        ('Ayden',     'perso-ayden.png',     1.20, 0.350, 0.905),
        ('Nolann',    'perso-nolann.png',    1.22, 0.650, 0.905),
        ('Léon',      'perso-leon-v2.png',   1.18, 0.500, 0.935),
    ],
    # B : formation en V, Léon en pointe, profondeur croissante vers les coachs
    'B': [
        ('Julien',    'perso-julien.png',    1.82, 0.500, 0.800),
        ('Flavien',   'perso-flavien.png',   1.80, 0.345, 0.812),
        ('Kilian',    'perso-kilian.png',    1.78, 0.655, 0.812),
        ('Lyssandro', 'perso-lyssandro.png', 1.24, 0.215, 0.870),
        ('Milo',      'perso-milo.png',      1.22, 0.785, 0.870),
        ('Ayden',     'perso-ayden.png',     1.20, 0.355, 0.905),
        ('Nolann',    'perso-nolann.png',    1.22, 0.645, 0.905),
        ('Léon',      'perso-leon-v2.png',   1.18, 0.500, 0.950),
    ],
}

def fond():
    im = Image.open(WORK / 'fond-jour.png').convert('RGB')
    w, h = im.size
    tw = round(h * W / H)                      # recadrage au ratio A4 (on perd un peu sur les côtés)
    x0 = (w - tw) // 2
    return im.crop((x0, 0, x0 + tw, h)).resize((W, H), Image.Resampling.LANCZOS)

def harmoniser(rgba):
    """Légère harmonisation : noirs relevés et saturation réduite pour coller à la lumière douce du décor."""
    arr = np.asarray(rgba).astype(np.float32)
    rgb = arr[..., :3] * 0.94 + 8
    gray = rgb.mean(axis=2, keepdims=True)
    rgb = gray + (rgb - gray) * 0.93
    arr[..., :3] = np.clip(rgb, 0, 255)
    out = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    return out.filter(ImageFilter.GaussianBlur(0.9))

def ombre(canvas, cx, feet_y, width, strength=0.32):
    """Ombre de contact douce (ellipse floutée) sous les pieds."""
    ow, oh = int(width * 1.05), int(width * 0.16)
    pad = int(ow * 0.5)
    layer = Image.new('L', (ow + 2 * pad, oh + 2 * pad), 0)
    cv = np.zeros((oh + 2 * pad, ow + 2 * pad), np.uint8)
    cv2.ellipse(cv, (pad + ow // 2, pad + oh // 2), (ow // 2, oh // 2), 0, 0, 360, 255, -1)
    cv = cv2.GaussianBlur(cv, (0, 0), ow * 0.07)
    layer = Image.fromarray(cv)
    shadow = Image.new('RGBA', layer.size, (20, 30, 15, 0))
    shadow.putalpha(layer.point(lambda v: int(v * strength)))
    canvas.alpha_composite(shadow, (int(cx - layer.width / 2), int(feet_y - layer.height / 2 - oh * 0.1)))

def main(variante='A', out=None):
    out = out or ROOT / f'planches/00-couverture-dessin-{variante}.png'
    canvas = fond().convert('RGBA')
    rapport = []
    for nom, fichier, taille, fx, fy in VARIANTES[variante]:
        cut, _ = detourer(str(WORK / fichier))
        feet_y = fy * H
        scale_px_m = (feet_y - Y_H) / CAM_H
        target_h = taille * scale_px_m
        k = target_h / cut.height
        cut = harmoniser(cut.resize((round(cut.width * k), round(cut.height * k)), Image.Resampling.LANCZOS))
        cx = fx * W
        x0 = int(cx - cut.width / 2); y0 = int(feet_y - cut.height)
        ombre(canvas, cx, feet_y, cut.width)
        canvas.alpha_composite(cut, (x0, y0))
        rapport.append(f'{nom:10s} taille {taille:.2f} m -> {cut.height:4d} px, tête y={y0} ({y0/H:.0%}), x={x0}..{x0+cut.width}')
    final = canvas.convert('RGB')
    final.save(out, dpi=(300, 300))
    final.resize((W // 3, H // 3), Image.Resampling.LANCZOS).save(str(out).replace('.png', '-apercu.jpg'), quality=88)
    print('\n'.join(rapport)); print('écrit', out, final.size)

if __name__ == '__main__':
    for v in (sys.argv[1:] or ['A', 'B']):
        main(v)
