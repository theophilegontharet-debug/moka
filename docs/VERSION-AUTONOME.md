# Moka autonome (Vercel)

Version de lecture de Moka, indépendante de claude.ai. Elle ne consomme aucun quota Claude :
ce sont des fichiers statiques servis par Vercel.

## Ce qu'elle contient

- `site/index.html` : l'application de `app/index.html`, inchangée, plus un petit adaptateur
  qui remplace `window.claude` par la lecture de `site/data/articles.json`.
- `site/data/articles.json` : les 32 articles (16 d'origine + 16 de la relève du 7 novembre 2026),
  avec les formats Express / Comprendre / Approfondir quand ils existent. Aucun lien Gmail.
- `site/photos/` : les 14 photos Wikimedia Commons ; crédits et licences dans les articles (`image`).
- `site/icons/`, `site/manifest.webmanifest` : icônes générées depuis `app/brand/symbol.svg`.
- `site/sw.js` : cache hors ligne (photos et icônes en cache, page et données d'abord depuis le réseau).
- `site/vercel.json` : en-têtes de cache.

## Reconstruire

    python3 tools/build_site.py      # régénère site/ à partir de app/ et data/
    python3 tools/make_icons.py      # seulement si le symbole change (Playwright + Chrome)

## Déployer

Projet Vercel distinct de Continuum, relié au dépôt GitHub privé `moka` :
Framework « Other », **Root Directory : `site`**, aucune commande de build.
Chaque `git push` sur `main` redéploie.

## Favoris

Stockés dans le navigateur (`localStorage`, clé `moka.saved`). Ils restent après fermeture de
l'application sur iPhone, mais ne sont pas synchronisés entre appareils, et sont perdus si l'on
supprime l'application de l'écran d'accueil ou les données du site.

## Ce qui n'est pas dans cette version

- Collecte Gmail et rédaction par Claude : elles n'existent que dans la version Claude Artifacts
  (code conservé dans `app/index.html`, désactivé en autonome via `window.MOKA_STANDALONE`).
- Synchronisation des favoris, ajout manuel de photos, Moka Audio.

Pour les réactiver plus tard : une petite API (fonctions Vercel) avec une base (par exemple
Vercel KV ou Supabase), la clé API Anthropic côté serveur, et un transfert des newsletters
vers une adresse dédiée. L'adaptateur de `tools/build_site.py` est l'endroit à remplacer.

## Ajouter une édition à la main (sans collecte)

1. Mettre à jour `data/` (nouveaux articles au format de `data/auto-2026-11-07.json`).
2. Ajouter les photos dans `photos/` et leurs crédits dans `data/photos.json`.
3. `python3 tools/build_site.py`, vérifier `site/` localement, puis `git push`.
