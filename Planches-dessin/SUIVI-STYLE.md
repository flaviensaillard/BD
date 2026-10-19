# État courant : revue fondée sur la couverture — EN COURS

**La couverture `00-couverture-marvel.png` est désormais la seule référence de style et d’identité.** La décision utilisateur remplace la priorité V2 décrite dans l’historique ci-dessous. La couverture reste inchangée.

Suivi actuel : [`validation/REVUE-COUVERTURE.md`](validation/REVUE-COUVERTURE.md) et son manifeste JSON : 153 vignettes inventoriées, 115 premières reprises, 1 contrôle sans retouche, 0 correction partielle, 37 autres contrôles individuels à faire, aucune validation définitive. Les anciennes approbations ne valent pas conformité au nouveau référentiel. La prise de 18/4 est reprise au lot U ; les raccords de 19/1 sont nettoyés au lot W, puis les cinq cases de 20 reprises au lot X. Planche 21 reprise au lot Y : souvenir mental de Flavien, gestes de réconciliation, visage clair d’Ayden isolé pour éviter sa confusion avec Nolann mat, et geste de Julien sur l’épaule de Flavien. Planche 22 reprise au lot Z : retour du printemps en manches courtes (suppression des sous-pulls d’hiver de 22-1), vestes marine des coachs (22-2 et 22-4), prise de parole de Léon/Lyssandro/Nolann (22-3) et clin d’œil complice de Milo (22-5). Prochaine planche : 23. Réserves transversales sur contacts de plaquage, âge/traits sous bonnets et conformité des motifs/écussons/sponsors des tenues. Aucune bulle ni texte de dialogue ajouté.

---

