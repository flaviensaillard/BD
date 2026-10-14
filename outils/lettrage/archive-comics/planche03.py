"""Lettrage déterministe de la planche 3. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[3]
S = 3
im = Image.open(ROOT/'planches/archive-comics/03-les-20-guerriers-dessin.png').convert('RGB').resize((1054*S,1492*S),Image.Resampling.LANCZOS)
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
caption((17,12,739,70),'NOUVELLE SAISON, NOUVELLE CATÉGORIE : VINGT JOUEURS COMPOSENT LE GROUPE U8 DU RCM !',21)
# Retrouvailles : Léon au centre, Lyssandro à sa gauche, Ayden à sa droite.
bubble((16,612,296,690),'Salut les gars ! Alors, prêts pour notre nouvelle saison de champions ?',tail=[(260,616),(281,616),(299,588)],maximum=19)
bubble((303,613,584,690),'Ouais ! Avec Léon, on en a parlé toute la semaine à l’école !',tail=[(403,618),(425,618),(419,593)],maximum=19)
bubble((16,698,584,760),"Trop content de vous retrouver ! Mon père m’a dit qu’on est vingt joueurs cette année, ça va faire quatre équipes de cinq !",tail=[(168,703),(187,703),(181,692)],maximum=19)
# Nolann et Milo : une réplique par joueur.
bubble((608,622,1038,692),"Regardez le maillot Rouge, Bleu et Blanc ! En U8, on dirait carrément l’équipe première !",tail=[(706,627),(728,627),(715,595)],maximum=20)
bubble((609,702,1038,759),'Et regardez mes appuis : zip, zap, essai ! Qui m’attrape ?!',tail=[(957,707),(979,707),(983,696)],maximum=20)
# Julien siffle et rassemble le groupe.
textfit('FIIIIIIIIT !',(328,787,455,829),25)
bubble((227,977,818,1070),"Rassemblement les U8 ! Tout le monde s’assoit en demi-cercle devant nous, et on pose les ballons !",tail=[(528,983),(554,983),(538,944)],maximum=21)
# Kilian accueille le groupe ; Léon chuchote à Lyssandro.
bubble((17,1096,790,1189),"Bienvenue en U8 les garçons ! Avant de commencer l’entraînement, on doit vous parler franchement de ce qui s’est passé la saison dernière…",tail=[(775,1155),(782,1177),(827,1176)],maximum=21)
bubble((189,1399,744,1477),'Tu vas voir, ils vont nous féliciter pour nos cinq trophées !',tail=[(228,1406),(251,1406),(248,1340)],maximum=21)
page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/archive-comics/03-les-20-guerriers-du-rcm.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche03.png')
