# Audit et corrections — planches 13 à 22

> Historique de la première passe. Le relumage de 18/19 décrit ici a été jugé trop sombre et annulé lors du [second audit](AUDIT2-13-22.md), qui décrit l’état actuel et les réparations supplémentaires.

Comparaison des dix pages du lot `2dc42ff` avec les originaux du commit `e0416a5` et avec le témoin V2 validé. Il s'agit d'une passe de contrôle et de correction, **pas d'une validation parfaite de chaque détail**. Les pages 23–30 restent inchangées.

## Résultats par page

| Page | Écart constaté | Intervention | Réserves restantes |
|---|---|---|---|
| 13 | Première case devenue ensoleillée alors que la source est couverte | Ciel gris rétabli ; premier essai rejeté car ses nuages étaient photographiques, second essai en formes graphiques intégré | Éclairage/météo des autres cases à réexaminer ; détails des personnes et du terrain non garantis à l'identique |
| 14 | Personnages lointains et feuillage encore photographiques dans la première case | Case 1 reprise avec fond et adversaires dessinés | Petits logos et lettrages non fiabilisés |
| 15 | Cheveux du garçon trop blonds dans cinq représentations | Correction chromatique masquée du blond doré vers le châtain clair ; aucune régénération des visages, des coupes ou des vêtements | La teinte finale est une correction visuelle, pas une mesure colorimétrique de la photographie éclairée en intérieur |
| 16 | Cinq coachs dans la dernière case au lieu des trois originaux | Dernière case reconstruite avec trois adultes et cinq garçons | Finesse du traitement des petits visages et du décor à réexaminer ; cette case n'est pas une validation définitive d'identité |
| 17 | Neige au sol plus étendue que dans les sources | Aucune modification dans cette passe | Écart de décor à reprendre ; nombre/identité des figurants du grand groupe non certifiés individuellement |
| 18 | La scène du soir a été transformée en plein jour dans les six cases | Éclairage nocturne/bleu du soir rétabli sur les six cases, découpage conservé | Variations fines des visages et des textures non exclues par cette retouche générative |
| 19 | Les trois premières cases sont passées du soir au jour | Éclairage du soir rétabli sur les cases 1–3 ; cases 4–5 conservées car leurs sources sont plus claires | Visages, cheveux et petits diagrammes peuvent encore différer des originaux |
| 20 | Un grand coach roux a été ajouté au premier plan de la case 3 | Suppression locale par masque et reconstitution du terrain ; candidats génératifs non utilisés pour les joueurs car leur cadrage/dessin dérivait | Sol gelé moins étendu que dans la source, à réexaminer ; le reste de la case n'a pas été régénéré |
| 21 | Gros plan avec cheveux trop hauts et trop foncés | Coiffure abaissée et éclaircie, visage repris dans la case 1 | Couverture neigeuse plus importante que dans la source et ressemblance exacte à contrôler encore |
| 22 | Décor photographique derrière la scène de passe de la case 4 | Fond redessiné en montagnes et feuillages encrés | Petites variations des personnages et des marquages non exclues |

## Méthode et limites

- Dix générations utilisées : six premières corrections locales, deux essais de relumage, puis deux reprises (13 et 20). La sortie générative finale de 20 n'a pas été utilisée pour redessiner les joueurs.
- Les corrections locales sont assemblées dans leurs rectangles d'origine, sans régénérer les autres cases.
- Sur 15, tous les pixels hors du masque chromatique sont conservés. Sur 20, tous les pixels hors du masque de suppression sont conservés : les joueurs, le petit coach d'origine au bord gauche et leurs vêtements ne sont pas redessinés.
- Sur 18, les six rectangles de cases sont repris d'un candidat de relumage ; bordures, marges et gouttières sont conservées. Sur 19, seules les trois premières cases sont reprises du candidat.
- Les dimensions des pages restent identiques à celles du lot généré. Il n'y a pas de promesse de master A4 natif : les corrections générées sont rééchantillonnées dans les cases.
- Une différence pixel à pixel nulle hors zone prouve la localité du montage, pas la fidélité des personnes à l'intérieur d'une zone générée. Les sorties ont été inspectées visuellement avant intégration, sans pouvoir certifier chaque visage de figurant.
- Les petits blasons, sponsors, textes et détails de diagrammes restent des écarts possibles. Ils ne sont pas annoncés comme corrigés.

## Vérification reproductible

Rapport des zones : [`audit-13-22.json`](audit-13-22.json).

Avec Pillow installé :

```sh
python outils/retouche/verifier_audit13_22.py
```

Le test compare les images au lot `2dc42ff`, vérifie leurs dimensions et l'absence de changements hors des cases ou masques autorisés. La planche 17 doit rester intégralement identique.
