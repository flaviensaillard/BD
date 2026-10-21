"""Génération du lettrage final des 30 planches vers Planches-dessin/Avec-texte/.

Étape « bulles et textes » : le dessin n'est plus modifié, on superpose uniquement
bulles, pensées, onomatopées et encadrés narratifs du scénario complet.
Contraintes : textes dans l'ordre de lecture, jamais sur les visages.
Plus de queue pointée : chaque dialogue est préfixé du locuteur
(Léon: "…") sur fond blanc ; la narration reste sur fond jaune/brun.

Usage : PYTHONPATH=.arena/vendor python outils/lettrage/generer_avec_texte.py [--check]
  --check : contrôle que les bulles ne recouvrent pas de zones de peau (visages).
"""
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from bd_common import Lettrage, ROOT  # noqa: E402
import personnages as PS  # noqa: E402

SRC = {
    1: 'Planches-dessin/01-la-legende-des-u6-marvel.png',
    2: 'Planches-dessin/02-matin-de-rentree-marvel.png',
    3: 'Planches-dessin/03-les-20-guerriers-du-rcm-marvel.png',
    4: 'Planches-dessin/04-nouvelles-regles-marvel.png',
    5: 'Planches-dessin/05-premiers-sifflets-marvel.png',
    6: 'Planches-dessin/06-deux-victoires-marvel.png',
    7: 'Planches-dessin/07-mur-vert-et-noir-marvel.png',
    8: 'Planches-dessin/08-action-individuelle-marvel.png',
    9: 'Planches-dessin/09-colere-et-larmes-marvel.png',
    10: 'Planches-dessin/10-ruminations-marvel.png',
    11: 'Planches-dessin/11-diagnostic-sous-la-pluie-marvel.png',
    12: 'Planches-dessin/12-travail-dans-la-boue-marvel.png',
    13: 'Planches-dessin/13-hauts-et-bas-de-novembre-marvel.png',
    14: 'Planches-dessin/14-les-mots-de-trop-marvel.png',
    15: 'Planches-dessin/15-la-lecon-d-un-pere-marvel.png',
    16: 'Planches-dessin/16-le-pardon-des-copains-marvel.png',
    17: 'Planches-dessin/17-decembre-sous-la-neige-marvel.png',
    18: 'Planches-dessin/18-ecole-du-plaquage-dans-le-froid-marvel.png',
    19: 'Planches-dessin/19-les-joueurs-analysent-les-coachs-preparent-marvel.png',
    20: 'Planches-dessin/20-le-test-du-grand-froid-le-mole-et-thonon-marvel.png',
    21: 'Planches-dessin/21-la-plus-belle-des-victoires-de-leon-marvel.png',
    22: 'Planches-dessin/22-le-soleil-de-mars-sur-la-motte-servolex-marvel.png',
    23: 'Planches-dessin/23-les-trois-piliers-du-jeu-marvel.png',
    24: 'Planches-dessin/24-veille-de-grand-tournoi-a-l-ecole-et-a-saint-sulpice-marvel.png',
    25: 'Planches-dessin/25-le-grand-tournoi-final-marvel.png',
    26: 'Planches-dessin/26-l-echec-qui-fait-grandir-marvel.png',
    27: 'Planches-dessin/27-la-correction-appliquee-l-heure-de-la-revanche-marvel.png',
    28: 'Planches-dessin/28-le-choc-des-titans-rcm-vs-montmelian-marvel.png',
    29: 'Planches-dessin/29-la-passe-de-la-victoire-marvel.png',
    30: 'Planches-dessin/30-on-apprend-de-ses-echecs-marvel.png',
}

