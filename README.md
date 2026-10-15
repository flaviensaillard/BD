# 🏉 LA FORCE DE L'ÉCHEC
> *« On apprend de ses échecs, c'est ce qui conduit à la victoire »*

Album de 30 pages en **style photographique réaliste**, créé pour **Léon** (6 ans), suivant la saison U8 du **Rugby Club Motterain (RCM)** à **La Motte-Servolex** et la vie à **Saint-Sulpice** en Savoie (saison septembre 2026 – juin 2027).

## Direction visuelle actuelle — 15 octobre 2026

- Le projet n'est plus réalisé en style comics : les nouvelles planches utilisent un rendu photographique réaliste et naturel.
- Utiliser comme références d'identité les photos des personnages dont le nom finit par **« réel »** (`personnages/* réel.jpg`). Les fichiers photo originaux ne sont pas modifiés.
- Ne pas utiliser les portraits PNG illustrés, les anciennes planches comics ni la couverture illustrée comme références de style pour les nouvelles scènes.
- Respecter le scénario et l'identité de chaque personnage. Les dialogues sont ajoutés manuellement dans une mise en page éditoriale discrète, sans bulles dessinées.
- La couverture existante est conservée telle quelle ; elle n'est pas à refaire.
- Les anciennes planches illustrées restent dans le dépôt comme versions antérieures, pas comme référence visuelle pour la suite.

---

## 📂 Structure du Dépôt (Éléments Validés)

