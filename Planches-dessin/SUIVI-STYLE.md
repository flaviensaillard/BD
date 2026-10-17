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