# Éléments par page, dans l'ordre de lecture du scénario.
# Formats : ('encadre', rect, txt[, max]) ; ('bulle', rect, txt, queue[, max]) ;
# ('pensee', rect, txt, bulles[, max]) ; ('voix', rect, txt[, max]) ;
# ('cri', rect, txt[, max]) ; ('ono', (cx, cy), txt[, size])
PAGES = {
    1: [
        ('encadre', (55, 45, 600, 110), "SAISON DERNIÈRE — CATÉGORIE U6. SEPT TOURNOIS DISPUTÉS. CINQ REMPORTÉS. DEUX FOIS DEUXIÈMES."),
        ('bulle', (470, 50, 800, 120), "ON EST LES CHAMPIONS ! PERSONNE NE PEUT NOUS BATTRE !", [(500, 118), (525, 118), (455, 180)]),
        ('bulle', (60, 655, 340, 740), "Cinq coupes en une seule saison ! Même les grands du club n'en reviennent pas !", [(150, 657), (175, 657), (190, 610)]),
        ('encadre', (45, 805, 275, 930), "Je m'appelle Léon. J'ai 6 ans. Et avec mes copains du Rugby Club Motterain, on a vécu une saison magique."),
        ('bulle', (45, 1085, 275, 1180), "Passe-moi la balle Lyssandro, j'ai mis mes chaussures fusées !", [(85, 1087), (110, 1087), (95, 1040)]),
        ('bulle', (315, 805, 555, 870), "Cinq fois premiers et deux fois deuxièmes… Vous vous rendez compte ?", [(350, 868), (375, 868), (360, 900)]),
        ('bulle', (315, 1090, 555, 1180), "C'est sûr, l'année prochaine chez les U8, ce sera exactement pareil !", [(480, 1092), (505, 1092), (515, 1045)]),
        ('bulle', (585, 800, 830, 960), "Pas « exactement pareil », Ayden… Ce sera encore MIEUX ! En U8, on ne finira même plus deuxièmes : on va TOUT gagner !", [(600, 962), (625, 962), (615, 1005)]),
    ],
    2: [
        ('encadre', (50, 45, 410, 105), "SEPTEMBRE 2026. SAINT-SULPICE, SAVOIE. LE JOUR DE LA REPRISE EN CATÉGORIE U8."),
        ('bulle', (460, 42, 820, 112), "Vanessa ! Alice ! On file au stade avec Léon, on rentre pour le déjeuner !", [(490, 114), (515, 114), (505, 155)]),
        ('voix', (620, 180, 820, 245), "Bon entraînement les garçons ! Amuse-toi bien Léon !"),
        ('bulle', (455, 240, 700, 322), "Merci Maman ! À tout à l'heure Alice ! Dépêche-toi Papa, on va arriver après les copains !", [(480, 242), (505, 242), (470, 205)]),
        ('bulle', (45, 358, 410, 448), "Papa, j'ai déjà fait le calcul dans ma tête ! Si on fait sept tournois cette année en U8, ça fera sept nouveaux trophées sur mon étagère !", [(100, 450), (125, 450), (110, 490)]),
        ('bulle', (45, 540, 410, 630), "Sept sur sept ? Carrément ! Tu ne crois pas que tu vas un peu vite en besogne, champion ?", [(330, 542), (355, 542), (370, 500)]),
        ('bulle', (455, 358, 820, 448), "Bah quoi ? En U6, presque personne ne nous arrêtait ! Et on a toujours la même bande : Lyssandro, Ayden, Nolann, Milo et moi !", [(480, 450), (505, 450), (490, 490)]),
        ('bulle', (455, 535, 820, 635), "Justement, Léon. En U8, les autres clubs aussi ont grandi. Et les règles changent beaucoup. Écoute bien ce qu'on va vous expliquer avec Julien et Kilian.", [(750, 537), (775, 537), (790, 495)]),
        ('encadre', (50, 670, 400, 745), "LA MOTTE-SERVOLEX — STADE DU RUGBY CLUB MOTTERAIN."),
        ('bulle', (50, 1090, 400, 1185), "Regarde Papa ! Il y a déjà la voiture de Julien ! Lyssandro est arrivé !", [(100, 1092), (125, 1092), (110, 1040)]),
    ],
    3: [
        ('encadre', (45, 42, 410, 100), "NOUVELLE SAISON, NOUVELLE CATÉGORIE : VINGT JOUEURS COMPOSENT LE GROUPE U8 DU RCM !"),
        ('bulle', (455, 42, 820, 115), "Salut les gars ! Alors, prêts pour notre nouvelle saison de champions ?", [(480, 117), (505, 117), (490, 160)]),
        ('bulle', (455, 180, 820, 255), "Trop content de vous retrouver ! Mon père m'a dit qu'on est vingt joueurs cette année, ça va faire quatre équipes de cinq !", [(470, 257), (495, 257), (460, 215)]),
        ('bulle', (455, 262, 820, 322), "Ouais ! Avec Léon, on en a parlé toute la semaine à l'école !", [(790, 264), (815, 264), (825, 290)]),
        ('bulle', (45, 355, 410, 430), "Regardez le maillot Rouge, Bleu et Blanc ! En U8, on dirait carrément l'équipe première !", [(70, 432), (95, 432), (80, 470)]),
        ('bulle', (45, 545, 410, 630), "Et regardez mes appuis : zip, zap, essai ! Qui m'attrape ?!", [(350, 547), (375, 547), (390, 510)]),
        ('ono', (490, 380), "FIIIIIIIIT !", 16),
        ('bulle', (600, 355, 830, 470), "Rassemblement les U8 ! Tout le monde s'assoit en demi-cercle devant nous, et on pose les ballons !", [(620, 472), (645, 472), (630, 510)]),
        ('bulle', (45, 665, 410, 760), "Bienvenue en U8 les garçons ! Avant de commencer l'entraînement, on doit vous parler franchement de ce qui s'est passé la saison dernière…", [(75, 762), (100, 762), (85, 805)]),
        ('bulle', (45, 1090, 410, 1185), "Tu vas voir, ils vont nous féliciter pour nos cinq trophées !", [(90, 1092), (115, 1092), (130, 1045)]),
    ],
    4: [
        ('bulle', (35, 35, 410, 150), "La saison dernière en U6, sur 7 tournois, vous en avez gagné 5 et fini 2es sur les 2 autres. C'était génial… mais écoutez-moi bien : une saison comme celle-là, c'est EXCEPTIONNEL et ça arrive très rarement !", [(60, 152), (85, 152), (70, 195)]),
        ('bulle', (35, 290, 410, 390), "Si vous croyez que vous allez gagner sans effort cette année parce que vous avez gagné en U6, vous allez avoir une énorme surprise !", [(340, 292), (365, 292), (380, 255)]),
        ('bulle', (455, 35, 830, 140), "En U8, voici vos nouvelles règles ! On joue à 5 contre 5 sur un terrain de 30 mètres par 20 mètres. Il n'y a pas de poteaux et pas de transformations : chaque essai marqué vaut 1 point !", [(480, 142), (505, 142), (490, 185)]),
        ('bulle', (35, 427, 410, 520), "Deuxième grand changement : l'arbitre siffle TOUS les en-avant quand le ballon tombe vers le camp adverse, et tous les hors-jeu si vous êtes devant le copain qui a le ballon !", [(60, 522), (85, 522), (70, 565)]),
        ('bulle', (35, 555, 230, 650), "Tous les en-avant ?! Même les tout petits ?!", [(55, 652), (80, 652), (65, 690)]),
        ('bulle', (240, 555, 410, 650), "Même les tout petits, Milo !", [(390, 652), (412, 652), (420, 690)]),
        ('bulle', (455, 427, 830, 520), "Et quand un joueur sort en touche, le ballon est directement rendu à l'autre équipe et il est joué comme une pénalité !", [(480, 522), (505, 522), (490, 565)]),
        ('bulle', (455, 565, 830, 665), "Enfin, pour les contacts : de septembre à fin novembre, c'est du touché à 2 mains simultanées ! Les vrais plaquages seront autorisés à partir du mois de décembre !", [(770, 567), (795, 567), (810, 530)]),
        ('bulle', (35, 697, 410, 775), "Faut faire super attention aux passes alors, sinon on rend tout le temps le ballon…", [(60, 777), (85, 777), (70, 818)]),
        ('bulle', (35, 835, 410, 920), "Et en défense, si on est hors-jeu, on se fait punir direct !", [(340, 837), (365, 837), (380, 800)]),
        ('bulle', (35, 955, 410, 1080), "Pfff, vous inquiétez pas les gars ! Touché à deux mains ou nouvelles règles, personne ne court aussi vite que nous. On va quand même tout rafler !", [(60, 1082), (85, 1082), (110, 1120)]),
    ],
    5: [
        ('ono', (110, 75), "FIIIIT !", 16),
        ('bulle', (300, 55, 820, 160), "En-avant ! Ballon rendu à l'autre équipe ! On garde les mains bien ouvertes en W devant la poitrine, Milo !", [(330, 162), (355, 162), (340, 205)]),
        ('ono', (90, 545), "FIIIIT !", 15),
        ('bulle', (35, 570, 410, 680), "Hors-jeu Léon ! Tu étais devant tes copains au départ de l'action !", [(60, 682), (85, 682), (70, 725)]),
        ('bulle', (35, 760, 410, 835), "Mais Coach, j'allais l'attraper ! Ça arrête pas de siffler en U8 !", [(340, 762), (365, 762), (380, 725)]),
        ('encadre', (455, 525, 830, 585), "PLUS TARD, DANS LE VESTIAIRE DES COACHS…"),
        ('bulle', (455, 600, 830, 710), "Bon, avec nos 20 joueurs, nos 4 équipes de 5 prennent forme pour le premier tournoi d'octobre. Sur le papier, l'équipe de Léon, Lyssandro, Ayden, Nolann et Milo a du feu dans les jambes.", [(480, 712), (505, 712), (490, 755)]),
        ('bulle', (35, 868, 410, 975), "Du feu dans les jambes, oui… mais tu as vu leur réaction à chaque coup de sifflet ? Ils ont encore la tête en U6 où il suffisait de courir tout droit pour marquer.", [(60, 977), (85, 977), (70, 1020)]),
        ('bulle', (35, 1050, 410, 1175), "C'est vrai qu'au niveau des passes sous pression et de la défense en ligne, il y a encore tout à construire.", [(340, 1052), (365, 1052), (380, 1015)]),
        ('bulle', (455, 868, 830, 975), "C'est surtout pour Léon que je m'inquiète. Il a un tel esprit de gagnant qu'il ne conçoit même pas qu'on puisse perdre un match.", [(480, 977), (505, 977), (490, 1020)]),
        ('bulle', (455, 1050, 830, 1175), "Le premier tournoi va être un sacré révélateur, Flavien. On sera là pour les accompagner.", [(770, 1052), (795, 1052), (810, 1015)]),
    ],
    6: [
        ('encadre', (35, 55, 420, 130), "OCTOBRE 2026 — PREMIER TOURNOI U8 DE LA SAISON. TROIS MATCHS AU PROGRAMME DE LA POULE !"),
        ('bulle', (450, 55, 830, 145), "Allez le RCM ! On se souvient des règles : 5 contre 5, touché à deux mains, pas de hors-jeu et on fait vivre le ballon !", [(480, 147), (505, 147), (490, 190)]),
        ('bulle', (35, 530, 400, 610), "Bien joué Ayden ! Tiens Nolann, fonce !", [(60, 612), (85, 612), (70, 655)]),
        ('bulle', (35, 700, 400, 790), "ESSAI ! UN POINT POUR LE RCM !", [(340, 702), (365, 702), (380, 665)]),
        ('encadre', (35, 805, 400, 845), "MATCH 1 : RCM bat CHAMBÉRY (JAUNE ET NOIR) !"),
        ('bulle', (455, 530, 830, 610), "À toi Léon !", [(480, 612), (505, 612), (490, 655)]),
        ('bulle', (455, 680, 830, 780), "Personne ne me rattrapera ! ESSAI !", [(770, 682), (795, 682), (810, 645)]),
        ('encadre', (455, 805, 830, 845), "MATCH 2 : RCM bat ALBERTVILLE (ROUGE ET BLANC) !"),
        ('bulle', (35, 875, 400, 985), "Deux matchs, deux victoires ! Qu'est-ce que je vous avais dit ?! C'est trop facile la catégorie U8, on est toujours invincibles !", [(60, 987), (85, 987), (70, 1030)]),
        ('bulle', (35, 1060, 400, 1185), "Attends Léon, contre Albertville on a quand même eu chaud sur la fin…", [(340, 1062), (365, 1062), (380, 1025)]),
        ('bulle', (455, 875, 830, 990), "Écoutez bien les garçons : le troisième match, c'est contre Montmélian. Ils ont gagné leurs deux matchs aussi.", [(480, 992), (505, 992), (490, 1035)]),
        ('bulle', (455, 1060, 830, 1185), "Ils montent très vite en défense et ils ne laissent aucun espace. Si vous jouez chacun pour vous, ça ne passera pas !", [(770, 1062), (795, 1062), (810, 1025)]),
    ],
    7: [
        ('bulle', (35, 52, 410, 135), "On monte ensemble les Vert et Noir ! Personne ne passe !", [(60, 137), (85, 137), (70, 180)]),
        ('bulle', (455, 52, 830, 135), "Oh là là, ils sont déjà sur nous !", [(480, 137), (505, 137), (490, 180)]),
        ('ono', (100, 430), "PLOP !", 14),
        ('ono', (300, 412), "FIIIIT !", 15),
        ('bulle', (35, 450, 400, 525), "En-avant du RCM ! Ballon rendu à Montmélian !", [(60, 527), (85, 527), (70, 565)]),
        ('bulle', (35, 530, 400, 600), "Mais fais attention Milo !", [(340, 532), (365, 532), (380, 495)]),
        ('ono', (700, 412), "FIIIIT !", 15),
        ('bulle', (455, 440, 830, 520), "Touche ! Ballon rendu à Montmélian, joué comme une pénalité !", [(480, 522), (505, 522), (490, 560)]),
        ('bulle', (455, 530, 830, 600), "Mince, le terrain de 20 mètres est moins large que je croyais !", [(770, 532), (795, 532), (810, 495)]),
        ('bulle', (35, 632, 400, 740), "La ligne défensive les garçons ! Si Léon monte tout seul, ça ouvre un boulevard !", [(60, 742), (85, 742), (70, 785)]),
        ('encadre', (35, 790, 400, 825), "ESSAI DE MONTMÉLIAN ! +1 POINT !"),
        ('ono', (700, 635), "FIIIIT !", 15),
        ('bulle', (455, 655, 830, 745), "Hors-jeu du joueur du RCM ! Pénalité pour Montmélian !", [(480, 747), (505, 747), (490, 790)]),
        ('bulle', (35, 855, 410, 950), "Calmez-vous le RCM ! Respirez ! Regardez vos copains avant de courir !", [(60, 952), (85, 952), (70, 995)]),
        ('bulle', (455, 855, 830, 950), "Ils s'énervent au lieu de construire…", [(480, 952), (505, 952), (490, 995)]),
    ],
    8: [
        ('bulle', (35, 55, 410, 140), "Vas-y Léon ! On monte avec toi !", [(60, 142), (85, 142), (70, 185)]),
        ('bulle', (35, 525, 400, 615), "Léon ! Passe à gauche, on est deux contre un !", [(60, 617), (85, 617), (70, 660)]),
        ('bulle', (35, 700, 400, 810), "Ici Léon ! Je suis tout seul sur l'aile !", [(340, 702), (365, 702), (380, 665)]),
        ('pensee', (455, 530, 830, 640), "Non ! C'est moi qui vais sauver l'équipe ! Je vais passer au milieu tout seul comme en U6 !", [(470, 650, 9), (492, 668, 6), (510, 683, 4)]),
        ('ono', (100, 880), "TCHAC !", 14),
        ('ono', (330, 875), "FIIIIIIIT !", 15),
        ('bulle', (35, 905, 400, 1010), "Touché à deux mains… et en-avant ! C'est terminé, fin du match !", [(60, 1012), (85, 1012), (70, 1055)]),
        ('encadre', (455, 875, 830, 960), "PREMIER TOURNOI U8 : 2 VICTOIRES, 1 DÉFAITE. LE RÊVE D'INVINCIBILITÉ VIENT DE VOLER EN ÉCLATS."),
    ],
    9: [
        ('bulle', (35, 45, 410, 130), "Bien joué Montmélian… Vous avez super bien défendu.", [(60, 132), (85, 132), (70, 175)]),
        ('bulle', (455, 45, 830, 130), "Merci ! À bientôt au prochain tournoi !", [(480, 132), (505, 132), (490, 175)]),
        ('bulle', (35, 420, 315, 545), "Non… Non, c'est pas vrai ! On n'a pas le droit de perdre ! On est le RCM ! En U6 on gagnait toujours !", [(60, 547), (85, 547), (120, 590)]),
        ('bulle', (355, 420, 600, 505), "Léon, calme-toi… On a quand même gagné deux matchs sur trois aujourd'hui !", [(380, 507), (405, 507), (390, 550)]),
        ('bulle', (610, 420, 835, 505), "Ouais, contre Chambéry et Albertville on a super bien joué !", [(780, 507), (805, 507), (815, 470)]),
        ('bulle', (355, 680, 835, 790), "Deux sur trois, c'est NUL ! Si on perd contre Montmélian, on n'est pas les premiers ! Moi je veux pas perdre ! Jamais !", [(380, 792), (405, 792), (390, 812)]),
        ('bulle', (35, 845, 410, 945), "Viens boire une gorgée d'eau, Léon. La colère ne fera pas rejouer le match.", [(60, 947), (85, 947), (70, 990)]),
        ('bulle', (455, 845, 830, 945), "Ce n'est que le début de la saison… Il va falloir que le groupe apprenne à rebondir.", [(480, 947), (505, 947), (490, 990)]),
    ],
    10: [
        ('bulle', (35, 55, 410, 145), "Oui Vanessa, je couche Léon et j'arrive ! Bonne nuit Alice !", [(60, 147), (85, 147), (70, 190)]),
        ('bulle', (450, 55, 830, 150), "Papa… Pourquoi l'arbitre il a sifflé tout le temps contre nous face à Montmélian ?", [(475, 152), (500, 152), (485, 195)]),
        ('bulle', (35, 525, 400, 650), "Ce n'est pas la faute de l'arbitre, Léon. En U8, les règles sont les mêmes pour tout le monde. Montmélian a juste mieux joué en équipe que nous sur ce match-là.", [(60, 652), (85, 652), (70, 695)]),
        ('bulle', (35, 750, 400, 835), "Pfff… Ils ont surtout eu de la chance !", [(340, 752), (365, 752), (380, 715)]),
        ('encadre', (455, 525, 830, 580), "LUNDI MATIN — À L'ÉCOLE, AVEC AYDEN."),
        ('bulle', (455, 595, 830, 690), "Alors Léon, t'es toujours fâché pour samedi ?", [(480, 692), (505, 692), (490, 735)]),
        ('bulle', (455, 760, 830, 835), "Bien sûr que je suis fâché ! Quand je repense à leurs maillots Vert et Noir, ça m'énerve !", [(770, 762), (795, 762), (810, 725)]),
        ('bulle', (35, 868, 410, 1000), "Tu sais, j'en ai parlé tout à l'heure avec Baptiste avant la sonnerie. Lui aussi au rugby ce week-end, il m'a dit qu'avec les nouvelles règles U8, son équipe a fait plein d'en-avant et de hors-jeu !", [(60, 1002), (85, 1002), (70, 1045)]),
        ('bulle', (35, 1060, 410, 1180), "Ah ouais ? Même Baptiste il a perdu un match ?", [(340, 1062), (365, 1062), (380, 1025)]),
        ('bulle', (455, 868, 830, 975), "Bah oui ! Baptiste dit que ses coachs leur ont expliqué qu'au début en U8, tout le monde se trompe.", [(480, 977), (505, 977), (490, 1020)]),
        ('bulle', (455, 1040, 830, 1180), "Mouais… Eh ben moi, mercredi à l'entraînement, je veux plus qu'on se trompe du tout !", [(770, 1042), (795, 1042), (810, 1005)]),
    ],
    11: [
        ('encadre', (35, 53, 420, 120), "FIN D'AUTOMNE À LA MOTTE-SERVOLEX. LA PLUIE SAVOYARDE S'INVITE À L'ENTRAÎNEMENT."),
        ('bulle', (35, 525, 400, 640), "Écoutez-moi tous les vingt ! Samedi dernier, on a vu de belles choses, mais on a aussi compris pourquoi une équipe comme Montmélian nous a battus.", [(60, 642), (85, 642), (70, 685)]),
        ('bulle', (35, 730, 400, 835), "Qui peut me dire ce qui nous a manqué quand ça devenait dur ?", [(340, 732), (365, 732), (380, 695)]),
        ('bulle', (455, 525, 830, 625), "Quand ils couraient vers nous, on n'était pas alignés ! Y en avait un devant et les autres derrière !", [(480, 627), (505, 627), (490, 670)]),
        ('bulle', (455, 640, 830, 735), "Et quand l'un de nous avait le ballon, il essayait de passer tout seul au lieu de faire la passe aux copains !", [(770, 642), (795, 642), (810, 605)]),
        ('bulle', (455, 745, 830, 835), "Et on a fait tomber le ballon vers l'avant plein de fois !", [(790, 747), (815, 747), (825, 715)]),
        ('bulle', (35, 868, 400, 985), "Bravo les garçons, vous avez tout compris ! En U8, un joueur tout seul ne gagnera JAMAIS contre cinq adversaires organisés.", [(60, 987), (85, 987), (70, 1030)]),
        ('bulle', (35, 1030, 400, 1180), "Pour progresser, on va travailler nos trois armes secrètes : des passes propres en arrière, une défense en ligne qui monte ensemble sans hors-jeu, et le soutien offensif toujours derrière le copain !", [(340, 1032), (365, 1032), (380, 995)]),
        ('bulle', (455, 868, 830, 980), "Et sous la pluie, le ballon glisse ! C'est le meilleur moment pour apprendre à s'appliquer ! Allez, tout le monde sur le pré !", [(480, 982), (505, 982), (490, 1025)]),
        ('bulle', (455, 1040, 830, 1180), "Ouais ! Du rugby sous la pluie !", [(770, 1042), (795, 1042), (810, 1005)]),
    ],
    12: [
        ('bulle', (40, 40, 820, 130), "On monte ensemble ! Regardez à votre gauche et à votre droite ! Si Léon accélère tout seul, vous criez quoi ?", [(65, 132), (90, 132), (75, 175)]),
        ('bulle', (40, 290, 400, 365), "ATTENDS LA LIGNE !", [(65, 292), (90, 292), (75, 255)]),
        ('bulle', (40, 400, 410, 495), "Eh ! Vous avez vu ? Quand on reste collés sur la même ligne, ils savent plus du tout par où passer !", [(65, 497), (90, 497), (75, 540)]),
        ('bulle', (455, 400, 830, 530), "C'est ça le soutien offensif ! Vous êtes les gardes du corps du porteur de balle ! Toujours derrière lui pour ne pas être hors-jeu ou faire d'en-avant, mais prêts à crier « JE SUIS LÀ ! »", [(480, 532), (505, 532), (490, 575)]),
        ('bulle', (40, 632, 410, 700), "Tiens Lyssandro !", [(65, 702), (90, 702), (75, 745)]),
        ('bulle', (40, 740, 410, 830), "Super passe Ayden, j'ai même pas eu besoin de ralentir !", [(340, 742), (365, 742), (380, 705)]),
        ('ono', (700, 650), "SPLATCH !", 14),
        ('bulle', (455, 670, 830, 780), "Oups… Il glisse comme un savon ce ballon !", [(480, 782), (505, 782), (490, 820)]),
        ('bulle', (40, 865, 410, 965), "Pfff… Sérieux Milo, si tu fais encore tomber le ballon comme ça au prochain tournoi, on va encore perdre !", [(65, 967), (90, 967), (75, 1010)]),
        ('bulle', (455, 865, 830, 965), "Oh ça va Léon, arrête de râler ! Toi aussi t'en as fait tomber un tout à l'heure !", [(480, 967), (505, 967), (490, 1010)]),
        ('bulle', (40, 1050, 830, 1185), "Lyssandro a raison, Léon. À l'entraînement, on est là pour essayer et se tromper. Encourage ton copain au lieu de soupirer.", [(65, 1052), (90, 1052), (75, 1015)]),
    ],
    13: [
        ('encadre', (40, 42, 820, 100), "NOVEMBRE 2026 — DEUXIÈME TOURNOI. AU FIL DES SEMAINES, L'ÉQUIPE CONNAÎT DES HAUTS… ET DES BAS."),
        ('bulle', (40, 350, 410, 430), "Soutien à droite ! Vas-y Ayden !", [(65, 432), (90, 432), (75, 475)]),
        ('bulle', (40, 480, 410, 550), "Pour toi Léon, va marquer !", [(340, 482), (365, 482), (380, 445)]),
        ('bulle', (455, 350, 830, 430), "Oui ! Quand on gagne comme ça, j'adore le rugby !", [(480, 432), (505, 432), (490, 475)]),
        ('bulle', (455, 480, 830, 550), "Super collectif les garçons ! Gardez cette tête-là pour le match contre Rumilly !", [(770, 482), (795, 482), (810, 445)]),
        ('bulle', (40, 583, 410, 668), "On les bloque chez eux les Rouge et Noir !", [(65, 670), (90, 670), (75, 713)]),
        ('bulle', (455, 583, 830, 668), "Mais plus vite ! Passez-moi le ballon !", [(480, 670), (505, 670), (490, 713)]),
        ('ono', (660, 735), "PAF !", 13),
        ('ono', (770, 735), "FIIIIT !", 13),
        ('bulle', (40, 820, 410, 915), "Essai pour Rumilly ! Fin du match !", [(65, 917), (90, 917), (75, 960)]),
    ],
    14: [
        ('bulle', (40, 42, 410, 120), "Désolé les gars… Le ballon est arrivé super vite et j'ai glissé dans la boue…", [(65, 122), (90, 122), (75, 165)]),
        ('bulle', (455, 42, 825, 120), "C'est ma faute aussi Milo, ma passe était trop haute…", [(480, 122), (505, 122), (490, 165)]),
        ('bulle', (40, 305, 410, 450), "OUAIS, C'EST TOUJOURS PAREIL ! C'est à cause de vous deux qu'on a perdu ! Vous faites que des en-avant, vous savez même pas attraper un ballon ! Avec vous, on gagnera jamais rien !", [(65, 452), (90, 452), (120, 495)]),
        ('bulle', (40, 652, 410, 730), "Je l'ai pas fait exprès Léon…", [(65, 732), (90, 732), (75, 775)]),
        ('bulle', (40, 760, 410, 855), "Arrête Léon, t'es super méchant ! Toi non plus t'étais pas en ligne sur leur essai !", [(340, 762), (365, 762), (380, 725)]),
        ('bulle', (40, 780, 410, 850), "Ouais ! Si c'est pour nous crier dessus comme ça, on n'a même plus envie de te faire des passes !", [(250, 782), (275, 782), (250, 800)]),
        ('bulle', (455, 652, 830, 760), "Ça suffit, Léon. On ne parle JAMAIS comme ça à ses coéquipiers. Viens avec moi sur le banc, tout de suite.", [(480, 762), (505, 762), (490, 805)]),
        ('bulle', (455, 780, 830, 855), "Venez les garçons, n'écoutez pas ça. Vous avez tout donné sur le terrain.", [(770, 782), (795, 782), (810, 745)]),
        ('pensee', (40, 900, 420, 1030), "Pourquoi j'ai dit ça… Milo et Nolann, c'est mes copains…", [(60, 1045, 9), (82, 1063, 6), (100, 1078, 4)]),
    ],
    15: [
        ('encadre', (38, 40, 500, 95), "LE SOIR MÊME, À SAINT-SULPICE…"),
        ('bulle', (520, 40, 825, 130), "Vanessa et Alice préparent le dîner à côté. Toi et moi, on a besoin de discuter d'homme à homme, Léon.", [(545, 132), (570, 132), (555, 175)]),
        ('bulle', (38, 292, 410, 380), "Je sais Papa… J'ai été méchant avec Milo et Nolann. Et avec Lyssandro et Ayden aussi.", [(63, 382), (88, 382), (73, 425)]),
        ('bulle', (38, 410, 410, 485), "Pourquoi tu t'es mis dans une colère pareille, mon grand ? Dis-moi ce qui se passe dans ton cœur quand on perd.", [(340, 412), (365, 412), (380, 375)]),
        ('bulle', (455, 292, 830, 385), "C'est que… j'ai trop envie qu'on gagne ! Quand l'autre équipe marque et qu'on perd, j'ai l'impression qu'on est devenus nuls par rapport à l'année dernière en U6… et ça me fait trop mal au ventre !", [(480, 387), (505, 387), (490, 430)]),
        ('bulle', (38, 520, 410, 640), "Écoute-moi bien, Léon, et garde cette phrase dans ta tête pour toute ta vie : on apprend toujours de ses échecs, jamais de ses victoires.", [(63, 642), (88, 642), (73, 685)]),
        ('bulle', (455, 720, 830, 855), "Quand on gagne tout comme en U6, on croit qu'on est parfait et on n'apprend rien. Mais quand on échoue, qu'on fait un en-avant ou qu'on perd un match… c'est là qu'on voit ce qu'il faut travailler pour évoluer !", [(480, 857), (505, 857), (490, 885)]),
        ('bulle', (38, 922, 410, 1010), "Alors… perdre un match, ça veut pas dire qu'on est nuls ? Ça veut dire qu'on est en train d'apprendre ?", [(63, 1012), (88, 1012), (73, 1055)]),
        ('bulle', (455, 922, 830, 1070), "Exactement champion : on apprend de ses échecs, c'est ce qui conduit à la victoire. Mais pour que l'équipe apprenne, tes copains ont besoin que tu les aides à comprendre, pas que tu leur cries dessus. Tu sais ce qu'il te reste à faire ?", [(480, 1072), (505, 1072), (490, 1115)]),
        ('bulle', (38, 1090, 410, 1190), "Oui Papa. Dès demain.", [(340, 1092), (365, 1092), (380, 1055)]),
    ],
    16: [
        ('bulle', (40, 40, 410, 150), "Salut Ayden… Je voulais te demander pardon pour samedi. T'avais raison, j'avais pas le droit de vous parler comme ça.", [(65, 152), (90, 152), (75, 195)]),
        ('bulle', (455, 40, 825, 190), "Je suis content que tu dises ça, Léon ! Justement, j'en parlais ce matin avec Baptiste devant le portail : Baptiste m'a dit que dans son équipe aussi, ils se sont promis de toujours s'encourager après une erreur !", [(480, 192), (505, 192), (490, 230)]),
        ('bulle', (455, 285, 825, 390), "Il a raison Baptiste. Mercredi au stade, je vais m'excuser auprès de Lyssandro, Nolann et Milo !", [(480, 392), (505, 392), (490, 435)]),
        ('bulle', (40, 285, 410, 410), "Les gars… Pardon d'avoir été méchant contre Rumilly. Mon papa m'a expliqué qu'on apprend toujours de nos échecs. Si on fait un en-avant ou qu'on perd, je ne m'énerverai plus : on cherchera ensemble comment faire mieux !", [(65, 412), (90, 412), (75, 455)]),
        ('bulle', (40, 565, 410, 655), "C'est vrai, tu nous crieras plus dessus si le ballon glisse ?", [(65, 657), (90, 657), (75, 700)]),
        ('bulle', (455, 565, 825, 650), "Promis juré ! Même s'il est plein de boue !", [(480, 652), (505, 652), (490, 695)]),
        ('bulle', (40, 730, 410, 820), "Trop bien ! Parce qu'ensemble, on est les cinq mousquetaires du RCM !", [(340, 732), (365, 732), (380, 695)]),
        ('bulle', (455, 730, 825, 850), "Allez, tapez tous vos mains au milieu : UN POUR TOUS, TOUS POUR LE RCM !", [(480, 852), (505, 852), (490, 895)]),
        ('bulle', (40, 965, 410, 1065), "Eh bien Flavien, je crois que ta discussion à la maison a fait des miracles !", [(65, 1067), (90, 1067), (75, 1110)]),
        ('bulle', (455, 965, 825, 1085), "Tant mieux, parce qu'avec l'hiver qui arrive en Savoie et le mois de décembre… ils vont avoir besoin d'être soudés !", [(480, 1087), (505, 1087), (490, 1130)]),
    ],
    17: [
        ('encadre', (38, 40, 820, 100), "DÉCEMBRE EN SAVOIE. LE FROID ET LA NEIGE SONT LÀ… MAIS AU RUGBY CLUB MOTTERAIN, L'ENTRAÎNEMENT EST MAINTENU !"),
        ('bulle', (38, 296, 410, 370), "Brrr ! Regardez, on dirait des dragons qui crachent de la fumée !", [(63, 372), (88, 372), (73, 415)]),
        ('bulle', (38, 420, 410, 500), "Avec mes gants de sport et mon bonnet, j'ai même pas froid !", [(340, 422), (365, 422), (380, 385)]),
        ('bulle', (455, 296, 830, 370), "Et surtout… vous avez vu le calendrier ? On est au mois de DÉCEMBRE !", [(480, 372), (505, 372), (490, 415)]),
        ('bulle', (38, 530, 410, 625), "Eh oui les garçons ! Qui dit mois de décembre en U8 dit… nouvelle règle !", [(63, 627), (88, 627), (73, 670)]),
        ('bulle', (455, 530, 830, 640), "Le touché à deux mains, c'est terminé ! À partir d'aujourd'hui, les vrais PLAQUAGES sont autorisés !", [(480, 642), (505, 642), (490, 685)]),
        ('bulle', (38, 700, 410, 775), "OUAAAAIS ! LES PLAQUAGES !", [(63, 777), (88, 777), (73, 820)]),
        ('bulle', (455, 700, 830, 790), "Enfin du vrai rugby de grands !", [(770, 702), (795, 702), (810, 665)]),
        ('bulle', (38, 910, 830, 1030), "Attention les guerriers ! Plaquer, ce n'est pas se jeter n'importe comment. Pour ne blesser personne et ne pas se faire mal, il y a une technique précise à apprendre. Regardez bien !", [(63, 1032), (88, 1032), (73, 1075)]),
    ],
    18: [
        ('bulle', (42, 40, 410, 140), "Règle numéro 1 : on baisse son centre de gravité, on vise entre la taille et les cuisses, JAMAIS au-dessus des épaules !", [(67, 142), (92, 142), (77, 185)]),
        ('bulle', (455, 40, 825, 140), "Règle numéro 2 : on pose l'épaule, on serre fort ses deux bras autour des jambes comme une ceinture, et on accompagne le joueur au sol !", [(480, 142), (505, 142), (490, 185)]),
        ('ono', (620, 55), "BOUM !", 15),
        ('bulle', (455, 80, 825, 160), "Super Nolann ! Bien bas et les bras bien fermés !", [(480, 162), (505, 162), (490, 205)]),
        ('bulle', (455, 185, 825, 245), "Même le boudin il a pas bougé d'un centimètre !", [(770, 187), (795, 187), (810, 150)]),
        ('bulle', (42, 277, 410, 360), "Je le plaque en bas, Milo !", [(67, 362), (92, 362), (77, 405)]),
        ('bulle', (455, 277, 830, 360), "Et moi je récupère le ballon dès qu'il est au sol !", [(480, 362), (505, 362), (490, 405)]),
        ('ono', (430, 650), "PAF !", 16),
        ('bulle', (42, 985, 410, 1080), "Bien plaqué ! Tiens Lyssandro, je te la laisse, continue l'action !", [(67, 1082), (92, 1082), (77, 1125)]),
        ('bulle', (455, 985, 825, 1080), "J'y vais Léon, bien joué !", [(480, 1082), (505, 1082), (490, 1125)]),
        ('bulle', (455, 1110, 825, 1190), "Bravo Léon ! En octobre tu aurais gardé le ballon pour toi tout seul. Là, tu as utilisé le plaquage pour faire briller ton copain en soutien !", [(480, 1098), (505, 1098), (490, 1060)]),
    ],
    19: [
        ('bulle', (42, 102, 410, 215), "Hé les gars, regardez ce que j'ai compris ! Avec les vrais plaquages maintenant, le premier qui a le ballon se fait presque toujours arrêter s'il court tout droit.", [(67, 217), (92, 217), (77, 260)]),
        ('bulle', (455, 102, 830, 215), "Oui ! Alors que si on est deux juste derrière lui en soutien offensif, dès qu'il est plaqué, l'action continue sans s'arrêter !", [(480, 217), (505, 217), (490, 260)]),
        ('bulle', (42, 570, 410, 680), "Et en défense, c'est pareil : mon papa dit que si un seul de nous cinq monte trop vite, il est hors-jeu ou il se fait éviter. Faut qu'on avance comme un mur !", [(67, 682), (92, 682), (77, 725)]),
        ('bulle', (42, 750, 410, 830), "Le mur Rouge, Bleu et Blanc du RCM !", [(340, 752), (365, 752), (380, 715)]),
        ('bulle', (455, 570, 830, 680), "Regardez-les tous les cinq là-bas… Ils n'attendent même plus qu'on leur parle, ils préparent déjà leurs combinaisons entre eux !", [(480, 682), (505, 682), (490, 725)]),
        ('bulle', (42, 865, 410, 975), "Ce week-end, on affronte Le Môle et Thonon. Ce sont deux équipes très solides qui plaquent fort.", [(67, 977), (92, 977), (77, 1020)]),
        ('bulle', (42, 1040, 410, 1190), "Ce sera le vrai test pour voir si Léon garde son calme quand un copain fera une erreur sous pression.", [(340, 1042), (365, 1042), (380, 1005)]),
        ('bulle', (455, 865, 830, 1000), "J'ai confiance en eux, Flavien. Nos petits U8 sont en train de devenir une vraie équipe de rugby.", [(480, 1002), (505, 1002), (490, 1045)]),
    ],
    20: [
        ('ono', (100, 60), "TCHAC !", 15),
        ('ono', (300, 55), "FIIIIT !", 16),
        ('bulle', (400, 45, 820, 145), "Sortie en touche ! Ballon rendu au RCM et joué comme une pénalité !", [(425, 147), (450, 147), (435, 190)]),
        ('bulle', (42, 510, 410, 600), "Vite, ils ne sont pas replacés ! À toi Léon !", [(67, 602), (92, 602), (77, 645)]),
        ('bulle', (42, 660, 410, 760), "Merci Lyssandro ! ESSAI !", [(340, 662), (365, 662), (380, 625)]),
        ('encadre', (42, 775, 410, 810), "VICTOIRE DU RCM CONTRE LE MÔLE (ROUGE ET BLANC) !"),
        ('bulle', (455, 510, 830, 615), "Dernière action le RCM ! Construisez, ne vous précipitez pas !", [(480, 617), (505, 617), (490, 660)]),
        ('ono', (110, 855), "BOUM !", 14),
        ('ono', (300, 850), "FIIIIIIIT !", 14),
        ('bulle', (42, 880, 410, 990), "En-avant ! Et c'est la fin du match ! Victoire de Thonon !", [(67, 992), (92, 992), (77, 1035)]),
        ('bulle', (455, 855, 830, 1000), "Oh non… J'ai raté l'essai de l'égalisation… Pardon Léon, pardon les gars…", [(480, 1002), (505, 1002), (490, 1045)]),
    ],
    21: [
        ('pensee', (42, 42, 430, 175), "Non. Si je crie sur Milo, on n'apprend rien. Cherche pourquoi on a raté l'action, Léon…", [(60, 190, 9), (82, 208, 6), (100, 223, 4)]),
        ('bulle', (42, 510, 410, 625), "Hé Milo, relève-toi ! C'est pas ta faute du tout ! Je t'ai fait la passe trop tard, le joueur de Thonon était déjà sur toi !", [(67, 627), (92, 627), (77, 670)]),
        ('bulle', (455, 505, 830, 580), "Tu… tu n'es pas en colère Léon ?", [(480, 582), (505, 582), (490, 620)]),
        ('bulle', (455, 592, 830, 690), "Bien sûr que non ! On a perdu d'un point contre Thonon, mais on sait exactement quoi travailler mercredi à l'entraînement : faire la passe avant le plaquage !", [(770, 594), (795, 594), (810, 557)]),
        ('bulle', (455, 700, 830, 755), "Et moi j'aurais dû être encore plus près de Milo en soutien offensif !", [(480, 702), (505, 702), (515, 690)]),
        ('bulle', (455, 762, 830, 812), "Trop bien dit Léon ! Au prochain tournoi, cette action-là, elle ira au bout !", [(770, 764), (795, 764), (810, 727)]),
        ('bulle', (42, 845, 410, 950), "Bravo Thonon ! Vos plaquages étaient super rapides !", [(67, 952), (92, 952), (77, 995)]),
        ('bulle', (455, 845, 830, 960), "Tu as vu ça, Flavien ? Ils viennent de perdre le match sur un en-avant à la dernière seconde… et Léon analyse la passe en relevant son copain !", [(480, 962), (505, 962), (490, 1005)]),
        ('bulle', (455, 1030, 830, 1140), "Il a compris, Julien. Il a enfin compris ce que veut dire grandir.", [(770, 1032), (795, 1032), (810, 995)]),
    ],
    22: [
        ('encadre', (42, 45, 820, 105), "MARS — LE SOLEIL DU PRINTEMPS REVIENT SUR LA SAVOIE. FINIS LES BONNETS ET LES GANTS : PLACE À LA VITESSE !"),
        ('bulle', (42, 510, 410, 640), "Les garçons, depuis septembre, on a connu des victoires, des défaites, de la pluie et de la neige. Qu'est-ce que nos défaites contre Montmélian, Rumilly et Thonon nous ont appris ?", [(67, 642), (92, 642), (77, 685)]),
        ('bulle', (455, 510, 830, 610), "Qu'il ne faut jamais jouer tout seul ni s'énerver ! Quand l'adversaire monte vite, il faut donner le ballon avant d'être plaqué !", [(480, 612), (505, 612), (490, 655)]),
        ('bulle', (455, 625, 830, 715), "Et que si on a toujours deux copains en soutien offensif dans notre dos, le ballon ne meurt jamais !", [(770, 627), (795, 627), (810, 590)]),
        ('bulle', (455, 725, 830, 810), "Et qu'en défense en ligne, on doit avancer tous les cinq comme un mur, sans faire de hors-jeu !", [(490, 727), (515, 727), (525, 695)]),
        ('bulle', (42, 845, 410, 950), "Eh bien montrez-nous ça sur le terrain ! Les 4 équipes de 5 en place !", [(67, 952), (92, 952), (77, 995)]),
        ('bulle', (455, 845, 830, 960), "Attention les yeux, la machine du RCM est lancée !", [(480, 962), (505, 962), (490, 1005)]),
    ],
    23: [
        ('bulle', (40, 68, 300, 145), "Mains en W !", [(65, 147), (90, 147), (75, 190)]),
        ('bulle', (310, 68, 560, 145), "Toujours en arrière, zéro en-avant !", [(335, 147), (360, 147), (345, 190)]),
        ('bulle', (570, 68, 830, 145), "Et au bout, toute la ligne a touché le ballon !", [(595, 147), (620, 147), (605, 190)]),
        ('bulle', (40, 350, 410, 445), "À gauche, monte d'un pas Nolann ! À droite, reste avec moi Léon !", [(65, 447), (90, 447), (75, 490)]),
        ('bulle', (455, 350, 830, 445), "Je te vois Ayden, on est alignés ! Personne n'est hors-jeu !", [(480, 447), (505, 447), (490, 490)]),
        ('bulle', (40, 632, 410, 715), "Je suis pris aux jambes ! Soutien !", [(65, 717), (90, 717), (75, 760)]),
        ('bulle', (455, 632, 830, 715), "ON EST LÀ DANS TON DOS !", [(480, 717), (505, 717), (490, 760)]),
        ('bulle', (40, 915, 410, 1025), "Plus un cri de colère, plus une tête baissée… Regardez la vitesse à laquelle le ballon circule !", [(65, 1027), (90, 1027), (75, 1070)]),
        ('bulle', (455, 915, 830, 1010), "Ils sont prêts pour le dernier grand tournoi de la saison.", [(480, 1012), (505, 1012), (490, 1055)]),
    ],
    24: [
        ('bulle', (40, 42, 830, 165), "Demain c'est le grand tournoi de fin de saison ! Baptiste vient de me dire que tous les clubs de Savoie seront là : Chambéry, Aix-les-Bains, Albertville, Le Môle, Rumilly, Thonon… et Montmélian !", [(65, 167), (90, 167), (75, 210)]),
        ('bulle', (40, 290, 830, 390), "Tant mieux qu'ils soient tous là, Ayden ! Ce sera le plus beau tournoi de l'année ! À demain matin au stade !", [(65, 392), (90, 392), (75, 435)]),
        ('bulle', (40, 510, 410, 615), "On fait encore dix passes avec Léon et on vient mettre la table, Vanessa !", [(65, 617), (90, 617), (75, 660)]),
        ('voix', (40, 700, 410, 775), "Dépêchez-vous, j'ai trop faim moi !"),
        ('bulle', (455, 510, 830, 625), "Dis-moi Léon… Demain, c'est le dernier tournoi U8 de la saison. Tu me promets que quoi qu'il arrive, tu garderas ce beau sourire ?", [(480, 627), (505, 627), (490, 670)]),
        ('bulle', (455, 650, 830, 810), "Promis Papa ! En septembre, je voulais juste la coupe pour dire qu'on était les plus forts. Demain, je veux qu'on joue notre meilleur rugby avec Lyssandro, Ayden, Nolann et Milo.", [(770, 652), (795, 652), (810, 615)]),
        ('bulle', (40, 845, 410, 975), "Et si jamais on fait une erreur… on saura quoi faire : apprendre tout de suite pour le match d'après !", [(65, 977), (90, 977), (75, 1020)]),
        ('bulle', (40, 1020, 410, 1140), "Je suis tellement fier de toi, mon fils.", [(340, 1022), (365, 1022), (380, 985)]),
    ],
    25: [
        ('encadre', (40, 45, 420, 120), "DERNIER TOURNOI DE LA SAISON U8. TOUTES LES ÉQUIPES DE SAVOIE SONT AU RENDEZ-VOUS !"),
        ('bulle', (450, 45, 830, 160), "Cinq matchs dans la journée pour aller chercher le bouclier du tournoi ! Faites-vous plaisir et jouez les uns pour les autres !", [(475, 162), (500, 162), (485, 205)]),
        ('bulle', (40, 510, 410, 600), "J'ai fixé ! Vas-y Ayden !", [(65, 602), (90, 602), (75, 645)]),
        ('bulle', (40, 650, 410, 750), "ESSAI ! Super passe Léon !", [(340, 652), (365, 652), (380, 615)]),
        ('encadre', (40, 765, 410, 810), "MATCH 1 : VICTOIRE CONTRE CHAMBÉRY (JAUNE ET NOIR) !"),
        ('bulle', (455, 510, 830, 600), "Plaqué aux jambes !", [(480, 602), (505, 602), (490, 645)]),
        ('bulle', (455, 650, 830, 750), "Et deuxième victoire pour nous !", [(770, 652), (795, 652), (810, 615)]),
        ('encadre', (455, 765, 830, 810), "MATCH 2 : VICTOIRE CONTRE ALBERTVILLE (ROUGE ET BLANC) !"),
        ('bulle', (40, 845, 410, 950), "Deux sur deux ! Et on n'a presque pas fait d'en-avant !", [(65, 952), (90, 952), (75, 995)]),
        ('bulle', (40, 1020, 410, 1140), "Très bien les garçons ! Maintenant attention : le troisième match, c'est contre Rumilly !", [(340, 1022), (365, 1022), (380, 985)]),
        ('bulle', (455, 845, 830, 975), "Rumilly… C'est contre eux que je m'étais énervé en novembre. Aujourd'hui, on reste calmes quoi qu'il arrive !", [(480, 977), (505, 977), (490, 1020)]),
    ],
    26: [
        ('bulle', (40, 73, 830, 190), "Attention, il est costaud lui, venez m'aider au milieu !", [(65, 192), (90, 192), (75, 235)]),
        ('ono', (400, 395), "FIIIIIIIT !", 16),
        ('bulle', (40, 420, 410, 530), "Essai de Rumilly ! Victoire de Rumilly 3 essais à 2 !", [(65, 532), (90, 532), (75, 575)]),
        ('bulle', (40, 682, 410, 790), "Oh non… On a perdu contre Rumilly… C'est fini, on ne peut plus gagner le tournoi maintenant ?", [(65, 792), (90, 792), (75, 835)]),
        ('bulle', (40, 815, 410, 905), "Pourtant on s'était tellement entraînés…", [(340, 817), (365, 817), (380, 780)]),
        ('bulle', (455, 683, 830, 795), "Mais non, rien n'est fini ! Regardez le tableau : Rumilly a perdu contre Montmélian ce matin, et Montmélian a été accroché par Thonon !", [(480, 797), (505, 797), (490, 840)]),
        ('bulle', (455, 815, 830, 905), "Ça veut dire que si vous gagnez vos deux derniers matchs contre Aix-les-Bains puis contre Montmélian, vous finissez PREMIERS du tournoi au classement général !", [(770, 817), (795, 817), (810, 780)]),
        ('bulle', (40, 937, 410, 1100), "Les gars, écoutez ! On a perdu contre Rumilly, alors il faut comprendre POURQUOI tout de suite ! Papa, Julien, Kilian, qu'est-ce qu'on a mal fait sur leur dernier essai ?", [(65, 1102), (90, 1102), (75, 1145)]),
        ('bulle', (455, 935, 830, 1020), "Vous avez oublié notre point d'entraînement sur la défense en ligne : vous vous êtes mis à trois sur le même porteur au milieu, ce qui a laissé tout le côté ouvert !", [(480, 1022), (505, 1022), (490, 1065)]),
        ('bulle', (455, 1030, 830, 1095), "Chacun son joueur dans la ligne : un qui plaque aux jambes, et les autres qui gardent la largeur des 20 mètres !", [(770, 1032), (795, 1032), (810, 995)]),
        ('bulle', (455, 1100, 830, 1163), "Compris ! Merci Rumilly de nous avoir montré notre erreur : contre Aix-les-Bains et Montmélian, notre ligne ne se déformera plus !", [(480, 1165), (505, 1165), (490, 1163)]),
    ],
    27: [
        ('bulle', (40, 42, 410, 150), "Ayden l'a pris au centre ! Ne vous resserrez pas, gardez vos postes sur la ligne !", [(65, 152), (90, 152), (75, 195)]),
        ('bulle', (455, 42, 830, 150), "Mince, tout est fermé sur les côtés !", [(480, 152), (505, 152), (490, 195)]),
        ('bulle', (40, 515, 410, 630), "ESSAI ! Ça marche ! Quand on corrige notre erreur du match d'avant, on est dix fois plus forts !", [(65, 632), (90, 632), (75, 675)]),
        ('encadre', (40, 760, 410, 815), "MATCH 4 : VICTOIRE CONTRE AIX-LES-BAINS (JAUNE ET NOIR) !"),
        ('voix', (455, 515, 830, 600), "DERNIER MATCH DÉCISIF POUR LE TROPHÉE U8 : RUGBY CLUB MOTTERAIN CONTRE MONTMÉLIAN !"),
        ('bulle', (40, 850, 410, 950), "C'est Montmélian… Ceux qui nous avaient battus au tout premier tournoi…", [(65, 952), (90, 952), (75, 995)]),
        ('bulle', (40, 1000, 410, 1115), "Ils ont toujours l'air aussi costauds dans leurs maillots Vert et Noir !", [(340, 1002), (365, 1002), (380, 965)]),
        ('bulle', (455, 850, 830, 1030), "Au premier tournoi, on était cinq joueurs qui couraient chacun dans leur coin, et moi je pleurais de colère. Aujourd'hui, on a appris de tous nos échecs de la saison. On joue ensemble, passes, soutien et défense en ligne !", [(480, 1032), (505, 1032), (490, 1075)]),
        ('bulle', (455, 1060, 830, 1130), "ALLEZ LE RCM !!", [(480, 1132), (505, 1132), (490, 1155)]),
    ],
    28: [
        ('encadre', (40, 40, 410, 180), "UN COMBAT MAGNIFIQUE À 5 CONTRE 5 ! CHAQUE ÉQUIPE REND COUP POUR COUP : 1 ESSAI PARTOUT, PUIS 2 ESSAIS PARTOUT !"),
        ('bulle', (455, 40, 830, 150), "Attention les garçons, c'est maintenant ! Montez en ligne comme on l'a corrigé après Rumilly !", [(480, 152), (505, 152), (490, 195)]),
        ('ono', (400, 315), "BAM !", 17),
        ('bulle', (40, 340, 410, 450), "Je l'ai en bas ! Gardez la ligne sur l'extérieur !", [(65, 452), (90, 452), (75, 495)]),
        ('ono', (110, 650), "TCHAC !", 14),
        ('ono', (300, 645), "FIIIIT !", 14),
        ('bulle', (40, 680, 410, 800), "Touche ! Ballon rendu au RCM et joué comme une pénalité ! Il reste une dernière action !", [(65, 802), (90, 802), (75, 845)]),
        ('bulle', (455, 632, 830, 745), "Dernière balle les gars ! En place le soutien !", [(480, 747), (505, 747), (490, 790)]),
        ('cri', (40, 900, 330, 1000), "VAS-Y LÉON !", 18),
    ],
    29: [
        ('bulle', (40, 76, 410, 180), "Bloquez Léon ! Il va essayer de passer tout seul comme en octobre !", [(65, 182), (90, 182), (75, 225)]),
        ('pensee', (455, 76, 830, 190), "Ils croient que je vais forcer tout seul… Mais j'ai appris de mes échecs !", [(475, 205, 9), (497, 223, 6), (515, 238, 4)]),
        ('bulle', (40, 402, 300, 505), "POUR VOUS LES COPAINS ! SOUTIEN !", [(65, 507), (90, 507), (120, 550)]),
        ('bulle', (310, 402, 560, 510), "Je l'ai Léon ! Tiens Milo, va marquer !", [(335, 512), (360, 512), (345, 555)]),
        ('bulle', (570, 402, 830, 510), "VAS-Y MILO, IL N'Y A PLUS PERSONNE !", [(595, 512), (620, 512), (605, 555)]),
        ('ono', (150, 900), "ESSAAAAI !", 16),
        ('ono', (400, 900), "FIIIIIIIIIIIT !", 14),
        ('bulle', (40, 950, 410, 1090), "Essai validé ! 1 point de plus ! Le Rugby Club Motterain bat Montmélian 3 à 2 !", [(65, 1092), (90, 1092), (75, 1135)]),
    ],
    30: [
        ('bulle', (42, 64, 410, 165), "Bravo le RCM… Votre dernière passe en soutien, on n'a rien pu faire !", [(67, 167), (92, 167), (77, 210)]),
        ('bulle', (42, 230, 410, 360), "Merci ! C'est grâce à vous au premier tournoi qu'on a appris à la travailler !", [(67, 362), (92, 362), (77, 400)]),
        ('bulle', (455, 64, 830, 170), "Champions du tournoi final ! Et vous savez ce qui est le plus beau ? Vous l'avez gagné APRÈS avoir perdu un match ce matin !", [(480, 172), (505, 172), (490, 210)]),
        ('bulle', (455, 190, 830, 330), "Parce qu'après Rumilly, au lieu de pleurer ou de s'énerver, on a corrigé notre défense en ligne !", [(480, 332), (505, 332), (490, 360)]),
        ('bulle', (455, 320, 830, 370), "VIVE LES U8 DU RCM !", [(480, 372), (505, 372), (490, 368)]),
        ('bulle', (42, 402, 410, 540), "Quelle saison… De la pluie d'automne à la neige de décembre jusqu'au soleil d'aujourd'hui, ils n'ont jamais rien lâché.", [(67, 542), (92, 542), (77, 585)]),
        ('bulle', (455, 402, 830, 530), "Papa… On va pouvoir raconter ça à Maman et à Alice ! Et lundi à l'école avec Ayden, on racontera tout à Baptiste !", [(480, 532), (505, 532), (490, 575)]),
        ('bulle', (455, 560, 830, 700), "Et qu'est-ce que tu leur diras si on te demande quel est le secret d'un vrai champion de rugby ?", [(770, 562), (795, 562), (810, 525)]),
        ('bulle', (42, 740, 410, 890), "Je leur dirai ta phrase, Papa : on apprend toujours de ses échecs, jamais de ses victoires !", [(67, 892), (92, 892), (120, 935)]),
        ('encadre', (42, 1020, 820, 1130), "FIN — LA FORCE DE L'ÉCHEC : « On apprend de ses échecs, c'est ce qui conduit à la victoire. »"),
    ],
}


