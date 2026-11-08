# Images : une solution durable

## Constat (vérifié le 7 novembre 2026)

- La page Moka **ne peut pas afficher une image hébergée ailleurs** (politique de sécurité des Artifacts), ni interroger une API d'images.
- La session de travail de Claude **ne peut pas télécharger** depuis Wikimedia Commons : connexion refusée par le proxy (`403`). Les domaines sont autorisables dans les paramètres claude.ai.
- Une session Claude **peut** ajouter un fichier aux assets de Moka (`upload_asset`) puis inscrire ses métadonnées dans la base (`db_write`). Ce chemin n'a pas encore été testé de bout en bout.
- Le bouton manuel « Ajouter une photo » existe dans l'app, en secours.

## Pipeline proposé (identique en trajectoire A ou B)

Pour chaque nouvel article, dans cet ordre :

1. **Photo du sujet** : entreprise, fondateur, produit, site industriel. Recherche par nom exact d'entité dans Wikimedia Commons ; pour les entreprises, kit presse officiel uniquement s'il précise des conditions de réutilisation.
2. **Photo de contexte** : lieu, secteur, infrastructure (ex. la Bourse du Caire pour une IPO égyptienne). Wikimedia Commons, puis Unsplash.
3. **Illustration Moka** si rien de pertinent.

Règles :

- Licences acceptées sur Commons : domaine public, CC0, CC BY, CC BY-SA. Refusées : NC, ND, « fair use », licence inconnue.
- Unsplash : API officielle uniquement, affichage du nom du photographe et lien vers son profil et Unsplash, appel de suivi de téléchargement exigé par leurs conditions.
- Jamais Google Images ni photos de sites de presse.
- Une photo de contexte porte toujours la mention **« Photo d'illustration »** ; seule une photo du sujet lui-même peut s'afficher sans cette mention.
- Pas de portrait d'une personne si l'article ne parle pas d'elle.
- Vérification visuelle avant publication : Claude regarde la miniature et rejette ce qui ne correspond pas (logo seul, mauvaise entreprise homonyme, image trop générique).

## Métadonnées enregistrées (champ `image` de l'article)

```json
{
  "asset": "id de l'asset Moka",
  "kind": "sujet | contexte",
  "alt": "Description de l'image",
  "credit": "Auteur",
  "license": "CC BY-SA 4.0",
  "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
  "source_url": "Page de l'image sur Commons ou Unsplash",
  "provider": "wikimedia | unsplash | officiel | manuel",
  "query": "Requête qui l'a trouvée",
  "added_at": "date"
}
```

L'app affiche déjà « Photo d'illustration · auteur · licence · source » quand `kind` vaut `contexte`.

## Prototype

`tools/images/find_images.py` implémente la recherche Commons avec filtrage des licences et la recherche Unsplash.
**Non testé** : le réseau de la session de travail n'a pas accès à ces sites.

## Procédure utilisée le 7 novembre 2026 (14 photos)

1. `commons.py requetes.json resultats.json` : recherche Wikimedia Commons (une requête toutes les ~12 s, respect du `Retry-After`).
   Ne garder que CC0, domaine public, CC BY, CC BY-SA. Aucun portrait de personne publique.
2. `batch.py choix.json` : télécharge la miniature standard (jamais l'original : Wikimedia le refuse aux robots),
   recadre les formats extrêmes, redimensionne à 1 400 px, JPEG qualité 80.
3. Vérifier chaque image à l'œil (pertinence, pas de données personnelles visibles).
4. `upload_asset` sur l'artifact, puis `ops.py` génère les mises à jour du seul champ `image`
   (asset, kind photo/contexte, caption, crédit, licence + lien, obligations, modifications, source).
5. Retour arrière : remettre `image` à `null` sur l'article.
Le détail des 14 photos retenues est dans `tools/images/photos-2026-11-07.json`.
