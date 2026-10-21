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
- Éléments recouvrant de la peau (corps nus) : **1** (dont têtes/visages couverts : 0)
- Éléments cachant un personnage (silhouette, maillot compris) : **0**
- Vignettes avec au moins un défaut : **1** sur 153

## Détail par planche et vignette

### Planche 05 — 05-premiers-sifflets

| Vignette | Él. | Type | Locuteur | Défauts |
|---|---|---|---|---|
| 5-2 | 3 | bulle | Kilian | corps/peau 56% de 677px² |

Détail chiffré dans `AUDIT-BULLES.json`.