# Reconstruire Moka à partir de ce dépôt

## Sur Claude Artifacts (situation actuelle)

1. Publier `app/index.html` et `app/brand/*` comme artifact (fichiers servis sous les mêmes chemins).
2. Déclarer les capacités de la page :
   ```json
   {
     "db": {"rules": [{"path": "", "read": "view", "write": "owner"},
                      {"path": "data/users/{self}", "write": "interact"}]},
     "user": {},
     "mcp": {"servers": [{"server": "Gmail", "tools": ["search_threads", "get_thread"]}]},
     "sample": {},
     "assets": {}
   }
   ```
3. Charger les articles : pour chaque entrée de `data/articles.json`, écrire `articles/<id>` avec les champs de l'article
   plus `formats` pris dans `data/formats.json` (clé = id de l'article).
4. Favoris : chaque utilisateur réimporte les siens depuis son export (« Copier mes données »). Il n'existe pas encore de bouton d'import ; à ajouter avant une vraie restauration.

## Ailleurs

L'interface fonctionne dans n'importe quel navigateur, mais tout ce qui passe par `window.claude.use(...)` doit être
remplacé : voir `ARCHITECTURE.md` (tableau des dépendances) et `MIGRATION.md`.

## Vérifier l'interface sans claude.ai

`python3 tools/preview.py`, puis ouvrir `preview/index.html`.

## Modèle de données d'un article

| Champ | Contenu |
|---|---|
| `title`, `dek`, `brief` | Titre, chapeau, résumé |
| `category`, `kind`, `score` | Rubrique, type (actu, analyse, brief), priorité |
| `event_date`, `event_label`, `published_date` | Date de l'événement, libellé, date de réception |
| `figures[]` | Chiffres clés `{v, l, n}` |
| `body[]` | Paragraphes `{h, p}` (version Comprendre) |
| `why`, `explain[]`, `moka_context`, `timeline[]`, `unknowns[]` | Enjeux, questions, contexte ajouté (signalé), suivi, inconnues |
| `items[]`, `chart` | Opérations listées, graphique simple |
| `sources[]` | `{name, via, date, gmail, web, web_label}` |
| `formats.express` | `{points[], why, figures[]}` (indices dans `figures`) |
| `formats.approfondir` | `{status: ok|court|indisponible, sections[{h,p[],refs[]}], limits[], sources[{id,name,url,date}], reason, note}` |
| `image` | Voir `IMAGES.md` ; absent = illustration Moka |
| `origin` | `claude-session` (rédigé en session) ou `auto` (relève) |
