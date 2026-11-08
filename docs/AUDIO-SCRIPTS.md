# Écrire un script oral pour Aoede (Google Chirp 3 HD)

Mise à jour du 8 novembre 2026. Les règles « à confirmer » attendent l'écoute de `/audio/tests-2/`.

## Ce que Chirp 3 HD permet (documentation Google)
- **Écriture et ponctuation** : point = pause franche ; virgule = pause courte ; points de suspension =
  pause longue et appuyée ; tiret = brève coupure. Phrases courtes et langage parlé recommandés.
- **Balises de pause** `[pause short]`, `[pause]`, `[pause long]` dans le champ `markup` (pas `text`) ;
  le modèle peut les ignorer si elles sont mal placées.
- **Vitesse** `speakingRate` (0,25 à 2) : sur un passage entier, pas phrase par phrase.
- **Prononciations imposées** (`customPronunciations`, alphabet phonétique IPA) pour un mot précis.
- **SSML** en préversion seulement.
- **Aucun réglage d'émotion ou de style** : l'enthousiasme, la surprise ou la gravité ne passent que par
  l'écriture (mots, longueur des phrases, ponctuation) et par l'interprétation propre de la voix.

## Règles automatiques (outils)
- Apostrophes droites converties en apostrophes typographiques avant l'envoi (`narrate.py`, `tests.py`).

## Fond
- Uniquement les faits, chiffres, incertitudes et nuances de l'article. Une explication de terme est
  permise si elle est exacte. Pas de contexte ni de réaction qui ne découle pas des sources.
- Les réactions (« Oui, tu as bien entendu », « c'est énorme ») seulement quand le fait le justifie,
  au plus une ou deux par narration. Jamais sur un chiffre dont on ne connaît pas le contexte.
- Sujets humains (suppressions de postes, faillites) : phrases plus courtes, pas d'enthousiasme,
  mention sobre du coût humain.
- Ne pas allonger : la durée suit le contenu de l'article.

## Forme
- Tutoiement, phrases de 8 à 20 mots, une idée par phrase.
- Transitions variées, jamais deux fois la même dans une narration : « Concrètement, ça veut dire
  quoi ? », « Autrement dit », « Mais attention, il y a une nuance importante », « Et c'est là que ça
  devient intéressant », « Ah, et autre chose ».
- Pas de deux-points au milieu d'une phrase longue ; points de suspension réservés à un vrai suspense.
- Éviter les élisions sensibles quand une tournure simple existe (« de son équipe » plutôt que
  « de l'équipe ») — à confirmer.
- Décimales : garder la précision sans virgule parlée quand c'est possible (« un peu plus de onze
  fois » pour 11,2) ; sinon en toutes lettres. Pas de chiffres décimaux en chiffres.
- Unités en mots (« millions de dollars », « pour cent ») ; sigles expliqués à la première occurrence.
- Interjections (« Bon… », « euh », « Tu sais quoi ? ») : à confirmer à l'écoute.

## Formats
- **Express** : flash de 30 à 60 secondes, l'essentiel et au plus une réaction.
- **Comprendre** : chroniqueuse ; mécanismes expliqués, transitions, enjeux, adresse directe.
- **Approfondir** : plus analytique et posé ; construit un raisonnement à partir de l'analyse de l'article.

## Contrôle
1. Relire le script contre l'article : chaque chiffre doit y figurer.
2. Toute tournure douteuse passe d'abord par un essai court (action « Essais de diction Moka »).
3. Narration générée ensuite (action « Narrations Moka Audio »), avec un plafond par lancement.