- [`personnages/charte-personnages-et-equipes.md`](personnages/charte-personnages-et-equipes.md) :
  - Charte graphique et physique des **5 joueurs principaux** (**Léon**, **Lyssandro**, **Ayden**, **Nolann**, **Milo**) au sein de l'effectif de 20 joueurs U8 (4 équipes de 5).
  - Charte des **3 coachs** (**Flavien** père de Léon, **Julien** père de Lyssandro, **Kilian**).
  - Personnages évoqués hors-champ (**Vanessa**, **Alice**, **Baptiste**).
  - Règlement officiel du rugby U8 (terrain 30m x 20m, 5 contre 5, 1 essai = 1 point sans poteaux ni transformations, touche rendue et jouée comme une pénalité, en-avant et hors-jeu comptés, touché à 2 mains jusqu'en novembre puis plaquages autorisés dès décembre).
  - Couleurs officielles du **RCM** (Rouge, Bleu et Blanc — *Locaself*) et des **7 équipes adverses** (Montmélian, Chambéry, Aix-les-Bains, Albertville, Le Môle, Rumilly, Thonon).
  - Règle vestimentaire stricte : tenue de rugby uniquement aux entraînements et tournois ; tenue civile à la maison et à l'école.

- [`scenario/scenario-complet-30-pages.md`](scenario/scenario-complet-30-pages.md) :
  - Découpage intégral page par page et scène par scène (couverture + pages 1 à 30) avec dialogues, narration et effets sonores. Les anciennes indications de bulles et de style comics sont remplacées par la direction photo-réaliste actuelle.

## 🖨️ Format du livre

- Couverture et 30 pages : **A4 portrait (210 × 297 mm), 2480 × 3508 pixels à 300 dpi**.
- [Couverture validée au format A4](planches/00-couverture.png) : illustration complète conservée, sans déformation ni recadrage, avec marges blanches latérales.
- [Source de la couverture validée](planches/00-couverture-source.png) conservée pour les futurs exports.

## Anciennes planches comics conservées

Les fichiers ci-dessous sont les versions illustrées précédemment produites. Ils sont conservés comme archives, mais ne servent plus de référence visuelle pour les nouvelles planches.

- [Planche 1 — La Légende des U6](planches/01-la-legende-des-u6.png) : ancienne version illustrée, avec lettrage corrigé et harmonisé avec la planche 2.
- [Source de la planche 1](planches/01-source.png) et [script de lettrage](outils/lettrage/planche01.py) conservés pour les retouches (Pillow, NumPy, OpenCV headless ; police Kalam sous licence OFL fournie).

- [Planche 2 — Matin de rentrée à Saint-Sulpice](planches/02-matin-de-rentree.png) : lettrage corrigé et validé, dialogues rétablis sans doublons, export A4 à 300 dpi.
- [Source graphique de la planche 2](planches/planches-02-source.png) et [script de lettrage](outils/lettrage/planche02.py) conservés pour les retouches ultérieures (Pillow ; police Kalam sous licence OFL fournie).

## Planche 3 — proposition photographique

- [Planche 3 — Les 20 Guerriers du RCM, version photo-réaliste](planches/03-les-20-guerriers-du-rcm-photo.png) : cinq scènes créées séparément à partir des portraits réels pertinents, assemblées en A4 portrait (2480 × 3508 px, 300 dpi). Dialogues et narration repris du scénario dans des blocs éditoriaux, sans bulles comics ; proposition en attente de validation.
- Les anciennes versions illustrées de la planche 3 restent conservées comme archives.

## Planche 4 — version photo-réaliste corrigée

- [Planche 4 — Nouvelles règles, nouveau monde](planches/04-nouvelles-regles-photo.png) : composition refaite directement avec les portraits photographiques réels de `personnages/* réel.jpg` ; aucun visage n'a été généré ou recréé. Les photos source sont recadrées et mises en page, en conservant leurs poses d'origine.
- Aucun dialogue ni aucune légende ne sont ajoutés, conformément à la demande. Format A4 portrait, 2480 × 3508 px à 300 dpi.

## Ancienne version comics de la planche 4 — archivée

- [Planche 4 — Nouvelles Règles, Nouveau Monde](planches/04-nouvelles-regles.png) : version validée en A4 portrait à 300 dpi, avec les 11 répliques du scénario et un lettrage manuel harmonisé avec les pages précédentes.
- [Dessin source](planches/planches-04-source.png) et [script de lettrage](outils/lettrage/planche04.py) conservés pour les retouches.

## Consignes de production des prochaines planches

- Utiliser les photos `* réel.jpg` des personnages réellement présents dans la scène ; éviter de fournir des portraits inutiles, pour préserver les identités.
- Décrire précisément qui apparaît, où, avec quelle tenue et quelle action. Suivre le découpage et les dialogues du scénario.
- Produire des images photoréalistes de type reportage sportif/familial, sans dessin, effets comics ni bulles. Ajouter les textes ensuite en blocs éditoriaux sobres.
- Ne pas utiliser la couverture ni les anciennes planches comics comme références de style. La photo réelle de la maison peut servir de référence d'architecture pour les scènes extérieures à Saint-Sulpice.
- Conserver les exports finaux au format A4 portrait : 2480 × 3508 px à 300 dpi.
- Un refus signifie que la ressemblance, le réalisme ou le scénario ne sont pas respectés ; corriger le point signalé plutôt que relancer à l'identique.

## Planche 5 — dessin et lettrage validés

- [Dessin sans bulles](planches/05-premiers-sifflets-dessin.png) validé avant lettrage.
- [Planche 5 — Premiers Sifflets & Conseil des Coachs](planches/05-premiers-sifflets.png) : version validée en A4 portrait à 300 dpi, avec huit répliques, deux coups de sifflet, encadré narratif et prénom Léon sur la liste.
- [Script de lettrage](outils/lettrage/planche05.py) conservé pour les retouches.

## Références visuelles — consigne actuelle

- Pour chaque scène, fournir seulement les photos réelles `personnages/<Nom> réel.jpg` des personnages présents.
- Ne pas joindre les portraits PNG illustrés, la couverture comics ou les anciennes planches comme références de style.
- La photo [`personnages/Maison saint sulpice.png`](personnages/Maison%20saint%20sulpice.png) reste une référence réelle d'architecture pour les scènes extérieures de la maison.

## Planche 6 — dessin et lettrage validés

- Source déposée par l'auteur : [planches/planches-06-source.png](planches/planches-06-source.png), validée avant lettrage.
- [Planche 6 — Deux Victoires pour Commencer !](planches/06-deux-victoires.png) : version validée en A4 portrait à 300 dpi, avec encadré narratif, rappel des règles par Flavien, les deux essais et encadrés de match (Chambéry jaune et noir, Albertville rouge et blanc), l'échange Léon/Ayden et l'avertissement de Kilian et Julien avant Montmélian (vert et noir).
- [Script de lettrage](outils/lettrage/planche06.py) conservé pour les retouches.

## Planche 7 — dessin et lettrage validés

- [Dessin sans bulles](planches/07-mur-vert-et-noir-dessin.png) validé avant lettrage.
- [Planche 7 — Le Mur Vert et Noir de Montmélian](planches/07-mur-vert-et-noir.png) : version validée en A4 portrait à 300 dpi, avec six cases : avancée alignée de Montmélian (vert et noir), en-avant de Milo (« PLOP ! FIIIIT ! »), pied en touche de Nolann, essai de Montmélian (+1 point), hors-jeu de Léon et encouragements de Julien et Kilian depuis la touche.
- [Script de lettrage](outils/lettrage/planche07.py) conservé pour les retouches.

## Planche 8 — dessin et lettrage validés

- [Dessin sans bulles](planches/08-action-individuelle-dessin.png) validé avant lettrage.
- [Planche 8 — L'Action Individuelle de Trop](planches/08-action-individuelle.png) : version validée en A4 portrait à 300 dpi, avec cinq cases : passe d'Ayden à Léon, appels démarqués de Lyssandro et Nolann, bulle de pensée de Léon en gros plan, touché à deux mains et en-avant (« TCHAC ! FIIIIIIIT ! », fin du match) et encadré final (2 victoires, 1 défaite).
- [Script de lettrage](outils/lettrage/planche08.py) conservé pour les retouches.

## Planche 9 — dessin et lettrage validés

- [Dessin sans bulles](planches/09-colere-et-larmes-dessin.png) validé avant lettrage.
- [Planche 9 — La Colère et les Larmes](planches/09-colere-et-larmes.png) : version validée en A4 portrait à 300 dpi, avec quatre cases : haie d'honneur avec Montmélian, colère de Léon au bord des larmes, consolation de Lyssandro et Nolann repoussée, puis Flavien agenouillé et l'échange Julien/Kilian.
- [Script de lettrage](outils/lettrage/planche09.py) conservé pour les retouches.
