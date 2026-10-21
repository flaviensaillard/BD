# AUDIT DU LETTRAGE LIVRÉ — queues et recouvrements

Audit des 30 planches de `Planches-dessin/Avec-texte/` (commit `0fd9784`),
réponses aux deux défauts signalés : *« les bulles ne pointent pas vers les têtes 
des personnages qui parlent »* et *« beaucoup cachent les personnages »*.

## Méthode

- Locuteur attendu de chaque bulle : scénario complet (aligné texte à texte sur les éléments livrés).
- Têtes détectées : cascades Haar frontal + profil + profil miroir (la génération n'utilisait que
  frontal + profil : des têtes ont été ratées, donc recouvertes ou non pointées).
- Identité des têtes : signatures couleur calibrées sur les 8 recadrages nominatifs de la couverture
  (8/8 reconnus en calibration) — teint mat de Nolann, roux de Kilian, gris de Julien,
  barbe/cheveux foncés de Flavien, maillots adverses vert/jaune. Léon, Milo, Lyssandro et Ayden
  (châtains) ne sont pas séparables par la couleur : vérifiables seulement si un seul châtain
  apparaît dans la vignette. En vignette, un fond coloré peut fausser une étiquette d'identité :
  les verdicts « QUEUE DANS LE VIDE » et « recouvrement » ne dépendent pas de l'identité.
- Queues : recalculées à l'identique du rendu livré (vérifié par échantillonnage de pixels),
  comparées aux boîtes de têtes de leur vignette (OK si pointe à ≤ 28 px du locuteur).
- Recouvrement : rectangle posé (manifeste) contre têtes (marge 15 %) et blobs de peau comics
  (corps) de la vignette.
- Aucune vision humaine dans cette session : les verdicts « non vérifiable » sont explicites et
  les seuils chiffrés restent dans le JSON (`AUDIT-BULLES.json`).

## Bilan

- Bulles et pensées auditées : **241**
- Queues correctes : **22** — imprécises : 7
- **Mauvais locuteur (pointe un autre personnage) : 11**
- **Queue dans le vide (aucune tête à moins de 28 px) : 94**
- Non vérifiables (locuteur châtain non isolable ou tête non détectée) : **107**
- Éléments recouvrant une tête ou un personnage : **101**
- Vignettes concernées au total : **107** sur 153
- Écart de contenu relevé : page 14 vignette 3, la réplique d'Ayden
  « Ouais ! Si c'est pour nous crier dessus comme ça, on n'a même plus envie de te faire des passes ! »
  du scénario n'a pas été lettrée.

## Détail par planche et vignette

### Planche 01 — 01-la-legende-des-u6

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 1-1 | 1 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 1-1 | 2 | bulle | Nolann | IMPRÉCIS | tête Nolann (59%) ; corps/peau 79% de 1254px² ; corps/peau 80% de 2136px² |
| 1-2 | 4 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 1-3 | 6 | bulle | Ayden | — | corps/peau 100% de 897px² ; corps/peau 99% de 959px² |
| 1-4 | 7 | bulle | Léon | QUEUE DANS LE VIDE | — |

### Planche 02 — 02-matin-de-rentree

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 2-2 | 2 | voix | Voix hors-champ depuis l'étage | — (sans queue) | corps/peau 100% de 737px² |
| 2-2 | 3 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 2-3 | 5 | bulle | Flavien | non vérifiable* | tête Julien (77%) |
| 2-4 | 6 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 2-5 | 9 | bulle | Léon | QUEUE DANS LE VIDE | — |

### Planche 03 — 03-les-20-guerriers-du-rcm

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 3-2 | 1 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 100% de 1474px² ; corps/peau 100% de 842px² |
| 3-2 | 2 | bulle | Lyssandro | QUEUE DANS LE VIDE | corps/peau 66% de 1474px² ; corps/peau 100% de 842px² |
| 3-2 | 3 | bulle | Ayden | QUEUE DANS LE VIDE | — |
| 3-3 | 4 | bulle | Nolann | QUEUE DANS LE VIDE | — |
| 3-3 | 5 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 3-5 | 9 | bulle | Léon | QUEUE DANS LE VIDE | tête chatain (60%) ; corps/peau 70% de 782px² ; corps/peau 100% de 671px² |

