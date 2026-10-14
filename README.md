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
- `personnages/*réel*` : photos réelles de référence des personnages (à déposer par l'auteur ; voir directives ci-dessus).
- `personnages/Maison saint sulpice.png` : photo réelle de la maison familiale (référence des extérieurs).
- [`scenario/scenario-complet-30-pages.md`](scenario/scenario-complet-30-pages.md) : découpage intégral page par page et vignette par vignette (Couverture + Pages 1 à 30) avec tous les dialogues, bulles de pensée, encadrés narratifs et effets sonores. Les mentions « comics » du scénario (titrage Marvel, trames) sont à transposer en réaliste ; le découpage et les dialogues restent la référence.
- `planches/` : planches réalistes en cours (dessin sans bulles validé + version lettrée finale).
- `outils/lettrage/` : police Kalam (licence OFL) et scripts de lettrage déterministes (Pillow) des planches réalistes.

## 🖨️ Format du livre

- Couverture et 30 pages : **A4 portrait (210 × 297 mm), 2480 × 3508 pixels à 300 dpi**.
- Illustration complète conservée, sans déformation ni recadrage ; marges blanches si le ratio diffère.

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
