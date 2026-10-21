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
- Éléments recouvrant de la peau (corps nus) : **3** (dont têtes/visages couverts : 0)
- Éléments cachant un personnage (silhouette, maillot compris) : **0**
- Boîtes recouvrant une zone dense du dessin (avertissement) : **13**
- Vignettes avec au moins un défaut : **2** sur 153

## Détail par planche et vignette

### Planche 11 — 11-diagnostic-sous-la-pluie

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 11-3 | 3 | bulle | Lyssandro | corps/peau 39% de 1306px² |
| 11-3 | 5 | bulle | Nolann | corps/peau 53% de 736px² |

### Planche 15 — 15-la-lecon-d-un-pere

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 15-4 | 5 | bulle | Flavien | corps/peau 50% de 14501px² |

Détail chiffré dans `AUDIT-BULLES.json`.