### Planche 04 — 04-nouvelles-regles

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 4-1 | 0 | bulle | Flavien | QUEUE DANS LE VIDE | — |
| 4-1 | 1 | bulle | Kilian | QUEUE DANS LE VIDE | — |
| 4-2 | 2 | bulle | Julien | QUEUE DANS LE VIDE | — |
| 4-3 | 3 | bulle | Kilian | non vérifiable* | corps/peau 100% de 768px² |
| 4-3 | 4 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 4-3 | 5 | bulle | Flavien | QUEUE DANS LE VIDE | corps/peau 100% de 671px² |
| 4-4 | 6 | bulle | Julien | non vérifiable* | corps/peau 100% de 704px² |
| 4-4 | 7 | bulle | Kilian | QUEUE DANS LE VIDE | — |
| 4-5 | 8 | bulle | Ayden | QUEUE DANS LE VIDE | — |
| 4-6 | 10 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 100% de 4319px² |

### Planche 05 — 05-premiers-sifflets

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 5-1 | 0 | ono | — | — (sans queue) | tête adversaire-jaune (11%) |
| 5-1 | 1 | bulle | Julien | MAUVAIS LOCUTEUR | tête adversaire-jaune (100%) |
| 5-2 | 3 | bulle | Kilian | QUEUE DANS LE VIDE | corps/peau 100% de 607px² ; corps/peau 100% de 1132px² ; corps/peau 48% de 1474px² |
| 5-2 | 4 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 93% de 1058px² ; corps/peau 100% de 1474px² |
| 5-3 | 6 | bulle | Kilian | QUEUE DANS LE VIDE | — |
| 5-4 | 7 | bulle | Julien | QUEUE DANS LE VIDE | tête chatain (100%) ; corps/peau 100% de 2289px² |
| 5-5 | 9 | bulle | Flavien | non vérifiable* | corps/peau 100% de 1908px² |

### Planche 06 — 06-deux-victoires

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 6-1 | 1 | bulle | Flavien | MAUVAIS LOCUTEUR | — |
| 6-2 | 2 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |
| 6-2 | 3 | bulle | Nolann | non vérifiable* | corps/peau 100% de 641px² |
| 6-2 | 4 | encadre | — | — (sans queue) | corps/peau 100% de 808px² |
| 6-3 | 5 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 6-3 | 6 | bulle | Léon | IMPRÉCIS | — |
| 6-3 | 7 | encadre | — | — (sans queue) | corps/peau 73% de 675px² |
| 6-4 | 8 | bulle | Léon | IMPRÉCIS | corps/peau 100% de 800px² ; corps/peau 100% de 809px² ; corps/peau 100% de 1006px² |
| 6-4 | 9 | bulle | Ayden | QUEUE DANS LE VIDE | corps/peau 52% de 800px² ; corps/peau 55% de 809px² ; corps/peau 67% de 1006px² |
| 6-5 | 10 | bulle | Kilian | non vérifiable* | tête Julien (78%) ; tête Flavien (100%) ; tête Nolann (71%) |
| 6-5 | 11 | bulle | Julien | QUEUE DANS LE VIDE | tête Nolann (83%) ; corps/peau 100% de 1041px² ; corps/peau 100% de 743px² |

### Planche 07 — 07-mur-vert-et-noir

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 7-1 | 0 | bulle | adversaire-vert | QUEUE DANS LE VIDE | — |
| 7-1 | 1 | bulle | Lyssandro | MAUVAIS LOCUTEUR | — |
| 7-2 | 5 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 7-3 | 8 | bulle | Nolann | QUEUE DANS LE VIDE | — |

### Planche 08 — 08-action-individuelle

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 8-1 | 0 | bulle | Ayden | QUEUE DANS LE VIDE | tête chatain (72%) ; corps/peau 100% de 754px² ; corps/peau 100% de 893px² |
| 8-2 | 1 | bulle | Lyssandro | QUEUE DANS LE VIDE | tête chatain (99%) |
| 8-3 | 3 | pensee | Léon | QUEUE DANS LE VIDE | corps/peau 70% de 4627px² |
| 8-4 | 6 | bulle | Arbitre | non vérifiable* | corps/peau 100% de 1095px² ; corps/peau 40% de 1045px² |
| 8-5 | 7 | encadre | — | — (sans queue) | tête adversaire-vert (15%) |

