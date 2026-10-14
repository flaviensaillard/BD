"""Lettrage déterministe de la planche 1. Dépendance : Pillow, NumPy, OpenCV headless.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[3]
S = 3
im = Image.open(ROOT/'planches/archive-comics/01-source.png').convert('RGB').resize((1024*S,1536*S),Image.Resampling.LANCZOS)
# Effacer uniquement quatre anciennes queues mal attribuées, par interpolation
# locale non générative ; visages et corps restent hors des masques.
import cv2
import numpy as np
pixels = np.array(im)
mask = np.zeros(pixels.shape[:2], dtype=np.uint8)
for points in [
    [(297,224),(318,222),(326,269),(309,253)],
    [(734,177),(749,178),(763,224),(748,214)],
    [(197,1034),(326,1034),(326,1075),(197,1075)],
    [(432,1028),(455,1030),(466,1069),(447,1056)],
]:
    cv2.fillPoly(mask,[np.array([(x*S,y*S) for x,y in points],dtype=np.int32)],255)
im=Image.fromarray(cv2.inpaint(pixels,mask,3*S,cv2.INPAINT_TELEA))
d = ImageDraw.Draw(im)
fontpath = str(Path(__file__).resolve().parents[1]/'Kalam-Bold.ttf')
def box(b): return tuple(round(v*S) for v in b)
def poly(points, fill='white', outline=None):
    d.polygon([(round(x*S),round(y*S)) for x,y in points],fill=fill)
    if outline: d.line([(round(x*S),round(y*S)) for x,y in points],fill=outline,width=2*S)
def textfit(text, rect, maximum=20, color='black', align='center'):
    x,y,r,b=box(rect)
    for size in range(maximum*S,11*S,-1):
        f=ImageFont.truetype(fontpath,size)
        lines=[]; line=''
        for word in text.replace(' !', '\u00a0!').replace(' ?', '\u00a0?').replace(' :', '\u00a0:').replace(' ;', '\u00a0;').split(' '):
            candidate=(line+' '+word).strip()
            if d.textlength(candidate,font=f)>r-x and line:
                lines.append(line);line=word
            else: line=candidate
        lines.append(line)
        step=round(size*1.22)
        if len(lines)*step<=b-y: break
    else: raise ValueError('Texte trop long : '+text)
    top=y+(b-y-len(lines)*step)//2
    for line in lines:
        left=x if align=='left' else x+(r-x-d.textlength(line,font=f))/2
        d.text((left,top),line,font=f,fill=color,anchor='lt')
        top+=step
    print(f'{size/S:.1f}px : {text}')
def bubble(rect,text,tail=None,maximum=20,pad=12):
    if tail: poly(tail,outline='black')
    d.rounded_rectangle(box(rect),radius=28*S,fill='white',outline='black',width=2*S)
    if tail:
        # Hide the balloon edge at the tail's base.
        poly([tail[0],tail[1],((tail[0][0]+tail[1][0])/2,(tail[0][1]+tail[1][1])/2+3)])
    x,y,r,b=rect
    textfit(text,(x+pad,y+9,r-pad,b-9),maximum)
def caption(rect,text,maximum=19):
    d.rectangle(box(rect),fill='#ffe38b',outline='black',width=2*S)
    x,y,r,b=rect;textfit(text,(x+9,y+6,r-9,b-6),maximum,align='left')
caption((42,45,320,134),'SAISON DERNIÈRE — CATÉGORIE U6. SEPT TOURNOIS DISPUTÉS. CINQ REMPORTÉS. DEUX FOIS DEUXIÈMES.',18)
bubble((226,117,394,233),'ON EST LES CHAMPIONS ! PERSONNE NE PEUT NOUS BATTRE !',tail=[(357,219),(378,218),(399,248)],maximum=19)
bubble((646,58,854,188),"Cinq coupes en une seule saison ! Même les grands du club n’en reviennent pas !",tail=[(735,179),(752,181),(726,231)],maximum=19)
# Case 2 : narration entière, puis réplique de Milo, avec queue dirigée vers lui.
caption((36,925,325,1077),"Je m’appelle Léon. J’ai 6 ans. Et avec mes copains du Rugby Club Motterain, on a vécu une saison magique.",17)
bubble((162,1330,325,1478),"Passe-moi la balle Lyssandro, j’ai mis mes chaussures fusées !",tail=[(251,1340),(274,1340),(279,1290)],maximum=18,pad=9)
# Case 3 : Lyssandro en haut, Ayden en bas ; aucune répétition.
bubble((350,921,570,1038),'Cinq fois premiers et deux fois deuxièmes… Vous vous rendez compte ?',tail=[(390,1026),(407,1026),(381,1064)],maximum=19)
bubble((478,1344,675,1469),"C’est sûr, l’année prochaine chez les U8, ce sera exactement pareil !",tail=[(498,1354),(520,1354),(466,1306)],maximum=19)
# Case 4 : réplique intégrale et formulation du scénario.
bubble((700,920,986,1090),'Pas « exactement pareil », Ayden… Ce sera encore MIEUX ! En U8, on ne finira même plus deuxièmes : on va TOUT gagner !',tail=[(780,1081),(804,1081),(813,1121)],maximum=20)
page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/archive-comics/01-la-legende-des-u6.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche01-corrigee.png')
