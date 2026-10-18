# Audit des planches 23–30 — corrections partielles

> Historique de la première passe. Voir [la seconde passe](AUDIT2-23-30.md) pour l’état actuel des huit vignettes ci-dessous et les réserves restantes.

Comparaison des **40 vignettes** des huit pages du lot `6942a37` avec les originaux `e0416a5` et le témoin V2 approuvé. Les sorties de correction ont ensuite été regardées avant intégration. **Audit effectué ; corrections NON terminées.** La limite de dix générations a empêché de poursuivre ce tour. Quatre des dix sorties ont été rejetées : un résultat défectueux n'est pas collé pour donner l'impression d'avancer.

## Modifications effectivement livrées

**Trois pages modifiées : 23, 26, 30.** Six sorties générées retenues, dont une correction de fond partielle, et une restauration provisoire de l'original. 00–22, 24, 25, 27, 28 et 29 sont intégralement inchangées.

| Page et cases | Constat | Intervention et état réel |
|---|---|---|
| 23/1 | Montagnes/arbres flous, mélange dessin/photo | Nettoyage **limité au haut du fond**, par masque. Joueurs, ballon, maillots et poteaux conservés. Un montage plus large a été écarté après apparition de raccords rectangulaires visibles ; les abords des personnages restent à reprendre. |
| 23/2–4 | Fonds encore flous/texturés, incohérence avec l'encrage V2 | Non corrigés : les trois appels supplémentaires ont été refusés par la limite de génération. |
| 24/1 | Les deux garçons ont des proportions/visages trop âgés | Candidat rejeté : amélioration trop faible ; la case n'est pas modifiée. |
| 24/2–5 | Ambiance scolaire/civile, gestes et tenues principales reconnaissables ; fond encore doux par endroits | Conservées ; détails et ressemblance fine non certifiés. L'orangé de la dernière case existe dans la source, pas de conversion arbitraire en nuit ou en ciel bleu. |
| 25/1–5 | Scènes, grands groupes, équipes jaune/noir et rouge/noir reconnaissables | Conservées ; pas de défaut local suffisamment caractérisé pour justifier une nouvelle génération à l'aveugle. Comptages détaillés des figurants, visages, mains et inscriptions restent une réserve. |
| 26/3 | Le garçon à gauche, à peau brune et cheveux noirs ras, était devenu clair avec cheveux bruns plus longs | Restauration locale de ce garçon depuis un candidat guidé par l'original. **Les deux autres garçons ne sont pas régénérés.** Même case, mêmes dimensions. |
| 26/1–2 et 4–6 | Actions et causeries globalement reconnaissables ; groupes et petites anatomies denses | Conservées. La case 5 contient bien trois coachs et cinq enfants dans la source ; ne pas inventer un défaut de nombre. Petits visages/gestes non certifiés. |
| 27/1–5 | Scènes de jeu, alignement et groupe final en dessin cohérent dans l'ensemble | Conservées. Le groupe final compte bien cinq enfants ; pas de suppression basée sur un comptage erroné. Détails des mains/logos encore à contrôler finement. |
| 28/6 | Bokeh et personnages plus semi-réalistes que le témoin | Candidat **rejeté**, car il reproduit la page témoin au lieu de la vignette. Aucun élément de cette sortie contaminée n'est intégré. La case reste à reprendre. |
| 28/1–5 | Actions et équipes lisibles ; contacts complexes dans les plaquages | Conservées ; mains/visages des petites silhouettes non certifiés individuellement. |
| 29/2 | Coiffure trop haute/pointue, portrait éloigné de la source | Candidat rejeté : cheveux non corrigés et peau plus semi-réaliste. Original du lot conservé, correction encore ouverte. |
| 29/1 et 3–4 | Course, passe et essai/arbitrage reconnaissables | Conservées ; identité fine, anatomie des prises et petits figurants non certifiés. |
| 30/1 | Les enfants étaient devenus des adultes alignés ; scène d'embrassade réinventée | Nouveau candidat rejeté : tête/personnage supplémentaire dans le groupe. **Retour provisoire à l'image source**, pour supprimer la scène adulte inventée. Cette case reste photographique/tramée et **n'est pas redessinée en V2**. |
| 30/2 | Photo d'équipe d'enfants remplacée par des joueurs adultes assis | Groupe d'enfants debout, cinq enfants au premier plan et trophée rétablis. Retouche chromatique masquée de cheveux trop dorés. Rangs arrière : nombres et identités pas garantis un par un. |
| 30/3 | Identités et tenues des coachs réinventées | Trois profils source rétablis : brun à épaules rouges, gris avec barbe grise et sifflet jaune, roux à barbe rousse et partie bleue du vêtement. **Rectification du précédent bilan : le nombre était déjà trois, pas quatre.** |
| 30/4 | Maison moderne à toit plat inventée, tenue/médaille du garçon erronées | Maison à toit incliné, pierres, chemin gravillonné, tenue civile bleu/tan et geste rétablis. Recadrage isotrope d'un candidat trop large ; architecture et cadrage ne sont pas une copie exacte de la source. |
| 30/5 | Ballon transféré au fils, gestes inversés, grosse médaille et maison réinventées | Ballon rendu au père ; fils bras baissés, père bras autour du garçon ; petite médaille et tenues sombres rétablies ; toit incliné. Fidélité fine des portraits et architecture non certifiées. |

## Montage et contrôle

- Pages 23 et 26 : montages **par masques**, pas de remplacement des autres cases ou personnes.
- Page 30 : les cinq cases et le découpage avaient dérivé. Les cases sont réassemblées sur la **grille originale**, avec mise à l'échelle uniforme de l'original et centrage vertical sur le canevas existant 864 × 1232. Bordures/gouttières de cette seule page sont donc volontairement reconstruites. Ne pas annoncer leurs anciens pixels comme conservés.
- Aucun étirement différent en largeur et en hauteur. La 30/4 utilise un recadrage centré ; les autres sorties sont ajustées uniformément avec de très fines prolongations des seuls pixels de bord.
- Les tests prouvent dimensions, empreintes, périmètres et conservation de certaines régions, **pas l'anatomie ou l'identité des parties générées**.

## Reste à traiter — huit vignettes

1. **23/1** : finir le fond près des personnages.
2. **23/2** : fond.
3. **23/3** : fond.
4. **23/4** : fond.
5. **24/1** : âge/proportions des garçons.
6. **28/6** : fond et rendu des personnages.
7. **29/2** : coiffure et ressemblance.
8. **30/1** : redessiner l'original restauré, sans tête/personnage en plus.

À ces huit reprises s'ajoutent les réserves de détail mentionnées dans le tableau. **Aucune validation globale de la série.**

## Pièces et vérification

- [Avant / après, avec originaux](AUDIT-23-30-AVANT-APRES.jpg).
- [Périmètres, masques, statuts, empreintes](audit-23-30.json).

Avec Pillow :

```sh
python outils/retouche/verifier_audit23_30.py
python outils/retouche/verifier_lot23_30.py
```

Le manifeste `lot-23-30.json` reste l'inventaire historique du premier lot ; le vérificateur utilise les empreintes actuelles de `audit-23-30.json` lorsqu'il est présent.
