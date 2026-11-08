# Écrire un script oral pour Aoede (Google Chirp 3 HD)

Version provisoire (8 novembre 2026), à confirmer après écoute des essais de diction (`/audio/tests/`).

## Fond
- Ne reprendre que les faits, chiffres et nuances de l'article (corps, chiffres clés, « pourquoi ça compte »,
  inconnues, analyse approfondie). Aucun fait nouveau ; une explication de terme est permise si elle est exacte.
- Garder les incertitudes et les limites (« Moka n'a pas pu établir… »).
- Ne pas allonger : la durée suit le contenu de l'article.

## Forme
- Une idée par phrase ; phrases de 10 à 25 mots. Les deux-points au milieu d'une phrase créent des
  pauses de lecture : préférer deux phrases.
- Apostrophes typographiques (’) partout : l'apostrophe droite (') peut provoquer une coupure
  (« jusqu' / à ») ou la lecture de la lettre seule (« de elle équipe » pour « de l'équipe »).
  À vérifier à l'écoute ; si c'est confirmé, le générateur les convertira automatiquement.
- Nombres : en toutes lettres pour les montants et les décimales (« onze virgule deux fois »),
  ou arrondis quand la précision n'apporte rien à l'oral (« plus de onze fois »). Pas de
  « 11,2 fois » en chiffres : Aoede marque une pause avant « fois ».
- Unités et symboles écrits en mots (« millions de dollars », « pour cent »), sigles expliqués
  à la première occurrence (« introduction en Bourse », « fonds de capital-risque »).
- Éviter les tournures qui coupent un groupe de mots : préférer « au plus haut de la séance, le titre
  gagnait dix-huit pour cent » à « le titre a pris jusqu'à dix-huit pour cent ».
- Ouvrir par le titre, finir par « Pourquoi ça compte » puis « Ce qu'on ne sait pas encore ».

## Contrôle
1. Relire le script contre l'article : chaque chiffre doit y figurer.
2. Générer d'abord un court essai pour toute tournure douteuse (`audio/tests/passages.json`, action
   « Essais de diction Moka », plafond 3 000 caractères).
3. Générer la narration (action « Narrations Moka Audio »), avec un plafond par lancement.