### Planche 09 — 09-colere-et-larmes

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 9-1 | 0 | bulle | Ayden | non vérifiable* | tête Nolann (100%) ; corps/peau 100% de 613px² ; corps/peau 100% de 643px² |
| 9-1 | 1 | bulle | adversaire-vert | non vérifiable* | tête Nolann (100%) ; corps/peau 100% de 603px² |
| 9-3 | 3 | bulle | Lyssandro | non vérifiable* | corps/peau 100% de 883px² |
| 9-3 | 4 | bulle | Nolann | QUEUE DANS LE VIDE | — |
| 9-3 | 5 | bulle | Léon | non vérifiable* | corps/peau 100% de 1000px² ; corps/peau 100% de 1267px² |
| 9-4 | 7 | bulle | Julien | QUEUE DANS LE VIDE | — |

### Planche 10 — 10-ruminations

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 10-1 | 1 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 10-2 | 2 | bulle | Flavien | non vérifiable* | corps/peau 47% de 2813px² |
| 10-3 | 5 | bulle | Ayden | QUEUE DANS LE VIDE | — |
| 10-3 | 6 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 10-5 | 9 | bulle | Ayden | QUEUE DANS LE VIDE | tête chatain-clair (65%) ; corps/peau 100% de 2532px² |
| 10-5 | 10 | bulle | Léon | QUEUE DANS LE VIDE | — |

### Planche 11 — 11-diagnostic-sous-la-pluie

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 11-2 | 1 | bulle | Kilian | IMPRÉCIS | tête Flavien (100%) ; tête chatain (100%) |
| 11-2 | 2 | bulle | Julien | non vérifiable* | tête Flavien (35%) ; corps/peau 100% de 1592px² ; corps/peau 100% de 1143px² |
| 11-3 | 3 | bulle | Lyssandro | — | corps/peau 67% de 736px² |
| 11-3 | 4 | bulle | Ayden | QUEUE DANS LE VIDE | corps/peau 47% de 796px² |
| 11-3 | 5 | bulle | Nolann | QUEUE DANS LE VIDE | corps/peau 100% de 796px² ; corps/peau 100% de 652px² |
| 11-4 | 6 | bulle | Flavien | QUEUE DANS LE VIDE | tête Flavien (83%) |
| 11-4 | 7 | bulle | Flavien | MAUVAIS LOCUTEUR | tête Flavien (83%) |

### Planche 12 — 12-travail-dans-la-boue

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 12-4 | 4 | bulle | Ayden | QUEUE DANS LE VIDE | tête Nolann (100%) |
| 12-4 | 5 | bulle | Lyssandro | — | tête Nolann (47%) |
| 12-5 | 7 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 12-6 | 8 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 12-6 | 9 | bulle | Lyssandro | MAUVAIS LOCUTEUR | corps/peau 100% de 1145px² |
| 12-6 | 10 | bulle | Flavien | non vérifiable* | corps/peau 100% de 1467px² ; corps/peau 100% de 944px² |

### Planche 13 — 13-hauts-et-bas-de-novembre

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 13-3 | 3 | bulle | Léon | QUEUE DANS LE VIDE | tête chatain (73%) ; tête ? (100%) ; corps/peau 100% de 670px² |
| 13-3 | 4 | bulle | Kilian | non vérifiable* | tête Nolann (42%) ; corps/peau 100% de 932px² |
| 13-5 | 6 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 100% de 611px² |

### Planche 14 — 14-les-mots-de-trop

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 14-1 | 0 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 14-1 | 1 | bulle | Nolann | MAUVAIS LOCUTEUR | — |
| 14-2 | 2 | bulle | Léon | QUEUE DANS LE VIDE | tête chatain (65%) ; corps/peau 77% de 8630px² ; corps/peau 100% de 6628px² |
| 14-4 | 5 | bulle | Flavien | QUEUE DANS LE VIDE | tête Flavien (100%) |
| 14-4 | 6 | bulle | Julien | QUEUE DANS LE VIDE | — |
| 14-5 | 7 | pensee | Léon | QUEUE DANS LE VIDE | tête Flavien (35%) ; corps/peau 53% de 3144px² |

### Planche 15 — 15-la-lecon-d-un-pere

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 15-2 | 2 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 15-3 | 4 | bulle | Léon | non vérifiable* | tête adversaire-vert (100%) ; corps/peau 100% de 6271px² ; corps/peau 100% de 1004px² |
| 15-4 | 5 | bulle | Flavien | non vérifiable* | corps/peau 37% de 7113px² |
| 15-4 | 6 | bulle | Flavien | non vérifiable* | corps/peau 91% de 14499px² |
| 15-5 | 8 | bulle | Flavien | non vérifiable* | corps/peau 100% de 5406px² ; corps/peau 48% de 792px² |
| 15-5 | 9 | bulle | Léon | non vérifiable* | corps/peau 48% de 5406px² ; corps/peau 75% de 792px² |

