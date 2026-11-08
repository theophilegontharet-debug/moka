# Architecture actuelle et dépendances

## Ce qui constitue réellement Moka aujourd'hui

| Couche | Où elle vit | Exportable ? |
|---|---|---|
| Interface (HTML/CSS/JS, logo, illustrations générées) | `app/index.html`, fichiers de l'artifact | Oui, entièrement (ce dépôt) |
| Articles (16 documents `articles/<id>`) | Base de l'artifact | Oui : `data/articles.json` + `data/formats.json`, ou bouton « Copier mes données » |
| Favoris et format préféré | `data/users/<id>/state`, privé à chaque utilisateur | Seulement par l'utilisateur lui-même (bouton d'export) ; même le propriétaire ou Claude ne peuvent pas les lire |
| Journal de relève | `meta/ingest` | Vide à ce jour (aucune relève exécutée) |
| Photos ajoutées | Assets de l'artifact | Aucune à ce jour |

## Fonctions qui dépendent de Claude Artifacts

Chacune passe par `window.claude.use(...)`, qui n'existe que dans une page servie par claude.ai.

| Capacité | Rôle dans Moka | Hors de claude.ai |
|---|---|---|
| `db` | Lire et écrire les articles, favoris, journal | À remplacer par une base (ex. Cloudflare D1, Supabase) |
| `user` | Identifier l'utilisateur, savoir s'il est propriétaire | À remplacer par une authentification |
| `mcp` → connecteur Gmail | Relève : `search_threads`, `get_thread` | **Non transférable.** Le connecteur appartient au compte claude.ai. Il faut une intégration Gmail propre (OAuth Google) ou un transfert d'emails (voir `MIGRATION.md`) |
| `sample` | Faire rédiger les articles par Claude dans la page | À remplacer par l'API Anthropic côté serveur, avec une clé jamais exposée au navigateur |
| `assets` | Stocker les photos ajoutées | À remplacer par un stockage de fichiers (ex. R2, S3) |

## Contraintes de l'environnement Artifacts qui limitent le produit

- **Images distantes bloquées** : la page ne peut afficher que ses propres fichiers, ses assets ou des images `data:`/`blob:`. Une photo de Wikimedia ou d'Unsplash doit donc être copiée dans les assets avant d'être affichée.
- **Pas de requête réseau depuis la page** vers d'autres sites : impossible d'interroger Wikimedia, Unsplash ou un flux RSS depuis Moka.
- **Pas d'exécution en arrière-plan** : la page ne fait rien quand elle est fermée. Une collecte quotidienne doit être lancée ailleurs (tâche planifiée Claude, ou serveur indépendant).
- **Audio** : lecture possible après un geste de l'utilisateur ; le comportement écran verrouillé dans l'app Claude n'est pas garanti.

## Indépendance vis-à-vis de Continuum

Vérifié : aucune référence à Continuum dans le code, les données ou la configuration. Le seul dépôt GitHub visible
depuis la session de travail est `continuum` ; il n'a été ni lu ni modifié.