def dst_path(page):
    stem = SRC[page].rsplit('/', 1)[-1].replace('-marvel.png', '')
    return f'Planches-dessin/Avec-texte/{stem}-avec-texte.png'


def _norm_txt(t):
    t = (t.replace('**', '').replace('«', '').replace('»', '')
         .replace('\u201c', '').replace('\u201d', '').replace('…', '...').replace('’', "'"))
    return re.sub(r'\s+', ' ', t).strip().lower()


def _ordre_lecture(r, pr):
    """r (après pr dans le dialogue) ne doit pas se lire avant pr."""
    below = r[1] >= pr[1] + 40
    if r[0] >= pr[2] - 8:      # colonne à droite : escalier toléré
        return r[1] >= pr[1] - 120
    if r[2] <= pr[0] + 8:      # colonne à gauche : rangée suivante
        return below
    return r[1] >= pr[1] - 16  # même colonne : jamais plus haut


def _point_estime(el):
    """Point locuteur estimé à la main (3e point de la queue) — simple prior.""" 
    if el[0] == 'bulle':
        return el[3][2]
    if el[0] == 'pensee':
        cx, cy, _ = el[3][-1]
        return (cx, cy)
    return None


def locuteurs_alignes(page, scen):
    """Locuteur scénario de chaque élément PAGES (alignement par texte)."""
    sc_els = [e for v in scen.get(page, []) for e in v['elements'] if e['kind'] != 'ono']
    out = []
    for el in PAGES[page]:
        if el[0] == 'ono':
            out.append('')
            continue
        n = _norm_txt(el[2])
        sp = ''
        for e in sc_els:
            en = _norm_txt(e['text'])
            if en == n or en.startswith(n[:60]) or n.startswith(en[:60]):
                sp = e['speaker']
                break
        out.append(PS.locuteur_reference(sp))
    return out


