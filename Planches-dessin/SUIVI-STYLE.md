# Harmonisation du style comics

## Référence validée par l'utilisateur

`validation/01-la-legende-des-u6-temoin-v2.png` : style validé et planche 1 reprise à l'identique dans le dossier principal. Cette image est désormais la référence graphique commune, y compris pour la couverture. Les premiers rendus et le témoin V1 ne sont pas des références de style.

## Lot courant

- 00 : couverture redessinée avec le témoin V2 comme référence.
- 01 : témoin V2 validé, copié sans modification.
- 02–08 et 10 : nouvelles sorties générées à partir des originaux avec le même témoin V2 joint à chaque appel. Contrôle détaillé des identités et du contenu encore nécessaire ; génération ne signifie pas validation définitive.
- 09 : nouvelle sortie rejetée au contrôle pour ajout de trois enfants empruntés à la référence dans la dernière case. Candidat isolé dans `validation/09-colere-et-larmes-a-corriger.png`. Le fichier principal 09 conserve provisoirement sa version précédente, qui n'est PAS conforme au nouveau style validé.
- 11–30 : pas encore retraitées avec le style validé.

Dix générations effectuées ce tour : couverture et pages 02–10. Continuer par la correction de 09 et les pages suivantes au prochain lot.

## Contrôle et limites

Conserver découpage, identités, teints, coiffures, expressions, couleurs des tenues et objets. La référence sert uniquement au rendu graphique, jamais à importer ses personnages, poses ou scènes. Vérifier ce risque explicitement pour chaque sortie.

Des variations de visages, de lettrage et de petits logos restent possibles. Les exports générés ne sont pas des masters A4 natifs à 300 dpi. Ne pas annoncer une fidélité parfaite sur la seule base du prompt.

Branche de livraison : `arena/da207e49-bd`. La branche `arena/a43899a7-bd` n'a pas été modifiée.

## Passe de corrections vignette par vignette

Les planches suivantes restent suspendues. Aucun traitement des pages 11–30 pendant cette passe.

Six remplacements locaux ont été intégrés, à partir de cases isolées avec un extrait du témoin V2 comme référence de traitement :

| Planche | Vignette | Correction ciblée |
|---|---|---|
| 03 | 5 | Simplification encrée de la grande scène du cercle, du terrain et des personnages |
| 05 | 2 | Suppression du fond photographique flou, spectateurs et clôture redessinés |
| 06 | 2 | Harmonisation de l'encrage des joueurs et du fond, adversaire jaune/noir conservé |
| 06 | 3 | Harmonisation de la scène de passe et du fond, adversaire rouge/blanc conservé |
| 08 | 3 | Remplacement du fond flou derrière le porteur de balle par des adversaires dessinés |
| 08 | 5 | Harmonisation des joueurs et du fond derrière le groupe |

Contrôle technique effectué : mêmes dimensions de pages ; différence pixel à pixel NULLE hors des rectangles remplacés. Coordonnées et résultats dans `validation/corrections-vignettes/controle.json`. Aucun redessin global de ces pages.

### Planche 09 : correction incomplète, ne pas valider

Les quatre vignettes ont été générées séparément depuis l'original. Les candidats 1 et 4 sont conservés individuellement dans `validation/corrections-vignettes/`, sans remplacement du fichier principal. La scène finale ne contient plus le trio de coureurs importé par erreur du témoin.

- Vignette 2 rejetée : dérive de la coiffure/couleur de cheveux du gros plan.
- Vignette 3 rejetée : rendu encore trop photographique de la scène de consolation.
- Limite de dix générations atteinte pour cette passe. Reprendre les corrections avant les nouvelles pages.

### Réserves

Cette passe corrige les écarts de rendu les plus visibles ; elle n'est pas une validation exhaustive de tous les visages, vêtements, lettres et détails de toutes les pages. Les pages non retouchées ne sont pas automatiquement déclarées conformes. Vérifier en particulier les expressions des gros plans (notamment 04, vignette 6) contre les originaux : ne pas propager la bouche ouverte du témoin simplement parce que son style a été validé. Contrôler les six cases remplacées à leur taille de lecture avant validation finale ; les différences d'identité ou de contenu restent des critères de rejet.

## Deuxième contrôle et corrections locales

Cette section remplace l'état précédent de 04 et 09.

Comparaison visuelle des originaux et des sorties courantes 00–10, y compris les retouches précédentes. Ce contrôle révèle notamment que le découpage inférieur de 04 avait dérivé : la case originale à trois enfants et la dernière case panoramique avaient été remplacées par deux portraits côte à côte.

