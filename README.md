# 🏉 LA FORCE DE L'ÉCHEC
> *« On apprend de ses échecs, c'est ce qui conduit à la victoire »*

Bande dessinée de 30 pages en **style réaliste** créée pour **Léon** (6 ans), suivant la saison U8 du **Rugby Club Motterain (RCM)** à **La Motte-Servolex** et la vie à **Saint-Sulpice** en Savoie (saison Septembre 2026 – Juin 2027).

---

## 🔁 Bascule en style réaliste (14 octobre 2026) — directives en vigueur

Décisions prises avec l'auteur, qui remplacent toutes les consignes « comics » antérieures :

1. **Style** : rendu **réaliste / photoréaliste**. On ne fait plus de comics (plus de trait encré, plus de trames, plus de titrage Marvel).
2. **Personnages** : on utilise les **photos réelles** des personnages, **telles quelles**, comme **référence visuelle de visage et de morphologie** pour générer les cases (poses, décors et actions du scénario). Ce n'est pas du photomontage : les photos ne sont pas découpées ni incrustées.
3. **Nommage des photos** : les photos réelles portent un nom qui **se termine par « réel »** (ex. `personnages/Léon réel.png`). Les anciens portraits comics (`Léon.png`, `Flavien.png`, …) ne servent **plus** de référence.
4. **Références visuelles par génération** : uniquement les photos « réel » des personnages présents dans la page, plus la photo `personnages/Maison saint sulpice.png` pour les extérieurs de la maison. Ne plus joindre la couverture comics ni les anciennes planches.
5. **Reprise** : on refait **tout depuis la couverture** (page 0 → page 30) pour un livre homogène. Les versions comics validées (couverture + planches 1 à 9) sont **archivées** dans [`planches/archive-comics/`](planches/archive-comics/) avec leurs scripts dans [`outils/lettrage/archive-comics/`](outils/lettrage/archive-comics/).
6. **Processus inchangé** : deux propositions de dessin **sans bulles** → validation par l'auteur → **lettrage manuel** (police Kalam, bulles, encadrés, onomatopées) → validation finale. Export **A4 portrait, 2480 × 3508 px à 300 dpi**.
7. **Refus** : par défaut, un refus de proposition signifie que les personnages ou la charte ne sont pas respectés. Ne pas redemander le motif ; l'auteur précisera spontanément toute autre raison.
8. **Outil de génération** : l'auteur autorise l'outil disponible pour toutes les pages, sans garantie sur le modèle utilisé. Inutile de redemander l'autorisation.
9. **Session** : interdiction de clore la session.

## 📂 Structure du dépôt

