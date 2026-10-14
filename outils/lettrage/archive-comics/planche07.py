"""Lettrage déterministe de la planche 7. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[3]
S = 3
im = Image.open(ROOT/'planches/archive-comics/07-mur-vert-et-noir-dessin.png').convert('RGB').resize((1100*S,1569*S),Image.Resampling.LANCZOS)
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

# Case 1 : le mur de Montmélian avance, Lyssandro est surpris.
bubble((55,52,470,125),"On monte ensemble les Vert et Noir ! Personne ne passe !",tail=[(170,120),(200,120),(185,162)],maximum=17)
bubble((800,52,1045,140),"Oh là là, ils sont déjà sur nous !",tail=[(825,135),(855,135),(812,198)],maximum=17)
# Case 2 : en-avant de Milo, l’arbitre siffle, Léon râle.
bubble((55,408,320,490),"En-avant du RCM ! Ballon rendu à Montmélian !",tail=[(280,485),(310,485),(378,508)],maximum=16)
textfit('FIIIIT !',(330,412,465,447),24)
bubble((360,660,540,740),"Mais fais attention Milo !",tail=[(430,665),(460,665),(458,632)],maximum=16)
textfit('PLOP !',(215,565,330,600),24)
# Case 3 : Nolann met le pied en touche.
bubble((810,408,1050,490),"Touche ! Ballon rendu à Montmélian, joué comme une pénalité !",tail=[(930,485),(960,485),(958,522)],maximum=15)
textfit('FIIIIT !',(575,405,735,440),22)
bubble((575,448,800,520),"Mince, le terrain de 20 mètres est moins large que je croyais !",tail=[(675,515),(705,515),(692,552)],maximum=15)
# Case 4 : essai de Montmélian, Flavien alerte depuis la touche.
bubble((430,800,800,875),"La ligne défensive les garçons ! Si Léon monte tout seul, ça ouvre un boulevard !",tail=[(760,868),(790,868),(878,885)],maximum=16)
caption((55,1050,430,1098),'ESSAI DE MONTMÉLIAN ! +1 POINT !',16)
# Case 5 : hors-jeu de Léon, pénalité pour Montmélian.
bubble((150,1128,420,1205),"Hors-jeu du joueur du RCM ! Pénalité pour Montmélian !",tail=[(350,1200),(380,1200),(408,1252)],maximum=16)
textfit('FIIIIT !',(425,1135,545,1170),22)
# Case 6 : Julien et Kilian encouragent depuis la touche.
bubble((575,1128,810,1215),"Calmez-vous le RCM ! Respirez ! Regardez vos copains avant de courir !",tail=[(795,1208),(825,1208),(845,1255)],maximum=15)
bubble((820,1128,1050,1210),"Ils s’énervent au lieu de construire…",tail=[(945,1205),(975,1205),(960,1232)],maximum=15)

page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/archive-comics/07-mur-vert-et-noir.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche07.png')
print('OK')
