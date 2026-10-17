# Restylage comics — prompt maître et contrôle

## État

Les rendus 01–10 du premier lot ne sont PAS validés : incohérences de style et dérives des visages/cheveux signalées par l'utilisateur. Ne pas les prendre comme références et ne pas poursuivre le lot sur cette base.

## Références à joindre réellement à chaque appel

1. SOURCE : planche originale, avant le premier lot de restylage. Ne pas restyliser une génération déjà déformée. Les originaux du premier lot sont récupérables dans Git au commit e0416a5462491acd7dcde78e506983aa526f0f40, dossier Planches-dessin.
2. STYLE : couverture fournie par l'utilisateur, Planches-dessin/00-couverture-marvel.png. Toujours le même fichier. Ne jamais substituer une autre planche générée.
3. IDENTITÉS : portraits `personnages/<Prénom> réel.jpg` des personnages présents, avec association explicite nom/fichier/rôle dans chaque case. Joindre uniquement les portraits pertinents. Ne pas déduire le nom d'un personnage de sa seule position.

L'outil accepte dix images maximum : une source + une couverture + huit portraits au maximum. Si l'identification d'une silhouette est ambiguë, résoudre cette ambiguïté avant génération.

## Prompt maître à transmettre

Tu effectues une ÉDITION DE STYLE d'une planche existante, pas une nouvelle interprétation de l'histoire. Produis une seule planche correspondant exactement à SOURCE. STYLE est l'unique référence de langage graphique. IDENTITÉS contient les références des personnes, pas des compositions à recopier.

### Hiérarchie non négociable

- SOURCE fixe le nombre et l'ordre des cases, leur géométrie, les cadrages, le nombre de personnes, leurs positions, poses, regards, expressions, accessoires, décors, vêtements et couleurs locales.
- IDENTITÉS fixe la morphologie de chaque personne : silhouette du visage, implantation et coupe des cheveux, nez, yeux, mâchoire, oreilles, pilosité, âge et teint. Ne pas remplacer ces personnes par des archétypes de héros.
- STYLE fixe uniquement la manière de dessiner et de mettre en couleur. Ne pas copier ses poses, sa disposition des personnages, ses tenues, son titre ou son éclairage nocturne dans SOURCE.
- Aucun transfert d'identité entre deux personnages. Aucun remplacement d'un enfant par un autre. Aucun embellissement, vieillissement ou changement d'origine apparente.

### Style unique : reproduire la couverture, pas un mélange de styles

Même famille de contours noirs dessinés à la plume, épaisseur modulée et détails intérieurs fins. Même modelé dessiné des visages : volumes construits par ombres encrées, hachures fines directionnelles et transitions colorées maîtrisées. Même traitement des yeux, nez, bouches, oreilles et mèches que la couverture. Même niveau de simplification anatomique et de détail des tissus. Même trame d'impression fine et discrète ; pas de points grossiers sur les visages. Même logique de couleurs locales et de reflets, sans modifier la pigmentation ou les vêtements.

Rendu entièrement illustré et encré. Ni photo filtrée, ni photoréalisme résiduel, ni manga, ni cartoon, ni peinture numérique floue, ni rendu 3D. Ne pas mélanger ces traitements entre cases, personnages ou arrière-plans. Adapter la direction de la lumière à SOURCE sans inventer une nouvelle ambiance.

### Verrouillage des personnages

Appliquer seulement les entrées correspondant aux personnes réellement présentes, avec leurs portraits joints :