### Planche 16 — 16-le-pardon-des-copains

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 16-1 | 0 | bulle | Léon | non vérifiable* | tête ? (100%) ; corps/peau 100% de 628px² |
| 16-2 | 1 | bulle | Ayden | QUEUE DANS LE VIDE | tête chatain (100%) |
| 16-3 | 3 | bulle | Léon | MAUVAIS LOCUTEUR | — |
| 16-4 | 4 | bulle | Milo | QUEUE DANS LE VIDE | corps/peau 100% de 4524px² |
| 16-4 | 5 | bulle | Léon | — | corps/peau 36% de 924px² |
| 16-4 | 6 | bulle | Nolann | non vérifiable* | corps/peau 100% de 1330px² ; corps/peau 100% de 3554px² ; corps/peau 56% de 4153px² |
| 16-4 | 7 | bulle | Lyssandro | QUEUE DANS LE VIDE | corps/peau 100% de 3554px² ; corps/peau 100% de 4153px² |
| 16-5 | 8 | bulle | Kilian | MAUVAIS LOCUTEUR | — |

### Planche 17 — 17-decembre-sous-la-neige

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 17-3 | 3 | bulle | Ayden | QUEUE DANS LE VIDE | tête chatain (100%) |
| 17-4 | 4 | bulle | Julien | QUEUE DANS LE VIDE | tête Nolann (100%) |
| 17-4 | 7 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 17-5 | 8 | bulle | Flavien | non vérifiable* | corps/peau 100% de 978px² ; corps/peau 100% de 872px² |

### Planche 18 — 18-ecole-du-plaquage-dans-le-froid

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 18-1 | 0 | bulle | Julien | QUEUE DANS LE VIDE | — |
| 18-1 | 2 | ono | — | — (sans queue) | tête ? (16%) |
| 18-1 | 7 | ono | — | — (sans queue) | tête ? (16%) |
| 18-2 | 1 | bulle | Flavien | non vérifiable* | tête ? (75%) |
| 18-6 | 9 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |

### Planche 19 — 19-les-joueurs-analysent-les-coachs-preparent

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 19-1 | 0 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 19-1 | 1 | bulle | Ayden | IMPRÉCIS | — |
| 19-2 | 2 | bulle | Lyssandro | QUEUE DANS LE VIDE | tête chatain (100%) ; corps/peau 100% de 981px² |
| 19-5 | 7 | bulle | Julien | — | corps/peau 61% de 8464px² |

### Planche 20 — 20-le-test-du-grand-froid-le-mole-et-thonon

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 20-1 | 2 | bulle | Arbitre | non vérifiable* | corps/peau 100% de 655px² |
| 20-5 | 10 | bulle | Milo | QUEUE DANS LE VIDE | tête chatain (100%) |

### Planche 21 — 21-la-plus-belle-des-victoires-de-leon

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 21-2 | 1 | bulle | Léon | non vérifiable* | corps/peau 85% de 2112px² |
| 21-3 | 2 | bulle | Milo | IMPRÉCIS | — |
| 21-3 | 3 | bulle | Léon | MAUVAIS LOCUTEUR | — |
| 21-3 | 4 | bulle | Ayden | MAUVAIS LOCUTEUR | — |
| 21-3 | 5 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |
| 21-4 | 6 | bulle | Léon | non vérifiable* | tête Julien (13%) ; tête Julien (55%) ; corps/peau 100% de 941px² |
| 21-5 | 8 | bulle | Flavien | non vérifiable* | corps/peau 68% de 661px² |

### Planche 22 — 22-le-soleil-de-mars-sur-la-motte-servolex

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 22-3 | 2 | bulle | Léon | QUEUE DANS LE VIDE | tête ? (31%) |
| 22-3 | 3 | bulle | Lyssandro | QUEUE DANS LE VIDE | corps/peau 100% de 1502px² |
| 22-3 | 4 | bulle | Nolann | QUEUE DANS LE VIDE | corps/peau 100% de 687px² |
| 22-4 | 5 | bulle | Kilian | MAUVAIS LOCUTEUR | corps/peau 100% de 1262px² |
| 22-5 | 6 | bulle | Milo | — | tête Nolann (100%) |