def _locuteur(el):
    """Point locuteur : pointe de la bulle vers la bouche du personnage qui parle."""
    if el[0] == 'bulle':
        return el[3][2]
    if el[0] == 'pensee':
        cx, cy, _ = el[3][-1]
        rx = (el[1][0] + el[1][2]) / 2
        ry = (el[1][1] + el[1][3]) / 2
        dx, dy = cx - rx, cy - ry
        n = max(1e-6, (dx * dx + dy * dy) ** 0.5)
        return (cx + dx / n * 26, cy + dy / n * 26)
    return None


def _snap_face(loc, faces, max_dist=55):
    """Ancre le locuteur présumé sur le visage dessiné le plus proche (si proche)."""
    if loc is None:
        return None, None
    lx, ly = loc
    best, bd = None, None
    for f in faces:
        dx = max(f[0] - lx, 0, lx - (f[0] + f[2]))
        dy = max(f[1] - ly, 0, ly - (f[1] + f[3]))
        dbox = (dx * dx + dy * dy) ** 0.5
        if dbox <= max_dist and (bd is None or dbox < bd):
            best, bd = f, dbox
    if best is not None:
        return (best[0] + best[2] / 2, best[1] + best[3] * 0.62), best
    return loc, None


def _frac_segment_rects(ax, ay, bx, by, rects):
    """Fraction du segment [A,B] passant à l'intérieur des rectangles."""
    dedans = 0
    for t in range(21):
        t /= 20
        px, py = ax + (bx - ax) * t, ay + (by - ay) * t
        if any(r[0] <= px <= r[2] and r[1] <= py <= r[3] for r in rects):
            dedans += 1
    return dedans / 21


