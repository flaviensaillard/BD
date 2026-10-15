"""Lettrage déterministe de la planche 6. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
Source déposée par l'auteur : planches/planches-06-source.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[2]
S = 3
im = Image.open(ROOT/'planches/planches-06-source.png').convert('RGB').resize((1100*S,1569*S),Image.Resampling.LANCZOS)
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

# Case 1 : arrivée au tournoi, Flavien rappelle les règles.
caption((12,12,425,85),'OCTOBRE 2026 — PREMIER TOURNOI U8 DE LA SAISON. TROIS MATCHS AU PROGRAMME DE LA POULE !',17)
bubble((440,12,865,100),"Allez le RCM ! On se souvient des règles : 5 contre 5, touché à deux mains, pas de hors-jeu et on fait vivre le ballon !",tail=[(820,93),(850,93),(915,138)],maximum=17)
# Case 2 : match 1 contre Chambéry (jaune et noir).
bubble((8,430,245,500),"Bien joué Ayden ! Tiens Nolann, fonce !",tail=[(80,495),(110,495),(95,535)],maximum=17)
bubble((255,430,532,500),"ESSAI ! UN POINT POUR LE RCM !",tail=[(285,495),(315,495),(232,572)],maximum=17)
caption((250,768,532,814),'MATCH 1 : RCM bat CHAMBÉRY (JAUNE ET NOIR) !',15)
# Case 3 : match 2 contre Albertville (rouge et blanc). Milo d’abord (bulle haute), puis Léon.
bubble((825,428,1090,490),"À toi Léon !",tail=[(880,485),(910,485),(892,522)],maximum=17)
bubble((565,448,800,508),"Personne ne me rattrapera ! ESSAI !",tail=[(695,503),(725,503),(732,548)],maximum=17)
caption((565,765,855,812),'MATCH 2 : RCM bat ALBERTVILLE (ROUGE ET BLANC) !',15)
# Case 4 : Léon fanfaronne (bulle haute), Ayden tempère.
bubble((255,840,660,922),"Deux matchs, deux victoires ! Qu’est-ce que je vous avais dit ?! C’est trop facile la catégorie U8, on est toujours invincibles !",tail=[(520,915),(550,915),(548,950)],maximum=17)
bubble((8,862,250,938),"Attends Léon, contre Albertville on a quand même eu chaud sur la fin…",tail=[(215,930),(240,930),(300,955)],maximum=17)
# Case 5 : Kilian d’abord (bulle haute), puis Julien, avant Montmélian (vert et noir).
bubble((765,1152,1092,1232),"Écoutez bien les garçons : le troisième match, c’est contre Montmélian. Ils ont gagné leurs deux matchs aussi.",tail=[(790,1225),(820,1225),(610,1255)],maximum=16)
bubble((8,1165,325,1255),"Ils montent très vite en défense et ils ne laissent aucun espace. Si vous jouez chacun pour vous, ça ne passera pas !",tail=[(255,1248),(285,1248),(278,1282)],maximum=16)

page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/06-deux-victoires.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche06.png')
print('OK')
