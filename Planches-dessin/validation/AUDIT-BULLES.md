# AUDIT DU LETTRAGE — queues et recouvrements (après correction)

Audit des 30 planches de `Planches-dessin/Avec-texte/`, par `outils/lettrage/audit_bulles.py`
(locuteurs du scénario, têtes détectées Haar ×3 + filtrage peau, identités couleur calibrées
sur la couverture et nettoyées par la présence scénario, pointes de queue lues dans le
manifeste du lettrage).

Cet audit fait suite à la correction du lettrage : les queues sont désormais ancrées sur la
tête du locuteur résolu (identité + présence scénario + ordre de lecture) et le placement
évite têtes et corps. Pour comparaison, l'audit initial (commit `97cc4e5`, lettrage `0fd9784`)
comptait : **22** queues correctes, **11** mauvais locuteurs, **94** queues dans le vide,
**101** recouvrements de personnages et **107**/153 vignettes touchées ; la réplique
d'Ayden (page 14, vignette 3) manquait.

## Bilan

- Bulles et pensées auditées : **242** (réplique d'Ayden p14 v3 réintégrée)
- OK : **150**
- IMPRÉCIS : **4**
- non vérifiable : **88**
- Éléments recouvrant un personnage : **6** (dont têtes couvertes : 0)
- Vignettes avec au moins un défaut : **8** sur 153

## Détail par planche et vignette

### Planche 04 — 04-nouvelles-regles

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 4-3 | 5 | bulle | Flavien | — | corps/peau 56% de 676px² |

### Planche 10 — 10-ruminations

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 10-2 | 3 | bulle | Léon | IMPRÉCIS | — |

### Planche 11 — 11-diagnostic-sous-la-pluie

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 11-3 | 5 | bulle | Nolann | non vérifiable* | corps/peau 52% de 810px² |

### Planche 12 — 12-travail-dans-la-boue

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 12-6 | 10 | bulle | Flavien | — | corps/peau 100% de 977px² |

### Planche 15 — 15-la-lecon-d-un-pere

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 15-5 | 9 | bulle | Léon | IMPRÉCIS | corps/peau 49% de 5414px² ; corps/peau 100% de 817px² |

### Planche 16 — 16-le-pardon-des-copains

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 16-4 | 6 | bulle | Nolann | — | corps/peau 74% de 4539px² |

### Planche 21 — 21-la-plus-belle-des-victoires-de-leon

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 21-3 | 4 | bulle | Ayden | IMPRÉCIS | — |
| 21-3 | 5 | bulle | Lyssandro | IMPRÉCIS | — |

### Planche 22 — 22-le-soleil-de-mars-sur-la-motte-servolex

| Vignette | Él. | Type | Locuteur attendu | Queue | Recouvrement |
|---|---|---|---|---|---|
| 22-3 | 4 | bulle | Nolann | — | corps/peau 64% de 1511px² |

\* Non vérifiable : locuteur non détecté (ancre estimée) ou identité non isolable dans la vignette. Détail chiffré dans `AUDIT-BULLES.json`.