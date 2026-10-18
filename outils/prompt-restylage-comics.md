# Décision utilisateur prioritaire — couverture canonique (2026-10-18)

**Cette décision remplace les anciennes décisions ci-dessous :** `Planches-dessin/00-couverture-marvel.png` fixe désormais **STYLE ET IDENTITÉS**. Le témoin V2 n’est plus une référence applicable. Les passages historiques contradictoires ne doivent pas être transmis comme instructions courantes.

Joindre réellement la couverture et les recadrages nominatifs pertinents dans `Planches-dessin/validation/revue-couverture/`. Le scénario fixe les acteurs et leurs actions ; les planches `planches/*realisme-sans-texte.png` fixent la mise en scène, mais ne peuvent imposer une carnation/coiffure erronée contre la couverture. Nolann : teint mat de la couverture, cheveux bruns très courts avec petite frange, jamais arbitrairement assombri ou rendu chauve. Contrôler toutes les surfaces de peau. Flavien brun, Julien gris avec moustache/bouc, Kilian roux : ne pas les permuter.

Appliquer un seul langage de dessin, celui de la couverture. Ne pas remplacer des identités précises par des enfants génériques. Ne pas copier les poses, expressions souriantes, titres, lumière ou composition de la couverture. Rejeter les décors, marquages ou signatures inventés ; intégrer uniquement les zones correctes avec protections explicites. Une génération n’est pas une validation. Suivi courant : `Planches-dessin/validation/REVUE-COUVERTURE.md` et son inventaire JSON.

---

## Instructions et décisions historiques (subordonnées à la décision ci-dessus)

# Restylage comics — prompt maître V2 : dessin intégral, sans semi-réalisme

## État

La planche témoin `validation/01-la-legende-des-u6-temoin.png` est également REJETÉE : rendu trop semi-réaliste. Ne pas la réutiliser comme référence.

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
- IDENTITÉS, uniquement après association vérifiée et sans contredire les caractéristiques de SOURCE, précise la morphologie de chaque personne : silhouette du visage, implantation et coupe des cheveux, nez, yeux, mâchoire, oreilles, pilosité, âge et teint. Ne pas remplacer ces personnes par des archétypes de héros.
- STYLE fixe uniquement la manière de dessiner et de mettre en couleur. Ne pas copier ses poses, sa disposition des personnages, ses tenues, son titre ou son éclairage nocturne dans SOURCE.
- Aucun transfert d'identité entre deux personnages. Aucun remplacement d'un enfant par un autre. Aucun embellissement, vieillissement ou changement d'origine apparente.

### Contrat graphique unique — à transmettre sans reformulation à chaque appel

DESSIN COMICS INTÉGRAL. Ce n'est ni une photographie stylisée, ni un portrait réaliste auquel on ajoute des contours, ni un compromis photo/BD. Reconstruire chaque surface par des formes dessinées, de l'encre et des aplats. La ressemblance vient des proportions et caractéristiques distinctives, PAS de textures photographiques. Les photographies d'identité ne donnent AUCUNE instruction de rendu.

1. ENCRAGE : contours noirs francs, modulés, continus et lisibles ; contours extérieurs plus forts que les détails intérieurs. Dessiner les traits du visage, les mains, les vêtements et les décors avec la même famille de traits. Ni contours extraits d'une photo, ni effet de seuil, ni contours vectoriels uniformes.
2. VISAGES : plans graphiques clairement construits. Forme de l'œil, paupières, nez, lèvres et oreilles exprimée par des lignes et des masses d'ombre choisies. Pas de peau lissée à l'aérographe, pores, photographie recolorée, reflet humide de portrait studio ou modelé 3D. Ne pas exagérer les yeux, mâchoires ou muscles ; préserver les proportions propres à chaque personne.
3. OMBRES : masses d'encre aux bords nets et ombres colorées découpées. Pour chaque matière, un aplat local dominant, une ombre principale et un accent lumineux éventuel. Les hachures dessinent les volumes là où nécessaire ; elles ne servent pas à masquer une photo. Ne pas compter la trame parmi ces niveaux de couleur.
4. COULEURS : aplats propres et cohérents avec les couleurs locales originales. Rouge reste rouge, bleu reste bleu, blanc reste blanc ; préserver la pigmentation de chaque personne. Les ombres ne changent pas la carnation ou la couleur des cheveux. Pas de dégradés photographiques sur les visages, pas de rendu huile, aquarelle ou peinture numérique douce.
5. CHEVEUX ET BARBES : même silhouette, implantation, longueur et couleur que SOURCE. Dessiner en mèches groupées avec noirs et réserves claires ; pas de fibres photographiques, pas de coiffure substituée, pas de pics ajoutés ou supprimés. Les zones grises ou rousses restent grises ou rousses.
6. MATIÈRES ET DÉCORS : plis indiqués par lignes et masses encrées. Pelouse, arbres, ciel, ballon et stade entièrement dessinés, jamais un fond photo derrière des personnages dessinés. Pas de profondeur de champ photographique, de bokeh, de flou d'objectif ou de texture photo résiduelle.
7. TRAME : fine trame d'impression discrète et uniforme, subordonnée au dessin. Aucun filtre de points appliqué sur une photo. Même échelle visuelle de trame sur l'ensemble de la page.
8. CONTINUITÉ : même encreur et même coloriste supposés pour toutes les cases ET toutes les pages. Conserver exactement cette grammaire graphique dans les gros plans, plans de groupe et arrière-plans. Une scène triste, pluvieuse ou nocturne modifie la lumière et l'expression, jamais le style de dessin. Ne jamais choisir un style différent selon le sujet ou le cadrage.

