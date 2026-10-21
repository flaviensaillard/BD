"""Bibliothèque commune de lettrage des planches Marvel (étape finale, sans retouche du dessin).

Principes :
- on part des planches validées de Planches-dessin/ (dessin figé, seul lettrage ajouté) ;
- les bulles suivent l'ordre de lecture du scénario, jamais sur les visages ;
- chaque queue pointe vers le personnage qui parle (bouche/tête) ;
- police comics Kalam-Bold, traits noirs nets, encadrés narratifs jaunes.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTPATH = str(Path(__file__).with_name('Kalam-Bold.ttf'))
W_STD, H_STD = 864, 1222  # trame cible des planches finales


class Lettrage:
    """Superpose bulles, pensées, onomatopées et encadrés sur une planche donnée."""

    def __init__(self, src: str, dst: str, debug=False):
        self.src = ROOT / src
        self.dst = ROOT / dst
        im = Image.open(self.src).convert('RGB')
        # Mise au format trame standard 864x1222 (les rectangles du plan de lettrage
        # sont définis dans cette trame ; l'ajustement reste inférieur à 4 %).
        if im.size != (W_STD, H_STD):
            im = im.resize((W_STD, H_STD), Image.LANCZOS)
        self.S = 3
        self.im = im.resize((W_STD * self.S, H_STD * self.S), Image.LANCZOS)
        self.d = ImageDraw.Draw(self.im)
        self.debug = debug

    # --- primitives -------------------------------------------------------
    def box(self, b):
        return tuple(round(v * self.S) for v in b)

    def poly(self, points, fill='white', outline=None):
        pts = [(round(x * self.S), round(y * self.S)) for x, y in points]
        self.d.polygon(pts, fill=fill)
        if outline:
            self.d.line(pts + [pts[0]], fill=outline, width=2 * self.S)

    def textfit(self, text, rect, maximum=15, color='black', align='center'):
        """Insère le texte dans rect en réduisant la taille jusqu'à tenir."""
        x, y, r, b = self.box(rect)
        if self.debug:
            self.d.rectangle((x, y, r, b), outline=(255, 0, 255))
        for size in range(maximum * self.S, 8 * self.S - 1, -1):
            f = ImageFont.truetype(FONTPATH, size)
            lines, line = [], ''
            text_nbsp = (text.replace(' !', '\u00a0!').replace(' ?', '\u00a0?')
                         .replace(' :', '\u00a0:').replace(' ;', '\u00a0;'))
            for word in text_nbsp.split(' '):
                candidate = (line + ' ' + word).strip()
                if self.d.textlength(candidate, font=f) > r - x and line:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
            step = round(size * 1.18)
            if len(lines) * step <= b - y:
                break
        else:
            raise ValueError('Texte trop long : ' + text)
        top = y + (b - y - len(lines) * step) // 2
        for line in lines:
            if align == 'left':
                left = x
            else:
                left = x + (r - x - self.d.textlength(line, font=f)) / 2
            self.d.text((left, top), line, font=f, fill=color, anchor='lt')
            top += step
        return round(size / self.S, 1)

    # --- éléments de BD ---------------------------------------------------
    def bulle(self, rect, text, maximum=15, pad=10):
        """Boîte de dialogue blanche ; le locuteur est nommé dans le texte
        (« Léon: "…" ») — plus de queue pointée vers le personnage."""
        self.d.rounded_rectangle(self.box(rect), radius=16 * self.S, fill='white',
                                 outline='black', width=2 * self.S)
        x, y, r, b = rect
        return self.textfit(text, (x + pad, y + 6, r - pad, b - 6), maximum)

    def pensee(self, rect, text, maximum=14, pad=10):
        """Pensée : même boîte blanche que le dialogue, locuteur nommé dans le texte."""
        return self.bulle(rect, text, maximum=maximum, pad=pad)

    def onomatopee(self, center, text, size=20, color='black'):
        """Onomatopée libre (sifflet, impact) posée hors des visages."""
        f = ImageFont.truetype(FONTPATH, round(size * self.S))
        cx, cy = center[0] * self.S, center[1] * self.S
        self.d.text((cx, cy), text, font=f, fill=color, anchor='mm')

    def encadre(self, rect, text, maximum=12, fill='#f2e3b0', align='left', pad=8):
        """Encadré narratif : fond jaune/brun, contour brun (caption de récit)."""
        self.d.rectangle(self.box(rect), fill=fill, outline='#6b4f2a', width=2 * self.S)
        x, y, r, b = rect
        return self.textfit(text, (x + pad, y + 5, r - pad, b - 5), maximum, align=align)

    def cri(self, rect, text, fill='white', maximum=16):
        """Bulle cri (burst) : rectangle à coins irréguliers simulés par double contour."""
        x1, y1, x2, y2 = self.box(rect)
        self.d.polygon([(x1, y1 + 8 * self.S), (x1 + 18 * self.S, y1), (x2 - 14 * self.S, y1 + 6 * self.S),
                        (x2, y1 + 20 * self.S), (x2 - 10 * self.S, y2 - 6 * self.S), (x2 - 26 * self.S, y2),
                        (x1 + 12 * self.S, y2 - 8 * self.S), (x1, y2 - 22 * self.S)],
                       fill=fill, outline='black')
        self.d.polygon([(x1 + 5 * self.S, y1 + 11 * self.S), (x1 + 20 * self.S, y1 + 5 * self.S),
                        (x2 - 16 * self.S, y1 + 10 * self.S), (x2 - 5 * self.S, y1 + 21 * self.S),
                        (x2 - 13 * self.S, y2 - 9 * self.S), (x2 - 27 * self.S, y2 - 5 * self.S),
                        (x1 + 14 * self.S, y2 - 11 * self.S), (x1 + 5 * self.S, y2 - 20 * self.S)],
                       outline='black')
        rx1, ry1, rx2, ry2 = rect
        return self.textfit(text, (rx1 + 14, ry1 + 12, rx2 - 14, ry2 - 12), maximum)

    def voix_off(self, rect, text, maximum=13, align='center'):
        """Voix hors-champ : boîte blanche comme le dialogue, locuteur nommé."""
        return self.bulle(rect, text, maximum=maximum)

    def save(self):
        final = self.im.resize((W_STD, H_STD), Image.LANCZOS)
        self.dst.parent.mkdir(parents=True, exist_ok=True)
        final.save(self.dst, dpi=(300, 300))
        return self.dst
