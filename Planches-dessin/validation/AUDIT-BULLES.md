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
- Éléments recouvrant de la peau (corps nus) : **7** (dont têtes/visages couverts : 0)
- Éléments cachant un personnage (silhouette, maillot compris) : **0**
- Vignettes avec au moins un défaut : **7** sur 153

## Détail par planche et vignette

### Planche 04 — 04-nouvelles-regles

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 4-3 | 5 | bulle | Flavien | corps/peau 65% de 676px² |

### Planche 05 — 05-premiers-sifflets

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 5-2 | 3 | bulle | Kilian | corps/peau 65% de 713px² ; corps/peau 92% de 677px² |

### Planche 09 — 09-colere-et-larmes

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 9-3 | 5 | bulle | Léon | corps/peau 36% de 814px² |

### Planche 11 — 11-diagnostic-sous-la-pluie

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 11-3 | 5 | bulle | Nolann | corps/peau 44% de 736px² |

### Planche 15 — 15-la-lecon-d-un-pere

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 15-5 | 9 | bulle | Léon | corps/peau 44% de 5414px² ; corps/peau 100% de 817px² |

### Planche 16 — 16-le-pardon-des-copains

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 16-4 | 7 | bulle | Lyssandro | corps/peau 44% de 1726px² |

### Planche 28 — 28-le-choc-des-titans-rcm-vs-montmelian

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 28-3 | 3 | bulle | Lyssandro | corps/peau 43% de 900px² |

Détail chiffré dans `AUDIT-BULLES.json`.