def _t0_segment_rect(ax, ay, bx, by, r):
    """Premier t (0..1) où le segment entre dans le rectangle, sinon None."""
    for t in range(41):
        t /= 40
        px, py = ax + (bx - ax) * t, ay + (by - ay) * t
        if r[0] <= px <= r[2] and r[1] <= py <= r[3]:
            return t
    return None


def _dist_segment_box(ax, ay, bx, by, box):
    """Distance minimale entre le segment [A,B] et une boîte (0 si traversée)."""
    best = 1e9
    for t in range(11):
        t /= 10
        px, py = ax + (bx - ax) * t, ay + (by - ay) * t
        dx = max(box[0] - px, 0, px - (box[0] + box[2]))
        dy = max(box[1] - py, 0, py - (box[1] + box[3]))
        best = min(best, (dx * dx + dy * dy) ** 0.5)
    return best


def _queue_auto(rect, locuteur, face=None, autres=None, bulles=None, max_long=400):
    """Queue de bulle : base sur le bord de la bulle dont la ligne vers le
    locuteur évite le mieux les autres têtes ; pointe arrêtée juste avant la
    tête visée (queues longues autorisées : la pointe doit ATTEINDRE la tête)."""
    x1, y1, x2, y2 = rect
    lx, ly = locuteur
    if face is not None:
        tx, ty = face[0] + face[2] / 2, face[1] + face[3] / 2
    else:
        tx, ty = lx, ly
    cands = []
    for t in (0.15, 0.3, 0.5, 0.7, 0.85):
        cands.append((min(max(tx, x1 + 14), x2 - 14) if t == 0.5 else x1 + t * (x2 - x1), y1, 'h'))
        cands.append((min(max(tx, x1 + 14), x2 - 14) if t == 0.5 else x1 + t * (x2 - x1), y2, 'h'))
        cands.append((x1, min(max(ty, y1 + 14), y2 - 14) if t == 0.5 else y1 + t * (y2 - y1), 'v'))
        cands.append((x2, min(max(ty, y1 + 14), y2 - 14) if t == 0.5 else y1 + t * (y2 - y1), 'v'))
    best = None
    for ax, ay, ori in cands:
        ax = min(max(ax, x1 + 6), x2 - 6)
        ay = min(max(ay, y1 + 6), y2 - 6)
        d = ((tx - ax) ** 2 + (ty - ay) ** 2) ** 0.5
        if d < 14:
            continue
        clearance = 1e9
        for b in (autres or []):
            clearance = min(clearance, _dist_segment_box(ax, ay, tx, ty, b))
        score = (0 if clearance > 26 else 26 - clearance) * 3 + d / 200
        # interdit : une base dont la queue retraverse sa propre bulle
        for tt in (0.2, 0.4, 0.6, 0.8):
            px, py = ax + (tx - ax) * tt, ay + (ty - ay) * tt
            if x1 + 2 <= px <= x2 - 2 and y1 + 2 <= py <= y2 - 2:
                score += 500
                break
        if bulles:
            score += 200 * _frac_segment_rects(ax, ay, tx, ty, bulles)
        if best is None or score < best[0]:
            best = (score, ax, ay, ori, d)
    if best is None:
        return None
    _, ax, ay, ori, d = best
    tip_d = min(d - 8, max_long)
    if tip_d < 10:
        tip_d = max(6, d - 4)
    ux, uy = (tx - ax) / max(d, 1e-6), (ty - ay) / max(d, 1e-6)
    tip = (ax + ux * tip_d, ay + uy * tip_d)
    # la pointe ne doit jamais pénétrer une autre bulle : on s'arrête avant
    if bulles:
        for r in bulles:
            t0 = _t0_segment_rect(ax, ay, tx, ty, r)
            if t0 is not None:
                coupe = t0 * d - 8
                if coupe < tip_d:
                    tip_d = max(12, coupe)
                    tip = (ax + ux * tip_d, ay + uy * tip_d)
        # garde-fou : si la pointe est encore dans une bulle, on recule par pas
        for _ in range(40):
            if not any(r[0] < tip[0] < r[2] and r[1] < tip[1] < r[3] for r in bulles):
                break
            tip_d -= 4
            if tip_d <= 12:
                tip_d = 12
                break
            tip = (ax + ux * tip_d, ay + uy * tip_d)
    if ori == 'h':
        base = [(ax - 13, ay), (ax + 13, ay)]
    else:
        base = [(ax, ay - 13), (ax, ay + 13)]
    return [base[0], base[1], tip]