### Planche 23 — 23-les-trois-piliers-du-jeu

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 23-1 | 0 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 23-1 | 1 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |
| 23-2 | 3 | bulle | Ayden | QUEUE DANS LE VIDE | — |
| 23-2 | 4 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 23-3 | 5 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |
| 23-3 | 6 | bulle | Léon & Milo | non vérifiable* | corps/peau 54% de 895px² ; corps/peau 100% de 805px² |
| 23-4 | 8 | bulle | Kilian | non vérifiable* | tête Nolann (91%) ; tête Nolann (32%) |

### Planche 24 — 24-veille-de-grand-tournoi-a-l-ecole-et-a-saint-sulpice

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 24-1 | 0 | bulle | Ayden | QUEUE DANS LE VIDE | corps/peau 100% de 2085px² |
| 24-1 | 1 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 24-2 | 2 | bulle | Flavien | non vérifiable* | tête ? (100%) |
| 24-3 | 4 | bulle | Flavien | non vérifiable* | tête Nolann (100%) |
| 24-4 | 6 | bulle | Léon | non vérifiable* | tête Nolann (100%) ; corps/peau 100% de 2154px² |

### Planche 25 — 25-le-grand-tournoi-final

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 25-2 | 2 | bulle | Léon | non vérifiable* | tête ? (23%) |
| 25-3 | 5 | bulle | Nolann | QUEUE DANS LE VIDE | — |
| 25-3 | 7 | encadre | — | — (sans queue) | corps/peau 79% de 727px² |
| 25-5 | 10 | bulle | Léon | QUEUE DANS LE VIDE | tête Flavien (100%) |

### Planche 26 — 26-l-echec-qui-fait-grandir

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 26-1 | 0 | bulle | Nolann | non vérifiable* | tête ? (51%) |
| 26-3 | 3 | bulle | Nolann | QUEUE DANS LE VIDE | — |
| 26-3 | 4 | bulle | Milo | QUEUE DANS LE VIDE | — |
| 26-4 | 5 | bulle | Julien | QUEUE DANS LE VIDE | — |
| 26-4 | 6 | bulle | Kilian | non vérifiable* | tête Flavien (100%) |
| 26-5 | 7 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 26-6 | 8 | bulle | Flavien | QUEUE DANS LE VIDE | — |
| 26-6 | 9 | bulle | Julien | non vérifiable* | tête Flavien (100%) |
| 26-6 | 10 | bulle | Léon | IMPRÉCIS | — |

### Planche 27 — 27-la-correction-appliquee-l-heure-de-la-revanche

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 27-4 | 6 | bulle | Nolann | — | tête Nolann (100%) |
| 27-5 | 7 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 100% de 1180px² ; corps/peau 73% de 1027px² |
| 27-5 | 8 | bulle | Tous les cinq | non vérifiable* | corps/peau 100% de 605px² |

### Planche 28 — 28-le-choc-des-titans-rcm-vs-montmelian

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 28-1 | 0 | encadre | — | — (sans queue) | tête adversaire-vert (92%) |
| 28-3 | 3 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |

### Planche 29 — 29-la-passe-de-la-victoire

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 29-1 | 0 | bulle | Défenseur de Montmélian | non vérifiable* | tête Nolann (100%) |
| 29-3 | 2 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 100% de 724px² |
| 29-3 | 3 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |
| 29-3 | 4 | bulle | Nolann | QUEUE DANS LE VIDE | — |

### Planche 30 — 30-on-apprend-de-ses-echecs

| Vignette | Él. | Type | Locuteur attendu | Queue livrée | Recouvrement |
|---|---|---|---|---|---|
| 30-1 | 1 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 30-2 | 2 | bulle | Julien | non vérifiable* | corps/peau 100% de 845px² |
| 30-2 | 3 | bulle | Léon | QUEUE DANS LE VIDE | — |
| 30-2 | 4 | bulle | Lyssandro | QUEUE DANS LE VIDE | — |
| 30-3 | 5 | bulle | Kilian | QUEUE DANS LE VIDE | — |
| 30-5 | 8 | bulle | Léon | QUEUE DANS LE VIDE | corps/peau 100% de 808px² |

\* Non vérifiable : la tête du locuteur n'a pas pu être identifiée avec certitude dans la vignette (châtains indissociables ou détection muette). Ces cas seront traités avec les mêmes corrections que les autres.