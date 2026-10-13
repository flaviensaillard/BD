"""Lettrage déterministe de la planche 3. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[2]
S = 3
im = Image.open(ROOT/'planches/03-les-20-guerriers-dessin.png').convert('RGB').resize((1024*S,1536*S),Image.Resampling.LANCZOS)
d = ImageDraw.Draw(im)
fontpath = str(Path(__file__).with_name('Kalam-Bold.ttf'))
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
# Le dessin sélectionné comporte une case de transition supplémentaire.
# Les dialogues du scénario sont répartis sans ajout ni répétition.
caption((55,36,736,116),'NOUVELLE SAISON, NOUVELLE CATÉGORIE : VINGT JOUEURS COMPOSENT LE GROUPE U8 DU RCM !',21)
bubble((47,491,278,570),'Salut les gars ! Alors, prêts pour notre nouvelle saison de champions ?',tail=[(156,560),(175,560),(157,589)],maximum=18)
bubble((290,492,517,580),'Ouais ! Avec Léon, on en a parlé toute la semaine à l’école !',tail=[(345,573),(361,573),(363,602)],maximum=18)
bubble((52,748,515,861),"Trop content de vous retrouver ! Mon père m’a dit qu’on est vingt joueurs cette année, ça va faire quatre équipes de cinq !",tail=[(141,752),(162,752),(156,715)],maximum=20)
bubble((546,491,975,574),"Regardez le maillot Rouge, Bleu et Blanc ! En U8, on dirait carrément l’équipe première !",tail=[(586,567),(609,567),(603,603)],maximum=20)
# Julien : onomatopée puis rassemblement.
textfit('FIIIIIIIIT !',(52,943,185,981),25)
bubble((49,1090,579,1188),"Rassemblement les U8 ! Tout le monde s’assoit en demi-cercle devant nous, et on pose les ballons !",tail=[(358,1095),(385,1095),(363,1038)],maximum=21)
bubble((611,894,975,1012),'Et regardez mes appuis : zip, zap, essai ! Qui m’attrape ?!',tail=[(705,1003),(727,1003),(718,1054)],maximum=21)
bubble((50,1221,801,1313),"Bienvenue en U8 les garçons ! Avant de commencer l’entraînement, on doit vous parler franchement de ce qui s’est passé la saison dernière…",tail=[(774,1266),(790,1287),(837,1300)],maximum=21)
bubble((308,1431,792,1507),'Tu vas voir, ils vont nous féliciter pour nos cinq trophées !',tail=[(316,1444),(329,1435),(300,1419)],maximum=21)
textfit('3',(490,1516,534,1534),17)
page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/03-les-20-guerriers-du-rcm.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche03.png')