# --- locuteur nommé dans le texte (plus de queue pointée) ----------------
_RENOMMAGES = {
    "Voix hors-champ depuis l'étage": 'Maman',
    "Voix d'Alice hors-champ": 'Alice',
    'Haut-parleur du stade': 'Haut-parleur',
    'Les 20 joueurs en chœur': 'Les 20 joueurs',
    'adversaire-vert': 'Adversaire vert',
    'adversaire-rumilly': 'Adversaire de Rumilly',
}
_KINDS_DIAL = ('bulle', 'pensee', 'cri', 'voix')


def _nom_locuteur(spk):
    """Nom affichable du locuteur (voix off ramenée au personnage)."""
    return _RENOMMAGES.get(spk, spk)


def _texte_affiche(el, spk):
    """Texte rendu : dialogues préfixés « Nom: "…" », narratifs tels quels."""
    if el[0] in _KINDS_DIAL and spk:
        return f'{_nom_locuteur(spk)}: "{el[2]}"'
    return el[2]


def _dbg(page, label, placements):
    print(f'DBG p{page:02d} {label}: '
          + ' '.join(f'{i}:{tuple(round(v) for v in q["rect"])}'
                     for i, q in enumerate(placements) if q), file=sys.stderr)


def _zones_persos(pers):
    """Silhouettes présumées sous chaque tête détectée : torse et jambes,
    maillot compris (la peau seule est couverte par les blobs). Un personnage
    habillé n'apparaît pas dans le masque de peau mais reste à ne pas cacher."""
    zones = []
    for p in pers:
        if p['tete'] is None:
            continue
        z = PS.zone_tete(p)
        if z is None:
            continue
        x, y, w, h = z
        zw, zh = 2.0 * w, 2.5 * h
        zones.append((x - 0.5 * w, y + 0.5 * h, zw, zh, zw * zh))
    return zones