## Historique antérieur à la décision couverture (non prescriptif)

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
- Un aperçu de livraison a été regardé, sans audit case par case ni reprise. Point manifeste à contrôler en priorité : **30**, dont les groupes et accessoires ont dérivé (identités des trois coachs altérées (le premier comptage à quatre était erroné ; voir rectification ci-dessous) ; ballon déplacé vers l'enfant dans la dernière case). Ce candidat reste à corriger/valider, pas annoncé conforme. D'autres écarts peuvent subsister sur les huit pages, notamment les fonds encore photographiques ou les identités.
- Inventaire : `validation/lot-23-30.json`. Aperçu : `validation/lot-23-30-apercu.jpg`.

**Couverture et pages 01–30 ont maintenant toutes une version restylée. Aucune page ne reste à générer ; cela ne signifie pas que toute la BD est validée. Le contrôle détaillé de 23–30 est différé, conformément à la demande.**

## Audit 23–30 — corrections partielles après contrôle des vignettes

Comparaison des 40 cases aux originaux. Trois pages modifiées (23, 26, 30), six candidats générés retenus et une restauration provisoire de source. 00–22 et les pages 24, 25, 27, 28, 29 sont intactes depuis `6942a37`.

- 23/1 : haut du fond corrigé par masque, tous les joueurs/maillots/ballon protégés. Fond près des personnages encore à reprendre.
- 26/3 : garçon de gauche restauré (peau brune, cheveux noirs ras) ; deux autres enfants protégés.
- 30/2–5 : enfants et trophée, identités/tenues des trois coachs, toit incliné/tenue civile, ballon rendu au père et gestes rétablis. Grille originale restaurée sans étirement. Architecture, rangs arrière et ressemblance fine gardent des réserves.
- 30/1 : candidat rejeté pour tête/personnage supplémentaire. **Source originale rétablie provisoirement au lieu de la scène adulte inventée ; encrage V2 restant à faire.**
- Rectification du premier bilan : 30/3 comptait déjà **trois**, pas quatre coachs. Leur identité était en revanche altérée.

Dix générations produites, quatre rejetées : 24/1 (âge non corrigé), 28/6 (copie de la page témoin), 29/2 (semi-réalisme et coiffure), 30/1 (tête ajoutée). Limite de génération atteinte, trois appels supplémentaires refusés. Pas d'intégration des sorties rejetées.

**Huit vignettes restent à reprendre : 23/1–4, 24/1, 28/6, 29/2, 30/1.** Audit détaillé : `validation/AUDIT-23-30.md`. Contrôles : `outils/retouche/verifier_audit23_30.py` et `verifier_lot23_30.py`. Ce travail est une correction partielle, pas une livraison intégralement validée.

## Seconde passe 23–30 — reprise des huit zones ouvertes

Cinq pages modifiées : **23, 24, 28, 29, 30**. Huit zones reprises, sans changement des autres cases/pages.

- 30/1 est maintenant dessinée : trois enfants dans l’embrassade, six au premier plan ; plus de restauration photographique provisoire. Les quatre autres cases de 30 sont intactes.
- 28/6 : une seule case large, joueurs et fond dessinés, pas de page témoin importée.
- 24/1 : visages plus enfantins et fond dessiné après un essai insuffisant.
- 29/2 : tête/coiffure masquées, châtain clair, maillot conservé ; veste de coach inventée dans le candidat exclue.
- 23/1,2,4 : décors repris par masques, avec premiers plans, bâtiments et terrain d’origine protégés. En 23/2 le nouveau grillage haut n’est pas repris.
- **23/3 reste partielle** : seuls les arbres à gauche sont utilisés ; le reste du décor proposé est écarté car il déplace/réinterprète tribune et montagne.

Dix générations produites, huit utilisées en tout ou partie, deux premiers essais de 24/1 et 29/2 non intégrés. Même témoin V2, mais extraits sans visage/personnage complet pour prévenir les contaminations. Échelle uniforme à chaque montage ; pas d’étirement des dessins.

Rapport actuel : `validation/AUDIT2-23-30.md` et `AUDIT2-23-30.json`. Comparatif : `AUDIT2-23-30-AVANT-APRES.jpg`. Contrôles passés : dimensions et régions hors zones/masques, régions protégées, empreintes, autres cases de 30 et bas du maillot de 29. Ils ne certifient pas le dessin ni les ressemblances.

**Reste ciblé : 23/3, fond principal**, plus les réserves antérieures sur les petits figurants, les identités/anatomies fines, la maison de 30/4 et les logos/lettrages. Quelques textures initiales sont volontairement conservées dans les zones protégées de 23. Pas de validation globale de la série.

## Troisième passe 23–30 — quatre corrections locales supplémentaires

Base `21e6081` ; quatre pages modifiées : **23, 24, 27, 30**. Les autres pages restent identiques.

- **23/3 :** fond principal montagne/végétation repris par masque, au-delà des arbres gauches ; acteurs, architecture masquée et terrain protégés. Pas de reprise de l'ancienne tribune rejetée.
- **24/5 :** fond haut dessiné ; personnages et maison conservés. Bas du décor encore doux : correction partielle. Essai d'aplats d'herbe retiré car trop pixellisé.
- **27/1 :** grands chiffres « 77 » inventés supprimés localement, sans régénérer les joueurs ni inventer de rayures/blason.
- **30/4 :** pignon gauche et petit balcon rétablis, veste brune et cheveux châtain clair ; seule cette case est remplacée. Architecture/proportions et ressemblances restent approximatives.
- **30/2 :** contrôle visuel annoté : 14 enfants derrière + 5 devant, 3 adultes dans la source comme dans la version actuelle. Aucune modification de la case et aucune suppression injustifiée. Ce comptage ne valide pas les identités.

Trois générations utilisées par masque ou dans la seule case concernée. Même témoin V2, extraits sans visage. Dimensions/grille conservées, transformations uniformes. Audit actuel : `validation/AUDIT3-23-30.md` ; preuves et inventaire : `AUDIT3-23-30.json`, `AUDIT3-23-30-AVANT-APRES.jpg`, `AUDIT3-30-2-COMPTAGE.jpg`. Vérificateur actuel : `outils/retouche/verifier_audit3_23_30.py` ; précédents audits contrôlés historiquement. **Pas de validation globale ; bas de 24/5, détails protégés et réserves de ressemblance/finitions restent ouverts.**

## Quatrième passe 23–30 — deux décors de 24, sans changer les personnages

Base `0532a10`. **Seule la page 24 est modifiée** ; 00–23 et 25–30 restent identiques octet pour octet.

- **24/5 :** herbe basse reprise avec les aplats d'une nouvelle proposition dessinée. Chemin, supports, père/fils, maison et fond haut protégés ; pas de reprise de l'essai pixellisé rejeté précédemment. La géométrie du nouveau chemin et les supports du candidat sont exclus de l'échantillonnage.
- **24/2 :** feuillage haut réencré par masque, avec garçon, cheveux/visage/tenue, personne jaune recadrée, piliers, grille, école et sol conservés.
- **28/6 contrôlée sans retouche :** les manches rouges du troisième garçon figurent bien dans la source. Pas de correction arbitraire en blanc et pas de modification de la page.

Deux générations utilisées par masques, même témoin V2, échelle uniforme. Rapport courant : `validation/AUDIT4-23-30.md`, inventaire `AUDIT4-23-30.json`. Comparatif : `AUDIT4-23-30-AVANT-APRES.jpg` ; détail vérifié : `AUDIT4-28-6-MANCHES.jpg`. Vérificateur : `outils/retouche/verifier_audit4_23_30.py` ; chaîne des audits historiques et inventaire du lot actualisés.

**Restent ouverts : architecture/proportions de 30/4, finitions des régions protégées, identités/anatomies fines, petits figurants et marquages. La reprise des deux décors n'est pas une validation globale de la BD.**

## Cinquième passe 23–30 — emprise de maison et couleurs de cérémonie

Base `c2d5b46`. **Pages 27 et 30 modifiées uniquement en 27/3 et 30/4**. Autres cases et fichiers principaux inchangés.

- **30/4 :** grande extension droite inventée supprimée, fond boisé rétabli ; petit appentis gauche réduit d'après le recadrage source. Façade principale, personnages, enfant, visages, terrain bas, chemin et muret existants conservés par masques. Deux générations utilisées localement, pas de relance intégrale de la case ni des personnages.
- **27/3 :** dérive violette de quatre tenues RCM corrigée en rouge/bleu par traitement de teinte local. Valeur HSV V conservée exactement, parties blanches et régions de visages contrôlées. Aucune génération ni changement de silhouette, de personne ou de décor.

L'écart volumétrique manifeste de 30/4 est corrigé ; les détails/proportions architecturaux fins restent réservés, comme les finitions des régions protégées, les ressemblances/anatomies, petits figurants et marquages. **Pas de validation globale.** Les manches rouges authentiques de 28/6 et le groupe de 30/2 ne sont pas modifiés.

Rapport courant : `validation/AUDIT5-23-30.md` ; inventaire `AUDIT5-23-30.json`. Preuves : `AUDIT5-23-30-AVANT-APRES.jpg` et `AUDIT5-27-3-COULEURS.jpg`. Vérificateur courant : `outils/retouche/verifier_audit5_23_30.py`, intégré à la chaîne historique ; inventaire du lot actualisé sans effacer les anciens états.

## Sixième passe 23–30 — coiffure/orientation de 23/2 et teintes des plans larges

Base `1cf3243`. **Pages 23 et 25 modifiées, uniquement en 23/1, 23/2 et 25/1** ; autres cases et fichiers inchangés.

- **23/2 :** garçon central repris d'après son recadrage source : cheveux très courts et tête tournée à droite, au lieu d'une longue mèche et d'une face frontale. Une génération de tête/cou seulement, petit raccord de col ; bras et autres visages conservés. L'ancienne coiffure/son halo sont effacés avec le fond vide déjà retenu à la deuxième passe, pas avec un nouveau paysage ni avec le décor de 23/3 rejeté.
- **23/1, 23/2, 25/1 :** teintes violettes de parties des maillots RCM ramenées au rouge par masques de couleur. Respectivement 782, 1 189 et 1 938 pixels corrigés, valeur HSV V inchangée. Bleus, blancs et peaux hors de la tête ciblée protégés ; pas de nouveau personnage ni de comptage/suppression dans les groupes.

Rapport courant : `validation/AUDIT6-23-30.md`, inventaire `AUDIT6-23-30.json`. Preuves : `AUDIT6-23-30-AVANT-APRES.jpg` et `AUDIT6-23-25-COULEURS.jpg`. Vérificateur courant : `outils/retouche/verifier_audit6_23_30.py`, intégré à la chaîne historique ; inventaire du lot actualisé.

**Coiffure et orientation corrigées ne signifient pas identité parfaite.** Source déjà tramée, ressemblances/expressions fines, anatomies, petits figurants, logos et finitions des zones protégées gardent des réserves. Pas de validation globale de la BD.

## Contrôle final 23–30 — terminé

Base `112958e`. Les **40 vignettes** ont une décision explicite dans `validation/AUDIT-FINAL-23-30.md` et son JSON. Dernière passe : 29 retouches de teinte de tenues/chaussettes et rétablissement du ballon crème à liseré rouge/rosé en 30/5, sans génération de personnage ou de décor, à V constant. Fichiers 00–22 et 24 inchangés. Comptages 25/1 (3+3+4+4) et 30/2 (19+3) conservés ; manches authentiques 28/6 inchangées.

**Pas de correction identifiée laissée en attente dans ce contrôle.** Les anciennes réserves générales relèvent des limites de sources déjà tramées, pas d’une liste de défauts démontrés à réinventer. Cela ne certifie pas la ressemblance trait pour trait ou une identité artistique absolue. Huit comparaisons source/état final et une preuve couleur sont livrées. Vérificateur : `outils/retouche/verifier_audit_final_23_30.py`, après la chaîne historique. La conversation reste ouverte pour les demandes suivantes.

## Nouvelle revue générale — couverture canonique, EN COURS

L’utilisateur remplace le témoin V2 par la couverture comme référence exacte de **style ET personnages** et demande une revue intégrale des 30 planches à l’appui du scénario et des sources réalistes. Les conclusions des anciens audits ne sont pas des validations de ressemblance. Suivi courant : `validation/REVUE-COUVERTURE.md` et `.json`.

Premières corrections : 26/3 (têtes Nolann/Milo/Ayden et carnation visible de Nolann), 26/6 (Flavien brun accroupi à la place de Kilian roux, groupe et style repris). Deux essais complets de 27/5 écartés ; vignette non remplacée. La couverture est inchangée. **Revue intégrale non terminée ; aucune validation définitive de vignette à ce stade.**