- Léon : 6 ans ; cheveux châtains clairs, pics relevés sur le dessus ; yeux marron. Garder l'implantation, la longueur et le visage du portrait. Ne pas brunir, blondir ou lisser les pics.
- Lyssandro : 6–7 ans ; cheveux châtains mi-longs, mèche souple sur le front vers la droite ; yeux verts/noisette clairs. Ne pas raccourcir en coupe d'Ayden.
- Ayden : 6–7 ans ; cheveux blonds/châtains clairs courts vers l'avant ; yeux foncés. Ne pas foncer en brun ni ajouter les pics de Léon.
- Nolann : 6–7 ans ; cheveux bruns très courts, petite frange courte ; teint mat/ensoleillé. Ne pas éclaircir sa peau ou ses cheveux.
- Milo : 6–7 ans ; cheveux châtains lisses, frange sur le front. Ne pas ajouter de pics ni de boucles.
- Flavien : adulte ; cheveux bruns courts avec mouvement sur le dessus ; barbe de trois jours/bouc finement taillé. Ne pas le grisonner ni lui donner la barbe de Julien ou Kilian.
- Julien : adulte au gabarit solide ; cheveux courts poivre et sel, moustache et bouc gris/blancs. Ne pas rajeunir ni brunir ses cheveux ou sa barbe.
- Kilian : adulte ; cheveux courts roux/blond vénitien, barbe rousse fournie. Ne pas changer le roux en brun ou blond neutre.

Les formulations ci-dessus complètent les portraits ; elles ne les remplacent pas. Conserver la carnation propre à CHAQUE portrait et les proportions faciales distinctives. Conserver les expressions de SOURCE, sans imposer le sourire du portrait.

### Vêtements, composition et texte

Ne changer aucune couleur de vêtement, aucun motif ni accessoire. RCM : rouge, bleu et blanc ; respecter précisément l'emplacement des bandes et manches de SOURCE. Conserver les tenues civiles lorsqu'elles sont présentes. Ne pas ajouter de cape, costume, muscles de superhéros ou accessoire absent.

Aucun ajout, suppression, fusion ou permutation de case ou de personne. Ne pas ajouter de bulles, de légendes, de titre ou de signature. Conserver le texte et les logos existants sans les réinventer. Garder les marges et le rapport largeur/hauteur de SOURCE.

Avant de finaliser, comparer chaque case à SOURCE, chaque personne à son portrait et le traitement graphique à STYLE. Une dérive de teint, cheveux, visage ou tenue n'est pas une variation autorisée.

## Annexe obligatoire propre à chaque appel

Renseigner AVANT d'envoyer le prompt (ne pas envoyer des champs vides) :

- fichier SOURCE et fichier STYLE ;
- liste ordonnée des portraits joints et leur nom ;
- pour chaque case : personnages identifiés et position, coupe/couleur des cheveux, teint et tenue à conserver ;
- éventuelles zones illisibles ou identités incertaines : résoudre avant génération.

## Procédure de validation

1. Repartir des originaux, jamais des dix rendus contestés.
2. Préparer une seule planche témoin et son annexe ; conserver le résultat comme candidat, sans écraser l'original.
3. Contrôler côte à côte : source/candidat pour le contenu, portraits/candidat pour les identités, couverture/candidat pour le style.
4. Rejeter si une case diffère de langage graphique, si une identité change, si les cheveux, le teint ou les couleurs de tenue dérivent. Un bon rendu global ne compense pas une erreur locale.
5. Faire valider le témoin par l'utilisateur avant tout nouveau lot. Cette validation ne dispense pas de contrôler chaque planche suivante.
6. Ne remplacer les fichiers de livraison qu'après validation. Corriger localement un défaut plutôt que régénérer toute une page déjà conforme lorsque c'est possible.

## Limites à ne pas masquer

Un prompt ne verrouille ni une identité ni le rendu pixel à pixel. L'outil disponible n'expose pas de verrouillage de seed, de modèle, de poids de style ou de contrôle structurel strict. Les textes et petits logos peuvent être déformés. Si les sorties ne passent pas le contrôle, ne pas les annoncer comme fidèles : une retouche locale ou un travail d'encrage manuel peut être nécessaire. Ne pas promettre une homogénéité parfaite sur la seule base de ces instructions.
