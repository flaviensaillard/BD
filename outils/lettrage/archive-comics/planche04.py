"""Lettrage déterministe de la planche 4. Dépendance : Pillow.
Ne régénère pas le dessin ; superpose des bulles et des textes contrôlés.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = Path(__file__).resolve().parents[3]
S = 3
im = Image.open(ROOT/'planches/archive-comics/planches-04-source.png').convert('RGB').resize((1055*S,1491*S),Image.Resampling.LANCZOS)
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
# Case 1 : bilan U6, puis avertissement de Kilian.
bubble((16,15,515,128),"La saison dernière en U6, sur 7 tournois, vous en avez gagné 5 et fini 2es sur les 2 autres. C’était génial… mais écoutez-moi bien : une saison comme celle-là, c’est EXCEPTIONNEL et ça arrive très rarement !",tail=[(128,120),(151,120),(150,148)],maximum=20)
bubble((17,361,516,486),"Si vous croyez que vous allez gagner sans effort cette année parce que vous avez gagné en U6, vous allez avoir une énorme surprise !",tail=[(382,370),(411,370),(392,311)],maximum=21)
# Case 2 : laisser visibles le visage de Julien et le schéma de terrain.
bubble((539,16,841,250),"En U8, voici vos nouvelles règles ! On joue à 5 contre 5 sur un terrain de 30 mètres par 20 mètres. Il n’y a pas de poteaux et pas de transformations : chaque essai marqué vaut 1 point !",tail=[(827,180),(831,201),(874,205)],maximum=21)
# Case 3 : les fautes expliquées par Kilian, question de Milo, réponse de Flavien.
bubble((16,745,515,858),"Deuxième grand changement : l’arbitre siffle TOUS les en-avant quand le ballon tombe vers le camp adverse, et tous les hors-jeu si vous êtes devant le copain qui a le ballon !",tail=[(107,752),(132,752),(117,675)],maximum=20)
bubble((196,867,514,925),'Tous les en-avant ?! Même les tout petits ?!',tail=[(290,872),(312,872),(302,861)],maximum=20)
bubble((246,933,514,978),'Même les tout petits, Milo !',tail=[(482,940),(502,940),(505,915)],maximum=20)
# Case 4 : touche puis contacts ; les visages et les mains restent dégagés.
bubble((540,775,1038,869),"Et quand un joueur sort en touche, le ballon est directement rendu à l’autre équipe et il est joué comme une pénalité !",tail=[(640,782),(665,782),(648,724)],maximum=20)
bubble((540,883,1038,975),"Enfin, pour les contacts : de septembre à fin novembre, c’est du touché à 2 mains simultanées ! Les vrais plaquages seront autorisés à partir du mois de décembre !",tail=[(983,890),(1004,890),(1014,874)],maximum=20)
# Case 5 : Ayden puis Lyssandro.
bubble((16,998,515,1088),'Faut faire super attention aux passes alors, sinon on rend tout le temps le ballon…',tail=[(91,1080),(111,1080),(99,1114)],maximum=21)
bubble((113,1366,514,1475),'Et en défense, si on est hors-jeu, on se fait punir direct !',tail=[(266,1374),(291,1374),(278,1315)],maximum=21)
# Case 6 : défi de Léon, sous le visage.
bubble((541,1350,1038,1477),'Pfff, vous inquiétez pas les gars ! Touché à deux mains ou nouvelles règles, personne ne court aussi vite que nous. On va quand même tout rafler !',tail=[(769,1358),(795,1358),(788,1330)],maximum=21)
page=Image.new('RGB',(2480,3508),'white')
art=ImageOps.contain(im,page.size,Image.Resampling.LANCZOS)
page.paste(art,((page.width-art.width)//2,(page.height-art.height)//2))
page.save(ROOT/'planches/archive-comics/04-nouvelles-regles.png',dpi=(300,300))
ImageOps.contain(page,(1000,1414)).save('/home/user/apercu-planche04.png')
