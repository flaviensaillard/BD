"""Lettrage déterministe de la planche 2. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[3]
S = 3
im = Image.open(ROOT/'planches/archive-comics/planches-02-source.png').convert('RGB').resize((1024*S,1536*S),Image.Resampling.LANCZOS)
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
caption((41,45,477,106),'SEPTEMBRE 2026. SAINT-SULPICE, SAVOIE. LE JOUR DE LA REPRISE EN CATÉGORIE U8.')
# Case 2 : couvrir les textes fautifs, garder les silhouettes et les visages.
bubble((43,576,297,674),'Vanessa ! Alice ! On file au stade avec Léon, on rentre pour le déjeuner !',maximum=19)
# Voix hors champ : contour rectangulaire conservant son origine extérieure.
d.rectangle(box((298,586,476,675)),fill='white',outline='black',width=2*S)
textfit('Bon entraînement les garçons ! Amuse-toi bien Léon !',(306,594,468,667),18)
bubble((234,691,461,810),"Merci Maman ! À tout à l’heure Alice ! Dépêche-toi Papa, on va arriver après les copains !",maximum=18)
# Case 3 : réplique de Léon et réponse du père, précédemment manquante ici.
bubble((522,588,748,751),"Papa, j’ai déjà fait le calcul dans ma tête ! Si on fait sept tournois cette année en U8, ça fera sept nouveaux trophées sur mon étagère !",maximum=18)
bubble((526,936,990,1031),'Sept sur sept ? Carrément ! Tu ne crois pas que tu vas un peu vite en besogne, champion ?',tail=[(897,938),(921,938),(943,912)],maximum=20)
# Case 4 : suppression du doublon et restauration des deux répliques du scénario.
# Nettoyer la queue d'origine, qui pointait à tort vers le conducteur.
poly([(265,1198),(284,1233),(254,1215)])
bubble((31,1063,298,1239),'Bah quoi ? En U6, presque personne ne nous arrêtait ! Et on a toujours la même bande : Lyssandro, Ayden, Nolann, Milo et moi !',maximum=18)
# La voix de Léon provient de la banquette arrière hors cadre.
poly([(41,1181),(41,1204),(31,1221)],outline='black')
# Recouvrir intégralement l'ancienne réponse, puis agrandir pour le texte complet.
d.rounded_rectangle(box((296,1241,501,1384)),radius=32*S,fill='white')
bubble((205,1241,501,1466),'Justement, Léon. En U8, les autres clubs aussi ont grandi. Et les règles changent beaucoup. Écoute bien ce qu’on va vous expliquer avec Julien et Kilian.',tail=[(207,1303),(207,1330),(190,1291)],maximum=19)
# Case 5 : narration et dialogue (non plus un encadré narratif pour Léon).
caption((533,1068,750,1158),'LA MOTTE-SERVOLEX — STADE DU RUGBY CLUB MOTTERAIN.',18)
d.rectangle(box((530,1442,800,1523)),fill='white')
bubble((532,1437,990,1519),'Regarde Papa ! Il y a déjà la voiture de Julien ! Lyssandro est arrivé !',tail=[(707,1440),(735,1440),(737,1288)],maximum=20)
page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/archive-comics/02-matin-de-rentree.png',dpi=(300,300))
# Aperçu de contrôle, hors livrables versionnés.
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche02.png')