### Corrections intégrées

- **04, vignette 5** : reconstitution de la case à trois enfants depuis la source originale, avec trois coiffures et carnations distinctes.
- **04, vignette 6** : reconstitution du garçon tenant son maillot avec les deux mains, sourire fermé et format horizontal. Fond redessiné sans flou photographique.
- **04, mise en page** : deux cases horizontales superposées rétablies en bas. Quatre cases supérieures conservées pixel à pixel.
- **09, vignette 1** : candidat isolé de la passe précédente intégré, poignée de mains et adversaires vert/noir conservés.
- **09, vignette 2** : nouveau gros plan avec cheveux courts châtain clair rabattus de côté, sans les pics importés du témoin. Expression sérieuse et bouche fermée.
- **09, vignette 3** : scène de consolation reprise ; feuillage et sol remplacés par des silhouettes graphiques et des aplats, sans fond photographique. Trois enfants conservés.
- **09, vignette 4** : candidat isolé de la passe précédente intégré ; scène avec bouteille et coachs conservée, sans trio de coureurs ajouté.
- **00, couverture** : sourire fermé du garçon central rétabli par retouche limitée à la bouche. Aucun autre pixel de la couverture modifié durant cette passe.

### Vérification technique

`validation/corrections-vignettes/controle-passe-2.json` contient les zones et résultats. Dimensions conservées. Différence nulle hors de la zone de la bouche sur 00 et hors du bas de page sur 04. Pour 09, les quatre cases sont assemblées sur l'original normalisé à 864 × 1222 ; ses marges et gouttières sont conservées, vérifiées par différence pixel à pixel. Ce test technique ne démontre pas à lui seul la fidélité des identités à l'intérieur des cases.

### Rejets et points encore ouverts

Deux essais de simplification des fonds de 07 (vignettes 2 et 6) ont été écartés : des expressions/détails de premier plan ont dérivé. Le fichier 07 n'a pas été remplacé. Préférer une correction avec masque limité aux fonds pour ne pas toucher aux visages. Ne pas déclarer toute la série parfaitement homogène : il reste des nuances de traitement, et les petits logos/lettrages générés ne sont pas fiabilisés. La planche 01 validée par l'utilisateur reste inchangée malgré son écart d'expression déjà signalé avant validation. Les pages 11–30 restent suspendues.

## Troisième passe — fonds de 07 corrigés par masques

Cette section remplace le statut « fonds de 07 en attente » pour les feuillages des vignettes 2 et 6.

- **07, vignette 2** : feuillage supérieur remplacé par un fond dessiné en aplats et contours encrés. Les quatre joueurs et le ballon proviennent du fichier précédent, pas d'une nouvelle génération des personnages.
- **07, vignette 6** : feuillage supérieur remplacé de la même manière ; coachs, joueurs, ballon et figurants conservés par détourage et masques.
- Le terrain, les marquages et la clôture restent inchangés. Les petits spectateurs lointains de la vignette 2 sont conservés, y compris leur rendu moins net ; leur flou résiduel n'est donc pas annoncé comme corrigé.
- Les deux premières plaques de fond et les premiers détourages ont été écartés après inspection (raccords trop visibles). Seuls les composites finaux sont intégrés.

### Contrôles reproductibles

Les masques blancs de conservation sont enregistrés dans `outils/retouche/masques/`. Les zones protégées réutilisent les pixels de la version précédente, pour ne pas échanger les identités, cheveux, couleurs de peau, tenues ou expressions.

`PYTHONPATH=.arena/vendor python outils/retouche/verifier_planche07.py` dans l'environnement de cette session (ou `python outils/retouche/verifier_planche07.py` avec Pillow installé) vérifie :

1. les dimensions inchangées ;
2. la différence nulle sur tous les pixels protégés ;
3. la différence nulle en dehors des deux vignettes autorisées.

Référence de comparaison : commit `0106661`. Rapport : `validation/corrections-vignettes/controle-passe-3.json`.

Ce test ne certifie ni une découpe sémantique parfaite des silhouettes ni une homogénéité absolue de tous les détails. Les petits logos et textes, certains figurants lointains et les écarts de modelé restent à examiner au besoin. Aucune page 11–30 n'a été traitée pendant cette passe.

## Reprise des nouvelles pages après validation utilisateur

L'utilisateur a validé la passe sur 07 et autorisé la suite.

