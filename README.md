# 🏉 LA FORCE DE L'ÉCHEC
> *« On apprend de ses échecs, c'est ce qui conduit à la victoire »*

Comics de 30 pages (style Marvel / DC Comics) créé pour **Léon** (6 ans), suivant la saison U8 du **Rugby Club Motterain (RCM)** à **La Motte-Servolex** et la vie à **Saint-Sulpice** en Savoie (saison Septembre 2026 – Juin 2027).

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
  - Découpage intégral page par page et vignette par vignette (Couverture + Pages 1 à 30) avec tous les dialogues enrichis, bulles de pensée, encadrés narratifs et effets sonores.

## 🖨️ Format du livre

- Couverture et 30 pages : **A4 portrait (210 × 297 mm), 2480 × 3508 pixels à 300 dpi**.
- [Couverture photoréaliste validée au format A4](planches/00-couverture.png) : portrait des cinq joueurs et de leurs trois coachs, en tenues RCM, sans titre ni texte ajouté ; export A4 portrait (2480 × 3508 px, 300 dpi).
- [Source de la couverture](planches/00-couverture-source.png) conservée pour les futurs exports.

## Planches validées

- [Planche 1 — La Légende des U6](planches/01-la-legende-des-u6.png) : lettrage corrigé et validé, harmonisé avec la planche 2. Réplique de Lyssandro rétablie, doublon supprimé, export A4 à 300 dpi sans régénération du dessin.
- [Source de la planche 1](planches/01-source.png) et [script de lettrage](outils/lettrage/planche01.py) conservés pour les retouches (Pillow, NumPy, OpenCV headless ; police Kalam sous licence OFL fournie).

- [Planche 2 — Matin de rentrée à Saint-Sulpice](planches/02-matin-de-rentree.png) : lettrage corrigé et validé, dialogues rétablis sans doublons, export A4 à 300 dpi.
- [Source graphique de la planche 2](planches/planches-02-source.png) et [script de lettrage](outils/lettrage/planche02.py) conservés pour les retouches ultérieures (Pillow ; police Kalam sous licence OFL fournie).

## Planche 3 — dessin et lettrage validés

- [Planche 3 — Les 20 Guerriers du RCM](planches/03-les-20-guerriers-du-rcm.png) : nouvelle version validée avec lettrage manuel, A4 portrait à 300 dpi.
- [Script de lettrage](outils/lettrage/planche03.py) conservé pour les retouches.
- [Nouveau dessin sans bulles](planches/03-les-20-guerriers-dessin.png) : validé par l'utilisateur, en remplacement de la proposition précédemment rejetée.
- Processus : validation du dessin sans bulles, puis ajout manuel des textes avec la police Kalam utilisée pour les planches 1 et 2 ; validation du lettrage avant publication finale.

## Planche 4 — dessin et lettrage validés

- [Planche 4 — Nouvelles Règles, Nouveau Monde](planches/04-nouvelles-regles.png) : version validée en A4 portrait à 300 dpi, avec les 11 répliques du scénario et un lettrage manuel harmonisé avec les pages précédentes.
- [Dessin source](planches/planches-04-source.png) et [script de lettrage](outils/lettrage/planche04.py) conservés pour les retouches.
- [Version photoréaliste sans bulles ni lettrage narratif](planches/04-nouvelles-regles-realisme-sans-texte.png) : six vignettes en A4 portrait à 300 dpi, basées sur les huit portraits réels ; [source générée](planches/04-nouvelles-regles-realisme-source.png) conservée.

## Contrainte pour les prochaines générations

- Préférence initiale de l'utilisateur : `gpt-image-2.5-sunburst`. L'outil disponible ne permet pas de sélectionner le modèle.
- L'utilisateur autorise désormais l'utilisation de cet outil **pour toutes les prochaines planches, sans garantie sur le modèle utilisé**. Il n'est pas nécessaire de redemander cette autorisation à chaque page.
- Les autres contraintes restent inchangées : deux propositions, couverture seule en référence visuelle, validation du dessin sans bulles, puis lettrage manuel harmonisé et validation finale.

- Par défaut, un refus de proposition signifie que les personnages et la charte graphique ne sont pas respectés. Ne pas redemander le motif ; l’utilisateur précisera spontanément toute autre raison.

## Planche 5 — dessin et lettrage validés

