# Collecte des actualités

## État réel

| Élément | État |
|---|---|
| Bouton « Relever les newsletters » (page Sources) | Développé, **jamais exécuté** : il doit être lancé par vous dans claude.ai, car il demande votre accord pour Gmail et pour Claude |
| Lecture texte des newsletters | Développée |
| Conversion HTML → texte (PitchBook et autres) | Développée, **testée** sur The Daily Pitch du 6 novembre : 192 Ko de HTML → 13 Ko de texte propre |
| Regroupement avec un article existant | Développé : Claude reçoit la liste des articles (titre, date, entités) et peut fusionner une source |
| Garde-fou sur les dates | Développé : un événement de plus de 30 jours avant la réception n'est pas publié comme actualité ; une date d'événement postérieure à la réception est ramenée à la réception |
| Format Express pour les nouveaux articles | Généré automatiquement |
| Format Approfondir pour les nouveaux articles | Marqué « indisponible » : aucune recherche complémentaire automatique pour l'instant |
| Automatisation quotidienne | Non mise en place |

## Premier test à faire (vous)

1. Ouvrir Moka dans claude.ai → Sources → « Relever les newsletters ».
2. Accepter les demandes d'accès (Gmail, Claude).
3. Le journal affiche chaque newsletter traitée. Me transmettre le résultat, surtout en cas d'erreur.

## Automatisation quotidienne proposée (trajectoire A)

Une tâche planifiée Claude, chaque matin vers 6 h :

1. Cherche les fils du libellé `Moka/Newsletters` des dernières 36 heures absents de `meta/ingest`.
2. Lit chaque email (texte, ou HTML converti).
3. Sélectionne les informations importantes selon vos priorités, rédige Comprendre et Express ; Approfondir seulement si une recherche web trouve des sources supplémentaires vérifiables.
4. Regroupe les doublons (même entreprise, même montant, dates proches) et ajoute les sources.
5. Cherche une image (voir `IMAGES.md`) si les domaines sont autorisés.
6. Écrit dans la base de Moka et met à jour `meta/ingest`.

Avantage : même qualité de rédaction que les 16 articles actuels, avec recherche web pour Approfondir.
À créer seulement après votre accord.

## Sources web et RSS

À ajouter progressivement, dans la tâche planifiée (trajectoire A) ou dans un Worker (trajectoire B), puisque la page ne peut pas lire de flux elle-même :

- **Agence Ecofin** : expéditeur à identifier dans Gmail, ou flux RSS du site s'il existe.
- **Energy Investor Weekly** : en attente du premier email.
- Médias et sites institutionnels : liste à établir ensemble.
