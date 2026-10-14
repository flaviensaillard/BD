"""Lettrage déterministe de la planche 8. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[3]
S = 3
im = Image.open(ROOT/'planches/archive-comics/08-action-individuelle-dessin.png').convert('RGB').resize((1100*S,1569*S),Image.Resampling.LANCZOS)
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
def thought(rect,text,maximum=20,pad=12):
    """Bulle de pensée : rectangle arrondi + petites bulles vers le personnage."""
    d.rounded_rectangle(box(rect),radius=28*S,fill='white',outline='black',width=2*S)
    for (cx,cy,r) in [(345,692,9),(368,713,6),(390,733,4)]:
        d.ellipse(box((cx-r,cy-r,cx+r,cy+r)),fill='white',outline='black',width=2*S)
    x,y,r,b=rect
    textfit(text,(x+pad,y+9,r-pad,b-9),maximum)
def caption(rect,text,maximum=19):
    d.rectangle(box(rect),fill='#ffe38b',outline='black',width=2*S)
    x,y,r,b=rect;textfit(text,(x+9,y+6,r-9,b-6),maximum,align='left')

# Case 1 : Ayden transmet à Léon.
bubble((315,16,655,82),"Vas-y Léon ! On monte avec toi !",tail=[(345,76),(375,76),(225,105)],maximum=17)
# Case 2 : Lyssandro et Nolann appellent le ballon.
bubble((35,295,370,355),"Léon ! Passe à gauche, on est deux contre un !",tail=[(170,350),(200,350),(195,385)],maximum=16)
bubble((700,295,1065,360),"Ici Léon ! Je suis tout seul sur l’aile !",tail=[(785,355),(815,355),(805,390)],maximum=16)
# Case 3 : gros plan, pensée de Léon.
thought((30,588,360,675),"Non ! C’est moi qui vais sauver l’équipe ! Je vais passer au milieu tout seul comme en U6 !",maximum=15)
# Case 4 : touché à deux mains et en-avant, fin du match.
textfit('TCHAC !',(300,855,480,892),24)
textfit('FIIIIIIIT !',(860,855,1060,892),24)
bubble((560,855,850,935),"Touché à deux mains… et en-avant ! C’est terminé, fin du match !",tail=[(825,928),(855,928),(882,982)],maximum=15)
# Case 5 : le rêve d’invincibilité s’envole.
caption((35,1203,645,1285),'PREMIER TOURNOI U8 : 2 VICTOIRES, 1 DÉFAITE. LE RÊVE D’INVINCIBILITÉ VIENT DE VOLER EN ÉCLATS.',15)

page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/archive-comics/08-action-individuelle.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche08.png')
print('OK')