- [Dessin sans bulles](planches/05-premiers-sifflets-dessin.png) validé avant lettrage.
- [Planche 5 — Premiers Sifflets & Conseil des Coachs](planches/05-premiers-sifflets.png) : version validée en A4 portrait à 300 dpi, avec huit répliques, deux coups de sifflet, encadré narratif et prénom Léon sur la liste.
- [Version photoréaliste sans bulles ni texte narratif](planches/05-premiers-sifflets-realisme-sans-texte.png) : cinq vignettes au format A4 portrait à 300 dpi, construites vignette par vignette à partir des portraits réels ; [source assemblée](planches/05-premiers-sifflets-realisme-source.png) conservée.
- [Script de lettrage](outils/lettrage/planche05.py) conservé pour les retouches.

## Références visuelles — consigne actuelle

- Pour toute nouvelle génération, utiliser **uniquement** `planches/00-couverture-source.png` (la couverture, référence de style et de continuité) **et les huit portraits PNG des personnages concernés** (`personnages/Léon.png`, `Lyssandro.png`, `Ayden.png`, `Nolann.png`, `Milo.png`, `Flavien.png`, `Julien.png`, `Kilian.png`) dans le paramètre `images`.
- Ne plus joindre les autres planches comme références visuelles. Les fichiers existants restent conservés.
- Les autres contraintes du scénario, du format A4, des deux propositions et du lettrage après validation restent inchangées.

## Planche 6 — dessin et lettrage validés

- Source déposée par l'auteur : [planches/planches-06-source.png](planches/planches-06-source.png), validée avant lettrage.
- [Planche 6 — Deux Victoires pour Commencer !](planches/06-deux-victoires.png) : version validée en A4 portrait à 300 dpi, avec encadré narratif, rappel des règles par Flavien, les deux essais et encadrés de match (Chambéry jaune et noir, Albertville rouge et blanc), l'échange Léon/Ayden et l'avertissement de Kilian et Julien avant Montmélian (vert et noir).
- [Version photoréaliste sans bulles ni texte narratif](planches/06-deux-victoires-realisme-sans-texte.png) : cinq vignettes au format A4 portrait à 300 dpi, construites vignette par vignette à partir des portraits réels ; [source assemblée](planches/06-deux-victoires-realisme-source.png) conservée.
- [Script de lettrage](outils/lettrage/planche06.py) conservé pour les retouches.

## Planche 7 — dessin et lettrage validés

- [Dessin sans bulles](planches/07-mur-vert-et-noir-dessin.png) validé avant lettrage.
- [Planche 7 — Le Mur Vert et Noir de Montmélian](planches/07-mur-vert-et-noir.png) : version validée en A4 portrait à 300 dpi, avec six cases : avancée alignée de Montmélian (vert et noir), en-avant de Milo (« PLOP ! FIIIIT ! »), pied en touche de Nolann, essai de Montmélian (+1 point), hors-jeu de Léon et encouragements de Julien et Kilian depuis la touche.
- [Version photoréaliste sans bulles ni texte narratif](planches/07-mur-vert-et-noir-realisme-sans-texte.png) : six vignettes au format A4 portrait à 300 dpi, construites vignette par vignette à partir des portraits réels ; [source assemblée](planches/07-mur-vert-et-noir-realisme-source.png) conservée.
- [Script de lettrage](outils/lettrage/planche07.py) conservé pour les retouches.

## Planche 8 — dessin et lettrage validés