STYLE reste la couverture fournie : prendre sa netteté d'encrage, ses ombres graphiques et son caractère de comics imprimé, PAS un traitement photographique de ses volumes. Ne pas reprendre sa mise en scène, ses costumes ou son titre. Si une reproduction littérale des dégradés de la couverture conduit à un visage semi-réaliste, privilégier le dessin encré et les ombres découpées demandés ici.

EXCLUSIONS ABSOLUES DE RENDU : semi-réalisme, photoréalisme, photo peinte, photo filtrée, photomontage, posterisation, peau aérographiée, sculpture 3D, éclairage de rendu 3D, peinture numérique douce, manga, cartoon caricatural. Ne pas confondre simplification graphique et modification de l'identité.

### Verrouillage des personnes — résoudre les contradictions avant l'appel

SOURCE fixe l'identité déjà représentée, les coiffures et leurs couleurs, les teints et les expressions. Ne pas remplacer une personne de SOURCE par une autre à cause d'un nom de fichier. Les descriptions de la charte et certains portraits nommés ont des divergences observées : ne pas transmettre aveuglément une liste nominative non vérifiée.

Préparer pour chaque personne une fiche vérifiée : case et position, forme du visage, coupe et implantation, couleur des cheveux, teint, âge apparent, pilosité, tenue. Si son portrait est associé sans ambiguïté, le joindre pour les proportions distinctives seulement. Sinon ne pas joindre un portrait susceptible de provoquer une substitution ; utiliser SOURCE et signaler l'ambiguïté avant de lancer la génération. Conserver l'expression de SOURCE, pas nécessairement celle du portrait.

Aucune permutation, aucun visage générique, aucun vieillissement, aucune modification de carnation. Le degré de stylisation doit être le même pour tous les visages, sans rendre les enfants ou les adultes plus photographiques que les autres.

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
4. Rejeter dès qu’un visage reste semi-réaliste, qu’un décor conserve un flou/une texture photographique, qu’une case diffère de langage graphique, si une identité change, si les cheveux, le teint ou les couleurs de tenue dérivent. Un bon rendu global ne compense pas une erreur locale.
5. La répétition de ce prompt ne garantit pas la continuité : inspecter réellement chaque résultat, sans annoncer une conformité automatique. Faire valider le témoin par l'utilisateur avant tout nouveau lot. Cette validation ne dispense pas de contrôler chaque planche suivante.
6. Ne remplacer les fichiers de livraison qu'après validation. Corriger localement un défaut plutôt que régénérer toute une page déjà conforme lorsque c'est possible.

## Limites à ne pas masquer

Un prompt ne verrouille ni une identité ni le rendu pixel à pixel. L'outil disponible n'expose pas de verrouillage de seed, de modèle, de poids de style ou de contrôle structurel strict. Les textes et petits logos peuvent être déformés. Si les sorties ne passent pas le contrôle, ne pas les annoncer comme fidèles : une retouche locale ou un travail d'encrage manuel peut être nécessaire. Ne pas promettre une homogénéité parfaite sur la seule base de ces instructions.

## Décision utilisateur et référence désormais applicable

L'utilisateur a validé le témoin V2 : `Planches-dessin/validation/01-la-legende-des-u6-temoin-v2.png`. Ce fichier remplace la couverture initiale comme autorité de STYLE pour les générations suivantes, couverture comprise. Sa validation porte sur le rendu choisi ; les erreurs d'expression signalées n'autorisent pas leur propagation. Les références à la couverture comme référence de style dans les sections historiques ci-dessus sont remplacées par cette décision.

Ne pas importer dans une autre planche les trois enfants qui courent, les médailles ou les expressions du témoin. Une telle contamination a été observée sur la sortie 09 et impose son rejet. Les photos ne sont pas jointes par défaut pour éviter le retour au rendu photographique ; la source originale conserve l'autorité sur les personnes.
