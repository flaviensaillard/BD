# AUDIT DU LETTRAGE — locuteurs nommés, fonds et recouvrements

Audit des 30 planches de `Planches-dessin/Avec-texte/`, par
`outils/lettrage/audit_bulles.py`. Le lettrage ne pointe plus les
locuteurs : chaque dialogue est préfixé du nom du personnage
(« Léon: "…" ») sur fond blanc, la narration est sur fond
jaune/brun. Contrôles : préfixe conforme au scénario, fond de la
boîte (échantillonné sur la planche finale), recouvrement des
personnes (têtes et zones de peau, détection indépendante).

## Bilan

- Dialogues (bulles, pensées, voix, cris) : **246**, encadrés narratifs : **24**
- Préfixes de locuteur faux : **0**
- Fonds non conformes (blanc/dialogue, jaune-brun/narratif) : **0**
- Éléments recouvrant un personnage : **7** (dont têtes/visages couverts : 0)
- Vignettes avec au moins un défaut : **5** sur 153

## Détail par planche et vignette

### Planche 05 — 05-premiers-sifflets

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 5-2 | 3 | bulle | Kilian | corps/peau 65% de 713px² ; corps/peau 92% de 677px² |

### Planche 15 — 15-la-lecon-d-un-pere

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 15-4 | 5 | bulle | Flavien | corps/peau 54% de 14501px² |
| 15-4 | 6 | bulle | Flavien | corps/peau 54% de 14501px² |

### Planche 16 — 16-le-pardon-des-copains

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 16-4 | 6 | bulle | Nolann | corps/peau 47% de 4160px² |
| 16-4 | 7 | bulle | Lyssandro | corps/peau 44% de 1726px² |

### Planche 22 — 22-le-soleil-de-mars-sur-la-motte-servolex

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 22-3 | 4 | bulle | Nolann | corps/peau 43% de 488px² ; corps/peau 57% de 1511px² |

### Planche 25 — 25-le-grand-tournoi-final

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 25-2 | 2 | bulle | Léon | corps/peau 35% de 476px² |

Détail chiffré dans `AUDIT-BULLES.json`.