### Planche 11 — Diagnostic sous la pluie

- Cinq vignettes extraites séparément des originaux, redessinées avec le même extrait d'encrage/aplats du témoin V2 validé, puis assemblées.
- Les photographies et les portraits contradictoires du dépôt ne sont pas joints : SOURCE fixe les identités et les vêtements ; la référence fixe seulement le rendu graphique.
- Premier essai de la vignette 2 rejeté car le cadrage était trop large et coupait le coach à la taille ; deuxième essai intégré avec le cadrage corrigé.
- Ambiance grise et humide, scène sous abri, tableaux, gestes et variantes de tenues conservés dans les consignes et vérifiés visuellement. Pas d'import de coureurs ou de pose du témoin.
- Canvas original **2480 × 3508** conservé, avec cinq cases aux mêmes coordonnées ; pixels de marges, bordures et gouttières vérifiés inchangés. Rapport : `validation/corrections-vignettes/controle-planche-11.json`.
- Réserve : les petits blasons, sponsors et détails des diagrammes générés peuvent varier. L'intérieur des cases n'est pas une conservation pixel à pixel. Les vignettes sont rééchantillonnées au canevas d'origine, pas générées nativement en A4 à 300 dpi.

La prochaine planche complète à traiter est **12 — Travail dans la boue**, à six vignettes. Les pages 12–30 ne sont pas encore retraitées avec la référence validée. La méthode reste vignette par vignette avec contrôle et correction avant assemblage, plutôt qu'un lot de pages entières non contrôlées.

## Planche 12 — Travail dans la boue

Six vignettes traitées séparément, avec le même extrait d'aplats/encrage du témoin V2 validé. La page complète remplace maintenant le fichier principal 12.

- Contrôle de chaque sortie contre son original avant assemblage.
- Reprises : vignette 2 (fond encore photographique), vignette 3 (traitement du coach et du décor), vignette 6 (premier cadrage coupant la tête du coach, puis fond trop photographique).
- Dix générations utilisées ce tour : six premières sorties et quatre reprises. Aucun nouveau fichier de planche 13 livré ; son original reste inchangé.
- Six cases aux mêmes emplacements, canevas 2480 × 3508 conservé ; pixels de bordures, marges et gouttières strictement inchangés, contrôlés par différence pixel à pixel. Écart de rapport largeur/hauteur inférieur à 1 % pour chaque vignette intégrée.
- Rapport : `validation/corrections-vignettes/controle-planche-12.json`.
- Réserves : les générations ne garantissent pas la fidélité pixel à pixel des visages, du lettrage ou des petits blasons. Certaines silhouettes lointaines conservent un traitement plus doux. Les cases sont rééchantillonnées dans le canevas original, pas générées nativement à sa résolution.

**Prochaine planche : 13 — Hauts et bas de novembre (six vignettes).** Les pages 13–30 ne sont pas encore retraitées dans le style validé. Continuer sans nouveau changement de référence graphique et sans remplacer les originaux par des pages partielles.

## Lot accéléré 13–22 — contrôle différé sur demande utilisateur

Nouvelle consigne : générer toutes les pages restantes sans passer du temps en corrections intermédiaires ; l'utilisateur indiquera ensuite les pages à reprendre. Cette consigne remplace la méthode vignette par vignette pour ce lot.

- **13 à 22 : générées et enregistrées en remplacement des fichiers principaux.** Une génération par page entière, à partir de chaque original ; témoin V2 validé joint systématiquement comme unique référence de style.
- **Statut : à contrôler par l'utilisateur**, pas « conformes et validées ». Aucun audit visuel détaillé ni correction locale n'est annoncé pour ce lot.
- Fichiers PNG et dimensions portrait contrôlés techniquement. Résolutions de sortie conservées, sans prétendre à un master A4 natif. Inventaire et empreintes : `validation/lot-13-22.json`.
- Dix générations utilisées, limite du tour atteinte.
- **23 à 30 : encore inchangées, à générer au prochain tour avec la même méthode.** Ne pas annoncer la série complète comme terminée avant cette dernière étape.
- Les pages 00–12 ne sont pas modifiées dans ce lot.

## Audit du lot 13–22 et première passe de correction

Les dix pages ont été comparées visuellement aux originaux et au témoin validé. Neuf fichiers corrigés : 13, 14, 15, 16, 18, 19, 20, 21, 22. La page 17 reste inchangée, avec un écart de couverture neigeuse encore ouvert. Les autres réserves ne sont pas masquées : voir `validation/AUDIT-13-22.md` pour le bilan page par page.