def _place_ono(ctx, cx, cy):
    """Décale une onomatopée pour éviter têtes, corps et bulles déjà posées.
    Fenêtre locale d'abord, puis balayage de toute la vignette en dernier
    recours (avec préférence pour rester près de la position d'origine)."""
    def cout(bx, by, eloigne):
        box = (bx - 48, by - 20, bx + 48, by + 20)
        surf = (box[2] - box[0]) * (box[3] - box[1])
        c_t = c_p = c_b = 0.0
        for f in ctx['tetes']:
            inter = _inter_box(box, f)
            if inter:
                c_t = max(c_t, inter / min(surf, f[2] * f[3]))
        for f in ctx['corps']:
            inter = _inter_box(box, f)
            if inter:
                c_b = max(c_b, inter / min(surf, f[4]))
        for r in ctx['placed']:
            inter = _inter_box(box, (r[0], r[1], r[2] - r[0], r[3] - r[1]))
            if inter:
                c_p = max(c_p, inter / surf)
        if not eloigne:                    # fenêtre locale : compromis distance/propreté
            return 3 * c_t + c_b + c_p + (abs(bx - cx) + abs(by - cy)) / 300
        # balayage large : la propreté domine largement la distance
        return 40 * c_t + 10 * c_p + c_b + ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5 / 800

    best, best_c = (cx, cy), None
    for dy in range(-150, 151, 12):
        for dx in range(-150, 151, 12):
            c = cout(cx + dx, cy + dy, False)
            if best_c is None or c < best_c:
                best, best_c = (cx + dx, cy + dy), c
    if best_c is None or best_c > 0.05:          # conflit résiduel -> vignette entière
        for pn in ctx['panels']:
            if pn[0] - 40 <= cx <= pn[2] + 40 and pn[1] - 40 <= cy <= pn[3] + 40:
                for by in range(int(pn[1]) + 22, int(pn[3]) - 22, 12):
                    for bx in range(int(pn[0]) + 30, int(pn[2]) - 30, 12):
                        c = cout(bx, by, True)
                        if c < best_c:
                            best, best_c = (bx, by), c
                break
    return best


def _inter_box(a, b):
    ix = max(0, min(a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[1] + b[3]) - max(a[1], b[1]))
    return ix * iy


