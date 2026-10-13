"""Lettrage déterministe de la planche 5. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[2]
S = 3
im = Image.open(ROOT/'planches/05-premiers-sifflets-dessin.png').convert('RGB').resize((1100*S,1569*S),Image.Resampling.LANCZOS)
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
# Case 1 : en-avant de Milo, Julien siffle.
bubble((17,17,531,137),"En-avant ! Ballon rendu à l’autre équipe ! On garde les mains bien ouvertes en W devant la poitrine, Milo !",tail=[(478,130),(501,130),(494,174)],maximum=22)
textfit('FIIIIT !',(330,146,454,181),27)
# Case 2 : hors-jeu signalé par Kilian, réponse de Léon.
bubble((568,17,1082,130),"Hors-jeu Léon ! Tu étais devant tes copains au départ de l’action !",tail=[(1000,124),(1026,124),(1015,164)],maximum=22)
bubble((568,144,941,229),"Mais Coach, j’allais l’attraper ! Ça arrête pas de siffler en U8 !",tail=[(696,222),(720,222),(710,250)],maximum=22)
textfit('FIIIIT !',(857,421,970,453),26)
# Case 3 : passage au local des éducateurs et bilan de Kilian.
caption((17,539,649,586),'PLUS TARD, DANS LE VESTIAIRE DES COACHS…',22)
bubble((315,899,1081,1023),"Bon, avec nos 20 joueurs, nos 4 équipes de 5 prennent forme pour le premier tournoi d’octobre. Sur le papier, l’équipe de Léon, Lyssandro, Ayden, Nolann et Milo a du feu dans les jambes.",tail=[(460,906),(486,906),(450,791)],maximum=22)
# Case 4 : Julien pensif, puis Kilian.
bubble((17,1353,534,1450),"Du feu dans les jambes, oui… mais tu as vu leur réaction à chaque coup de sifflet ? Ils ont encore la tête en U6 où il suffisait de courir tout droit pour marquer.",tail=[(126,1361),(150,1361),(178,1325)],maximum=21)
bubble((17,1462,535,1551),"C’est vrai qu’au niveau des passes sous pression et de la défense en ligne, il y a encore tout à construire.",tail=[(475,1470),(499,1470),(512,1455)],maximum=21)
# Case 5 : inquiétude de Flavien et soutien de Julien.
bubble((568,1051,905,1151),"C’est surtout pour Léon que je m’inquiète. Il a un tel esprit de gagnant qu’il ne conçoit même pas qu’on puisse perdre un match.",tail=[(797,1144),(820,1144),(806,1170)],maximum=21)
textfit('LÉON',(590,1201,683,1236),23)
bubble((653,1435,1081,1550),"Le premier tournoi va être un sacré révélateur, Flavien. On sera là pour les accompagner.",tail=[(984,1444),(1010,1444),(1002,1383)],maximum=22)
page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/05-premiers-sifflets.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche05.png')