Corrections : météo de 13/1, fond de 14/1, teinte des cheveux du garçon sur 15 par masque sans régénération, nombre de coachs de 16/5, soirée de 18 et des trois premières cases de 19, suppression masquée du coach ajouté sur 20/3 en conservant les joueurs, coiffure de 21/1 et décor de 22/4.

Dix générations utilisées, certaines écartées ou reprises. Pour 20, les sorties générées n'ont pas été utilisées pour les joueurs : seul le terrain de la zone de suppression est reconstitué. Contrôles reproductibles avec `outils/retouche/verifier_audit13_22.py` : dimensions et pixels hors cases/masques conservés ; page 17 inchangée. Tests passés sur les dix pages. Ils ne prouvent pas la fidélité des détails à l'intérieur des zones générées.

23–30 : toujours à générer ; aucune de ces pages n'est modifiée par cet audit. Pas de déclaration de conformité globale des pages 13–22 à ce stade.

## Second audit 13–22 — déformations et excès nocturne

Signalement utilisateur confirmé : le relumage précédent de 18/19 était trop sombre. Il est annulé ; ces deux pages retrouvent exactement les pixels clairs du lot `2dc42ff`, sans nouveau filtre ni régénération. La fidélité finale au crépuscule source reste une réserve, pas une validation acquise.

Six fichiers corrigés : 13, 14, 16, 18, 19, 21. Réparations masquées de visages sur 13/5, 14/3 et 21/1, mains sur 16/4 et 21/2 ; remontage sans étirement sur 13/1 et 16/5. Les candidats générés ne sont intégrés qu’à l’intérieur des masques utiles, pour éviter leurs changements parasites de regards, de blasons ou de personnes.

Cinq générations utilisées. Deux contrôles reproductibles : `outils/retouche/verifier_audit2_13_22.py` et le contrôle cumulatif `verifier_audit13_22.py`. Dimensions, pixels hors zones/masques, régions de visages/maillots protégées et restaurations de lumière contrôlés. **Ils ne certifient pas les identités ou l’anatomie générées.**

Bilan détaillé et réserves : `validation/AUDIT2-13-22.md`. Comparatif : `validation/AUDIT2-AVANT-APRES.jpg`. Réserves encore ouvertes : neige/givre, météo de certaines cases de 13, petits détails et fonds trop photographiques, notamment 16/5 et 22/5. **23–30 restent à générer. Pas de validation globale de 13–22.**

## Dernier lot 23–30 — pages entières, contrôle différé

Après accord utilisateur sur la poursuite, **les huit dernières pages 23 à 30 sont générées et remplacent les fichiers principaux**. Une génération par page entière, original `e0416a5` et témoin V2 approuvé joints à chacun des huit appels. Pas de reprise intermédiaire ni de changement de référence. Aucune modification des fichiers principaux 00–22 (comparaison binaire avec `fa1baf0`).

- Sources utilisées telles que présentes avant ce lot, sans réutiliser une page déjà restylée comme contenu.
- Sorties PNG natives conservées sans étirement, majoritairement 864 × 1232, page 27 : 864 × 1222. Ce n'est pas un master A4 à 300 dpi.
- Consignes renforcées sur les enfants U6, les couleurs, les mains, l'éclairage diurne et les décors dessinés. La présence de ces consignes ne garantit pas leur respect.
- Vérification technique : huit PNG lisibles, dimensions portrait, empreintes enregistrées et pages 00–22 inchangées. **Pas de validation de fidélité des visages, du nombre de personnes, du style ou des petits détails.**
- Un aperçu de livraison a été regardé, sans audit case par case ni reprise. Point manifeste à contrôler en priorité : **30**, dont les groupes et accessoires ont dérivé (quatre coachs au lieu des trois de la source dans la case correspondante ; ballon déplacé vers l'enfant dans la dernière case). Ce candidat reste à corriger/valider, pas annoncé conforme. D'autres écarts peuvent subsister sur les huit pages, notamment les fonds encore photographiques ou les identités.
- Inventaire : `validation/lot-23-30.json`. Aperçu : `validation/lot-23-30-apercu.jpg`.

**Couverture et pages 01–30 ont maintenant toutes une version restylée. Aucune page ne reste à générer ; cela ne signifie pas que toute la BD est validée. Le contrôle détaillé de 23–30 est différé, conformément à la demande.**