def apply_page(page, ctx, manifest):
    """Lettrage d'une planche : résolution des locuteurs, placement, rendu."""
    L = Lettrage(SRC[page], dst_path(page))
    els = PAGES[page]
    panels = ctx['panels']
    pers = ctx['personnes']
    speakers = ctx['speakers']
    txts = [_texte_affiche(el, speakers[i] if i < len(speakers) else '')
            for i, el in enumerate(els)]

    # panel de chaque élément (les onomatopées restent sans panel)
    pidx_of = {}
    for i, el in enumerate(els):
        if el[0] == 'ono':
            continue
        pidx_of[i] = P._panel_of(el[1], panels)[0]

    # résolution locuteur -> personne (têtes détectées + identités + présence scénario)
    priors = {i: _point_estime(el) for i, el in enumerate(els) if el[0] in ('bulle', 'pensee')}
    a_res = [{'idx': i, 'panel': pidx_of[i], 'speaker': speakers[i]}
             for i, el in enumerate(els)
             if el[0] in ('bulle', 'pensee') and speakers[i]]
    resol = PS.resoudre_page(a_res, pers, panels, ctx['vigs'], priors)

    # obstacles : têtes (interdites, marge haute renforcée pour cheveux/front)
    # et zones de peau (corps, mains, visages partiels : fortement pénalisées)
    tetes = []
    for pr in pers:
        z = PS.zone_tete(pr)
        if z is None:
            continue
        x, y, w, h = z
        tetes.append((x - 0.15 * w, y - 0.15 * h, 1.3 * w, 1.3 * h))
    # visages probables non détectés par Haar : orphelins dont le blob de peau
    # a une forme de tête (carré, 22-90 px) -> protégés comme une tête
    for pr in pers:
        if pr['tete'] is not None or not pr.get('corps'):
            continue
        bx, by, bw, bh = pr['corps']
        if 22 <= bw <= 90 and 22 <= bh <= 90 and 500 <= bw * bh \
                and 0.55 <= bw / bh <= 1.8:
            z = PS.zone_tete(pr)
            x, y, w, h = z
            tetes.append((x - 0.15 * w, y - 0.15 * h, 1.3 * w, 1.3 * h))
    corps = list(ctx.get('blobs') or [])   # zones de peau (avec aire réelle)
    persos = _zones_persos(pers)           # silhouettes (maillots compris)
    ctx['tetes'] = tetes
    ctx['corps'] = corps
    ctx['persos'] = persos

    # --- Phase 1 : placement glouton, élément par élément ------------------
    placements = [None] * len(els)
    panel_elems = {}
    prev_per_panel = {}
    placed = []
    # les onomatopées restent à leur place canonique : les bulles les évitent
    onos = [(el[1][0] - 48, el[1][1] - 18, el[1][0] + 48, el[1][1] + 18)
            for el in els if el[0] == 'ono']
    placed.extend(onos)
    for i, el in enumerate(els):
        if el[0] == 'ono':
            continue
        pidx = pidx_of[i]
        panel = panels[pidx]
        pr = resol.get(i)
        spk = PS.point_bouche(pr) if pr is not None else priors.get(i)
        rect, size, soft = P.placer(el[0], txts[i], el[1], tetes, placed, panel,
                                     speaker=spk, prev=prev_per_panel.get(pidx),
                                     bodies=corps, persos=persos)
        prev_per_panel[pidx] = rect
        placed.append(rect)
        placements[i] = {'rect': rect, 'size': size, 'soft': soft, 'panel': pidx,
                         'pers': pr, 'kind': el[0]}
        panel_elems.setdefault(pidx, []).append(i)

    if os.environ.get('ARENA_DEBUG'):
        _dbg(page, 'apres phase 1', placements)

    # --- Phase 1.5 : déblocage local (seule la bulle bloquée bouge) ---------
    import placer as _P
    _debloque = []
    for pidx, idxs in panel_elems.items():
        for k, i in enumerate(idxs):
            if els[i][0] not in ('bulle', 'pensee'):
                continue
            pr = placements[i]['pers']
            spk = PS.point_bouche(pr) if pr is not None else priors.get(i)
            if spk is None:
                continue
            obst = [placements[j]['rect'] for j, q in enumerate(placements)
                    if q and j != i] + list(onos)
            if _P._blocage_vers(placements[i]['rect'], spk, obst) <= 0.10:
                continue
            # chercher une position de la même bulle, queue dégagée
            panel = panels[pidx]
            rect0 = placements[i]['rect']
            prev_r = placements[idxs[k - 1]]['rect'] if k > 0 else None
            next_r = placements[idxs[k + 1]]['rect'] if k + 1 < len(idxs) else None
            best = None
            for dy in range(-100, 101, 10):
                for dx in range(-100, 101, 10):
                    cand = (rect0[0] + dx, rect0[1] + dy,
                            rect0[2] + dx, rect0[3] + dy)
                    if _P._inside_ratio(cand, panel) < 0.995:
                        continue
                    if not _P._face_ok(cand, tetes, 0.03):
                        continue
                    if any(_P._placed_overlap(cand, [o]) > 0.015 for o in obst):
                        continue
                    if _P._peau_overlap(cand, corps) > 0.30:
                        continue
                    if _P._peau_overlap(cand, persos) > 0.45:
                        continue
                    if prev_r is not None and not _ordre_lecture(cand, prev_r):
                        continue
                    if next_r is not None and not _ordre_lecture(next_r, cand):
                        continue
                    if _P._blocage_vers(cand, spk, obst) > 0.0:
                        continue
                    ec = ((dx * dx + dy * dy) ** 0.5
                          + 300 * _P._peau_overlap(cand, corps)
                          + 60 * _P._peau_overlap(cand, persos))
                    if best is None or ec < best[0]:
                        best = (ec, cand)
            if best is not None:
                placements[i]['rect'] = best[1]
                placements[i]['soft'] = False
                _debloque.append((page, pidx, i))

    if os.environ.get('ARENA_DEBUG'):
        _dbg(page, 'apres 1.5', placements)

    # --- Phase 2 : réparation (repli, recouvrement de peau, queue bloquée) --
    for pidx, idxs in panel_elems.items():
        trop_couvert = any(_P._peau_overlap(placements[i]['rect'], corps) > 0.30
                           for i in idxs if placements[i])
        queue_bloquee = False
        for i in idxs:
            pr = placements[i]['pers']
            spk = PS.point_bouche(pr) if pr is not None else priors.get(i)
            if spk is None:
                continue
            obst = [placements[j]['rect'] for j, q in enumerate(placements)
                    if q and j != i] + list(onos)
            if _P._blocage_vers(placements[i]['rect'], spk, obst) > 0.10:
                queue_bloquee = True
        if (not any(placements[i]['soft'] for i in idxs)
                and not trop_couvert and not queue_bloquee):
            continue
        panel = panels[pidx]
        els_p = []
        for i in idxs:
            pr = placements[i]['pers']
            els_p.append({'kind': els[i][0], 'text': txts[i],
                          'speaker': PS.point_bouche(pr) if pr is not None else priors.get(i)})
        placed_other = [placements[j]['rect'] for j, q in enumerate(placements)
                        if q and q['panel'] != pidx] + list(onos)
        res = P.reparer_panel(panel, els_p, tetes, placed_other, bodies=corps,
                              persos=persos)
        if res:
            rects, size = res
            print(f'  page {page:02d} : réparation vignette {pidx} '
                  f'({len(idxs)} éléments, taille {size})', file=sys.stderr)
            for i, r in zip(idxs, rects):
                placements[i] = {'rect': r, 'size': size, 'soft': False, 'panel': pidx,
                                 'pers': placements[i]['pers'],
                                 'queue': placements[i].get('queue'),
                                 'kind': placements[i].get('kind', els[i][0])}

    if os.environ.get('ARENA_DEBUG'):
        _dbg(page, 'apres 2', placements)

    # --- Phase 2.7 : sécurité têtes (dernier filet anti-visage couvert) ----
    # l'audit signale une tête couverte dès 10% de la boîte BRUTE ; la
    # génération padde les boîtes (1.3x) : 5% paddé ≈ 8.4% brut -> marge.
    # Toute bulle qui couvre encore une tête tente un décalage local strict.
    for pidx, idxs in panel_elems.items():
        for k, i in enumerate(idxs):
            if els[i][0] not in ('bulle', 'pensee') or not placements[i]:
                continue
            if _P._face_ok(placements[i]['rect'], tetes, 0.05):
                continue
            panel = panels[pidx]
            rect0 = placements[i]['rect']
            prev_r = placements[idxs[k - 1]]['rect'] if k > 0 else None
            next_r = placements[idxs[k + 1]]['rect'] if k + 1 < len(idxs) else None
            obst = [placements[j]['rect'] for j, q in enumerate(placements)
                    if q and j != i] + list(onos)
            best = None
            for dy in range(-120, 121, 10):
                for dx in range(-120, 121, 10):
                    cand = (rect0[0] + dx, rect0[1] + dy,
                            rect0[2] + dx, rect0[3] + dy)
                    if _P._inside_ratio(cand, panel) < 0.995:
                        continue
                    if not _P._face_ok(cand, tetes, 0.03):
                        continue
                    if any(_P._placed_overlap(cand, [o]) > 0.015 for o in obst):
                        continue
                    if _P._peau_overlap(cand, corps) > 0.30:
                        continue
                    if _P._peau_overlap(cand, persos) > 0.45:
                        continue
                    if prev_r is not None and not _ordre_lecture(cand, prev_r):
                        continue
                    if next_r is not None and not _ordre_lecture(next_r, cand):
                        continue
                    ec = ((dx * dx + dy * dy) ** 0.5
                          + 300 * _P._peau_overlap(cand, corps)
                          + 60 * _P._peau_overlap(cand, persos))
                    if best is None or ec < best[0]:
                        best = (ec, cand)
            if best is not None:
                placements[i]['rect'] = best[1]
                placements[i]['soft'] = False
                print(f'  page {page:02d} : sécurité tête, élément {i} décalé '
                      f'({best[1][0] - rect0[0]:+d},{best[1][1] - rect0[1]:+d})',
                      file=sys.stderr)

    if os.environ.get('ARENA_DEBUG'):
        _dbg(page, 'apres 2.7', placements)

    # --- Phase 2.8 : sécurité chevauchements (aucune boîte sur une autre) --
    # un repli peut laisser deux boîtes superposées : on décale localement
    # celle qui gêne, avec les mêmes contraintes dures que la phase 2.7.
    for pidx, idxs in panel_elems.items():
        for k, i in enumerate(idxs):
            if not placements[i]:
                continue
            rect0 = placements[i]['rect']
            obst = [placements[j]['rect'] for j, q in enumerate(placements)
                    if q and j != i] + list(onos)
            if not any(_P._placed_overlap(rect0, [o]) > 0.015 for o in obst):
                continue
            panel = panels[pidx]
            prev_r = placements[idxs[k - 1]]['rect'] if k > 0 else None
            next_r = placements[idxs[k + 1]]['rect'] if k + 1 < len(idxs) else None
            best = None
            for dy in range(-140, 141, 10):
                for dx in range(-140, 141, 10):
                    cand = (rect0[0] + dx, rect0[1] + dy,
                            rect0[2] + dx, rect0[3] + dy)
                    if _P._inside_ratio(cand, panel) < 0.995:
                        continue
                    if not _P._face_ok(cand, tetes, 0.03):
                        continue
                    if any(_P._placed_overlap(cand, [o]) > 0.015 for o in obst):
                        continue
                    if _P._peau_overlap(cand, corps) > 0.30:
                        continue
                    if _P._peau_overlap(cand, persos) > 0.45:
                        continue
                    if prev_r is not None and not _ordre_lecture(cand, prev_r):
                        continue
                    if next_r is not None and not _ordre_lecture(next_r, cand):
                        continue
                    ec = ((dx * dx + dy * dy) ** 0.5
                          + 300 * _P._peau_overlap(cand, corps)
                          + 60 * _P._peau_overlap(cand, persos))
                    if best is None or ec < best[0]:
                        best = (ec, cand)
            if best is not None:
                placements[i]['rect'] = best[1]
                placements[i]['soft'] = False
                print(f'  page {page:02d} : sécurité chevauchement, élément {i} décalé '
                      f'({best[1][0] - rect0[0]:+d},{best[1][1] - rect0[1]:+d})',
                      file=sys.stderr)

    if os.environ.get('ARENA_DEBUG'):
        _dbg(page, 'apres 2.8', placements)

    # --- Phase 2.5 : ordre de lecture au sein de chaque vignette -----------
    # deux bulles inversées spatialement -> on échange leurs textes si chacun
    # tient dans le rectangle de l'autre (le préfixe suit le locuteur du texte)
    def _taille_qui_tient(texte, kind, r, s_max):
        w, h = r[2] - r[0], r[3] - r[1]
        for taille in range(min(s_max, 13), 7, -1):   # plancher 8 (textfit)
            if P.mesurer(texte, w, taille, *P.PADS[kind][:2]) <= h:
                return taille
        return None

    def _echange_possible(ia, ib):
        ea, eb = els[ia], els[ib]
        if ea[0] != eb[0] or ea[0] not in ('bulle', 'pensee'):
            return False
        ra, rb = placements[ia]['rect'], placements[ib]['rect']
        return (_taille_qui_tient(txts[ia], ea[0], rb, 13) is not None
                and _taille_qui_tient(txts[ib], eb[0], ra, 13) is not None)

    for pidx, idxs in panel_elems.items():
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                ia, ib = idxs[a], idxs[b]
                ra, rb = placements[ia]['rect'], placements[ib]['rect']
                if not _ordre_lecture(rb, ra) and _echange_possible(ia, ib):
                    placements[ia]['rect'], placements[ib]['rect'] = rb, ra
                    placements[ia]['size'] = _taille_qui_tient(txts[ia], els[ia][0], rb, 13)
                    placements[ib]['size'] = _taille_qui_tient(txts[ib], els[ib][0], ra, 13)
                    print(f'  page {page:02d} : ordre rétabli dans la vignette {pidx} '
                          f'(éléments {ia} et {ib} échangés)', file=sys.stderr)

    if os.environ.get('ARENA_DEBUG'):
        _dbg(page, 'apres 2.5 (final)', placements)

    # --- Phase 3 : rendu (boîtes blanches et encadrés, puis onomatopées) ---
    for i, el in enumerate(els):
        p = placements[i]
        if p is None:
            continue
        rect, size, kind = p['rect'], p['size'], el[0]
        if kind == 'encadre':
            L.encadre(rect, txts[i], maximum=size)
        elif kind == 'bulle':
            L.bulle(rect, txts[i], maximum=size)
        elif kind == 'pensee':
            L.pensee(rect, txts[i], maximum=size)
        elif kind == 'voix':
            L.voix_off(rect, txts[i], maximum=size)
        elif kind == 'cri':
            L.cri(rect, txts[i], maximum=size)
    for i, el in enumerate(els):
        if el[0] != 'ono':
            continue
        # obstacles à jour : bulles posées (après réparation) + autres onomatopées
        ctx['placed'] = [q['rect'] for q in placements if q and q.get('kind') != 'ono']
        for j, e2 in enumerate(els):
            if e2[0] != 'ono' or j == i:
                continue
            if placements[j] is not None:
                ctx['placed'].append(tuple(placements[j]['rect']))
            else:
                ctx['placed'].append((e2[1][0] - 48, e2[1][1] - 18,
                                      e2[1][0] + 48, e2[1][1] + 18))
        bx, by = _place_ono(ctx, el[1][0], el[1][1])
        L.onomatopee((bx, by), el[2], size=el[3] if len(el) > 3 else 15)
        box = (bx - 48, by - 18, bx + 48, by + 18)
        ctx['placed'].append(box)
        placements[i] = {'rect': box, 'size': None, 'soft': False,
                         'panel': None, 'pers': None, 'kind': 'ono'}

    # --- manifeste enrichi (locuteur attendu + texte affiché) ---------------
    for i, el in enumerate(els):
        p = placements[i]
        manifest.append({'kind': el[0], 'rect': [round(v) for v in p['rect']],
                         'panel': p['panel'], 'size': p['size'],
                         'speaker': speakers[i] or None, 'texte': txts[i]})
    return L.save()


if __name__ == '__main__':
    import placer as P

    scen = PS.parse_scenario()
    panels_all = P.load_panels()
    all_manifests = {}
    for page in sorted(PAGES):
        base = np.asarray(Image.open(ROOT / SRC[page]).convert('RGB')
                          .resize((864, 1222), Image.LANCZOS))
        bgr = base[..., ::-1].copy()
        pers = PS.detecter_personnages(bgr)
        import cv2
        pm = PS.masque_peau(bgr)
        n_cc, _, stats_cc, _ = cv2.connectedComponentsWithStats(pm, 8)
        blobs = [(int(stats_cc[i, 0]), int(stats_cc[i, 1]),
                  int(stats_cc[i, 2]), int(stats_cc[i, 3]), int(stats_cc[i, 4]))
                 for i in range(1, n_cc) if stats_cc[i, 4] >= 450]
        panels_p = panels_all.get(page, [(20, 20, 844, 1202)])
        vigs = scen.get(page, [])
        if len(vigs) != len(panels_p):
            pres = set()
            for v in vigs:
                pres |= v['presence']
            vigs = [{'hints': {}, 'presence': pres,
                     'match': any(v['match'] for v in vigs)}] * len(panels_p)
        ctx = {'personnes': pers, 'placed': [], 'panels': panels_p, 'vigs': vigs,
               'speakers': locuteurs_alignes(page, scen), 'blobs': blobs}
        manifest = []
        out = apply_page(page, ctx, manifest)
        all_manifests[str(page)] = manifest
        print(f'OK page {page:02d} -> {out} ({len(manifest)} éléments, {len(pers)} personnes)')

    import json
    mf = ROOT / 'Planches-dessin/validation/lettrage-manifest.json'
    mf.write_text(json.dumps({'trame': [864, 1222], 'pages': all_manifests},
                             ensure_ascii=False, indent=1))
    print('Manifeste :', mf)
