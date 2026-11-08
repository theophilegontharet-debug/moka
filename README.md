# Moka

Application personnelle d'actualité, centrée sur l'investissement et l'économie africaine.
Projet entièrement indépendant de Continuum : aucun code, aucune donnée, aucun service partagé.

## État au 7 novembre 2026

| Élément | État |
|---|---|
| Application (une page HTML) | En ligne comme Claude Artifact, privée |
| 16 articles, 3 formats de lecture | En base, vérifiés |
| Favoris, format préféré | Par utilisateur, privés |
| Relève Gmail dans l'app | Développée, **jamais exécutée en conditions réelles** |
| Conversion HTML (PitchBook) | Développée et testée sur un vrai email |
| Photos automatiques | Conçu, non opérationnel (voir `docs/IMAGES.md`) |
| Collecte quotidienne automatique | Proposée, non mise en place (voir `docs/COLLECTE.md`) |
| Audio | Conception uniquement (voir `docs/AUDIO.md`) |

## Contenu du dépôt

```
app/index.html        L'application (HTML, CSS et JS dans un seul fichier)
app/brand/            Logo : symbole, icône, versions horizontale et empilée (SVG)
data/articles.json    Les 16 articles (copie de la base, sans adresse email)
data/formats.json     Versions Express et Approfondir de chaque article
tools/                Scripts de génération des données, captures d'écran, prototype d'images
docs/                 Architecture, reconstruction, migration, images, collecte, audio
```

## Ce que ce dépôt ne contient pas, volontairement

- Aucun identifiant, jeton ou clé.
- Aucune adresse email ni lien Gmail dans les données publiées.
- Les favoris (privés, lisibles uniquement par leur propriétaire). Pour les récupérer : bouton « Copier mes données » de la page Sources.

## Lancer en local

`app/index.html` s'ouvre dans un navigateur, mais sans base de données ni connecteur : hors de claude.ai,
la page affiche « Moka ne peut pas joindre sa base ». `python3 tools/preview.py` produit un aperçu avec les données du dépôt.
Voir `docs/ARCHITECTURE.md` pour la liste des dépendances à Claude Artifacts.

## Version autonome (Vercel)

`site/` contient une version de lecture indépendante de claude.ai : 32 articles, 14 photos,
favoris locaux, installable sur l'écran d'accueil de l'iPhone. Voir `docs/VERSION-AUTONOME.md`.