- [`personnages/charte-personnages-et-equipes.md`](personnages/charte-personnages-et-equipes.md) :
  - Charte physique et caractère des **5 joueurs principaux** (**Léon**, **Lyssandro**, **Ayden**, **Nolann**, **Milo**) au sein de l'effectif de 20 joueurs U8 (4 équipes de 5).
  - Charte des **3 coachs** (**Flavien** père de Léon, **Julien** père de Lyssandro, **Kilian**).
  - Personnages évoqués hors-champ (**Vanessa**, **Alice**, **Baptiste**).
  - Règlement officiel du rugby U8 (terrain 30m x 20m, 5 contre 5, 1 essai = 1 point sans poteaux ni transformations, touche rendue et jouée comme une pénalité, en-avant et hors-jeu comptés, touché à 2 mains jusqu'en novembre puis plaquages autorisés dès décembre).
  - Couleurs officielles du **RCM** (Rouge, Bleu et Blanc — *Locaself*) et des **7 équipes adverses** (Montmélian, Chambéry, Aix-les-Bains, Albertville, Le Môle, Rumilly, Thonon).
  - Règle vestimentaire stricte : tenue de rugby uniquement aux entraînements et tournois ; tenue civile à la maison et à l'école.
- `personnages/<Prénom> réel.jpg` : photos réelles de référence des 8 personnages (Léon, Lyssandro, Ayden, Nolann, Milo, Flavien, Julien, Kilian). Fournies par l'auteur le 14 octobre 2026 ; description détaillée dans la charte (section 2 bis).
- `personnages/Maison saint sulpice.png` : photo réelle de la maison familiale (référence des extérieurs).
- [`scenario/scenario-complet-30-pages.md`](scenario/scenario-complet-30-pages.md) : découpage intégral page par page et vignette par vignette (Couverture + Pages 1 à 30) avec tous les dialogues, bulles de pensée, encadrés narratifs et effets sonores. Les mentions « comics » du scénario (titrage Marvel, trames) sont à transposer en réaliste ; le découpage et les dialogues restent la référence.
- `planches/` : planches réalistes en cours (dessin sans bulles validé + version lettrée finale).
- `outils/lettrage/` : police Kalam (licence OFL) et scripts de lettrage déterministes (Pillow) des planches réalistes.

## 🖨️ Format du livre

- Couverture et 30 pages : **A4 portrait (210 × 297 mm), 2480 × 3508 pixels à 300 dpi**.
- Illustration complète conservée, sans déformation ni recadrage ; marges blanches si le ratio diffère.

## Méthode de fabrication des pages réalistes (mise au point sur la couverture, 14 octobre 2026)

Les générations « tout-en-un » à 8 personnages ont été refusées trois fois (doublons, visages inventés, corps tronqués). La méthode retenue, validée techniquement sur la couverture :

1. **Décor seul** généré sans personne (`planches/travail/<page>/fond-*.png`).
2. **Chaque personnage généré individuellement, en pied, sur fond gris uni**, avec deux références : son gros plan `personnages/portraits-reels/<Prénom>.jpg` (identité) et sa photo en pied `personnages/<Prénom> réel.jpg` (tenue, gabarit). Visage grand dans l'image ⇒ meilleure ressemblance. Contrôle de ressemblance par comparaison côte à côte avant usage ; on régénère si besoin.
3. **Détourage** automatique (`outils/assemblage/detourage.py` (segmentation MediaPipe + clé couleur signée : le tissu clair devient opaque, les ombres au sol sont rejetées ; les membres détachés — bras levés — et les objets tenus sont conservés) : segmentation MediaPipe + clé colorimétrique sur fond local) et **assemblage par calcul** (`outils/assemblage/couverture.py` : perspective simple, taille réelle de chaque personne, ombres de contact, harmonisation légère) directement en **A4 2480 × 3508 à 300 dpi**. Résultat garanti : exactement les bons personnages, une seule fois chacun, corps entiers.
4. Lettrage manuel ensuite, comme avant (police Kalam).

Environnement : `outils/setup-env.sh` (à relancer si le bac à sable a été réinitialisé). Limite de l'outil : 10 générations d'images par tour.

## Couverture réaliste — en attente de validation

- Décor : `planches/travail/couverture/fond-jour.png` (stade de La Motte-Servolex, lumière douce de fin d'après-midi, choix de l'auteur).
- Personnages générés : `planches/travail/couverture/perso-*.png` (Léon : `perso-leon.png` v1 et `perso-leon-v2.png` v2 retenue ; une v3 est prévue au prochain tour, la limite de générations ayant été atteinte).
- Deux propositions sans texte soumises à l'auteur : [`planches/00-couverture-dessin-A.png`](planches/00-couverture-dessin-A.png) (deux rangées) et [`planches/00-couverture-dessin-B.png`](planches/00-couverture-dessin-B.png) (formation en V, Léon en pointe) ; comparatif `planches/travail/couverture/comparatif-A-B.jpg`.
- Titre et sous-titre seront ajoutés au lettrage, dans le ciel (haut) et sur la pelouse (bas).

## Planche 1 réaliste — en attente de validation

- Proposition de dessin sans texte : [`planches/01-la-legende-des-u6-dessin.png`](planches/01-la-legende-des-u6-dessin.png) (aperçu `-apercu.jpg`), assemblée par `python3 outils/assemblage/planche01.py`.
- Mise en page reprise du gabarit validé en comics : grande case haute (célébration du trophée, 8 personnages, confettis dorés, stade ensoleillé du flashback printemps 2026), puis trois cases étroites : Lyssandro ballon en main suivi d'Ayden et Milo / médailles d'or autour du cou (cadrage sous les épaules, sans visage) / gros plan sur le regard de Léon.
- Éléments générés : `planches/travail/planche01/` (`fond-case1.png`, `perso-leon-trophee.png`, `perso-nolann-joie.png`, `perso-*-course.png`, `case3-medailles-v2.png`, `case4-leon-regard.png`) ; les poses debout de la couverture (`planches/travail/couverture/perso-*.png`) sont réutilisées en case 1.
- Lettrage à faire après validation : encadré jaune « SAISON DERNIÈRE… », bulles de Léon et Nolann (case 1), voix de Léon + bulle de Milo (case 2), bulles Lyssandro/Ayden (case 3), bulle de Léon (case 4) — textes dans `scenario/scenario-complet-30-pages.md`.

## Planches réalistes validées

*(aucune pour l'instant — reprise depuis la couverture)*

## 🗄️ Archive comics (versions antérieures, conservées pour mémoire)

Couverture et planches 1 à 9 validées en style comics avant la bascule, dans [`planches/archive-comics/`](planches/archive-comics/) :

- Couverture : `00-couverture.png` (source `00-couverture-source.png`).
- Planche 1 — La Légende des U6 : `01-la-legende-des-u6.png` (source `01-source.png`).
- Planche 2 — Matin de rentrée à Saint-Sulpice : `02-matin-de-rentree.png` (source `planches-02-source.png`).
- Planche 3 — Les 20 Guerriers du RCM : `03-les-20-guerriers-du-rcm.png` (dessin `03-les-20-guerriers-dessin.png`).
- Planche 4 — Nouvelles Règles, Nouveau Monde : `04-nouvelles-regles.png` (source `planches-04-source.png`).
- Planche 5 — Premiers Sifflets & Conseil des Coachs : `05-premiers-sifflets.png` (dessin `05-premiers-sifflets-dessin.png`).
- Planche 6 — Deux Victoires pour Commencer ! : `06-deux-victoires.png` (source `planches-06-source.png`).
- Planche 7 — Le Mur Vert et Noir de Montmélian : `07-mur-vert-et-noir.png` (dessin `07-mur-vert-et-noir-dessin.png`).
- Planche 8 — L'Action Individuelle de Trop : `08-action-individuelle.png` (dessin `08-action-individuelle-dessin.png`).
- Planche 9 — La Colère et les Larmes : `09-colere-et-larmes.png` (dessin `09-colere-et-larmes-dessin.png`).

Les scripts de lettrage correspondants (`outils/lettrage/archive-comics/planche01.py` … `planche09.py`) ont été adaptés aux nouveaux chemins et restent exécutables (`python3 outils/lettrage/archive-comics/planche09.py`). Les anciens portraits comics (`personnages/Léon.png`, etc.) et `Maison-saint-sulpice-comics.png` sont conservés mais ne servent plus de référence.