- [Dessin sans bulles](planches/08-action-individuelle-dessin.png) validé avant lettrage.
- [Planche 8 — L'Action Individuelle de Trop](planches/08-action-individuelle.png) : version validée en A4 portrait à 300 dpi, avec cinq cases : passe d'Ayden à Léon, appels démarqués de Lyssandro et Nolann, bulle de pensée de Léon en gros plan, touché à deux mains et en-avant (« TCHAC ! FIIIIIIIT ! », fin du match) et encadré final (2 victoires, 1 défaite).
- [Version photoréaliste sans bulles ni texte narratif](planches/08-action-individuelle-realisme-sans-texte.png) : cinq vignettes au format A4 portrait à 300 dpi, construites vignette par vignette à partir des portraits réels ; [source assemblée](planches/08-action-individuelle-realisme-source.png) conservée.
- [Script de lettrage](outils/lettrage/planche08.py) conservé pour les retouches.

## Planche 9 — dessin et lettrage validés

- [Dessin sans bulles](planches/09-colere-et-larmes-dessin.png) validé avant lettrage.
- [Planche 9 — La Colère et les Larmes](planches/09-colere-et-larmes.png) : version validée en A4 portrait à 300 dpi, avec quatre cases : haie d'honneur avec Montmélian, colère de Léon au bord des larmes, consolation de Lyssandro et Nolann repoussée, puis Flavien agenouillé et l'échange Julien/Kilian.
- [Version photoréaliste sans bulles ni texte narratif](planches/09-colere-et-larmes-realisme-sans-texte.png) : quatre vignettes au format A4 portrait à 300 dpi, construites vignette par vignette à partir des portraits réels ; [source assemblée](planches/09-colere-et-larmes-realisme-source.png) conservée.
- [Script de lettrage](outils/lettrage/planche09.py) conservé pour les retouches.

## Planche 10 — version photoréaliste

- [Ruminations à Saint-Sulpice et à l'École — dessin sans bulles](planches/10-ruminations-realisme-sans-texte.png) : cinq vignettes photoréalistes au format A4 portrait à 300 dpi, avec les tenues civiles à la maison et à l'école ; [source assemblée](planches/10-ruminations-realisme-source.png) conservée.

## Planche 11 — version photoréaliste

- [Le Diagnostic sous la Pluie — dessin sans bulles](planches/11-diagnostic-sous-la-pluie-realisme-sans-texte.png) : cinq vignettes photoréalistes au format A4 portrait à 300 dpi, avec la pluie au stade et un tableau composé de schémas visuels sans texte ; [source assemblée](planches/11-diagnostic-sous-la-pluie-realisme-source.png) conservée.

## Planche 12 — version photoréaliste

- [Travail dans la Boue — sans bulles ni texte narratif](planches/12-travail-dans-la-boue-realisme-sans-texte.png) : six vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), sur les ateliers de défense et de passes sous la pluie ; [source assemblée](planches/12-travail-dans-la-boue-realisme-source.png) conservée.

## Planche 13 — version photoréaliste

- [Les Hauts et les Bas de Novembre — sans bulles ni texte narratif](planches/13-hauts-et-bas-de-novembre-realisme-sans-texte.png) : six vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), entre tournoi d'automne, victoire contre Aix-les-Bains et essai décisif de Rumilly ; [source assemblée](planches/13-hauts-et-bas-de-novembre-realisme-source.png) conservée.

## Planche 14 — version photoréaliste

- [Les Mots de Trop — sans bulles ni texte narratif](planches/14-les-mots-de-trop-realisme-sans-texte.png) : cinq vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), autour de la défaite contre Rumilly, de l'éclat de Léon et du réconfort de ses amis et de Flavien ; [source assemblée](planches/14-les-mots-de-trop-realisme-source.png) conservée.

## Planche 15 — version photoréaliste

- [La Leçon d'un Père — sans bulles ni texte narratif](planches/15-la-lecon-d-un-pere-realisme-sans-texte.png) : cinq vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), montrant le dialogue intimiste de Léon et Flavien dans le salon familial de Saint-Sulpice ; [source assemblée](planches/15-la-lecon-d-un-pere-realisme-source.png) conservée.

## Planche 16 — version photoréaliste

- [Le Pardon des Copains — sans bulles ni texte narratif](planches/16-le-pardon-des-copains-realisme-sans-texte.png) : cinq vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), du pardon entre Léon et Ayden dans la cour d'école à la réconciliation de l'équipe au stade ; [source assemblée](planches/16-le-pardon-des-copains-realisme-source.png) conservée.

## Planche 17 — version photoréaliste

- [Décembre sous la Neige : Place aux Plaquages ! — sans bulles ni texte narratif](planches/17-decembre-sous-la-neige-realisme-sans-texte.png) : cinq vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), du stade enneigé et des équipements d'hiver à l'annonce des plaquages et aux consignes de Flavien ; [source assemblée](planches/17-decembre-sous-la-neige-realisme-source.png) conservée.

## Planche 18 — version photoréaliste

- [L'École du Plaquage dans le Froid — sans bulles ni texte narratif](planches/18-ecole-du-plaquage-dans-le-froid-realisme-sans-texte.png) : six vignettes photoréalistes générées séparément puis assemblées en A4 portrait (2480 × 3508 px, 300 dpi), des démonstrations de plaquage bas au soutien offensif de Léon par Lyssandro ; [source assemblée](planches/18-ecole-du-plaquage-dans-le-froid-realisme-source.png) conservée.
