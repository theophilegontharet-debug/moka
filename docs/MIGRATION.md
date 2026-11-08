# Sauvegarde et migration : plan

Aucune étape qui modifie l'hébergement ou le fonctionnement actuel n'est lancée sans accord explicite.

## Étape 0 : sauvegarde (sans risque)

1. Créer sur GitHub un dépôt **privé et vide** nommé `moka` (sans README).
2. Y pousser ce dépôt. Il ne contient ni secret ni adresse email (vérifié par recherche automatique).
3. Exporter ses favoris depuis l'app : Sources → « Copier mes données », coller dans un fichier conservé hors du dépôt.

La version en ligne n'est pas touchée.

## Trois trajectoires possibles

### A. Rester sur Claude Artifacts et l'enrichir (recommandé à court terme)

- Garde tout ce qui fonctionne : base, favoris, connecteur Gmail, rédaction par Claude.
- Collecte quotidienne : une **tâche planifiée Claude** relève les newsletters chaque matin, rédige les trois formats et écrit dans la base de Moka.
- Photos : la même tâche cherche des images libres de droits et les ajoute aux assets de Moka. **Condition** : autoriser dans claude.ai (Paramètres → Capacités → domaines autorisés) `commons.wikimedia.org`, `upload.wikimedia.org`, et pour Unsplash `api.unsplash.com`, `images.unsplash.com`. Sans cela, la session de travail ne peut pas télécharger d'images.
- Limites : dépendance à claude.ai ; audio en arrière-plan incertain ; pas d'accès hors compte Claude.

### B. Application indépendante (recommandé à moyen terme)

Proposition d'architecture, simple et peu coûteuse :

| Besoin | Proposition |
|---|---|
| Hébergement de l'app (PWA installable) | Cloudflare Pages |
| API, tâches quotidiennes | Cloudflare Workers + Cron Triggers |
| Base de données | Cloudflare D1 (SQLite) |
| Images et fichiers audio | Cloudflare R2 |
| Accès réservé à vous | Cloudflare Access (connexion par email) |
| Rédaction | API Anthropic, clé stockée en secret côté serveur |
| Newsletters | Voir ci-dessous |

**Gmail hors de claude.ai, deux options :**

1. **Transfert automatique (recommandé)** : un filtre Gmail transfère les emails du libellé Moka/Newsletters vers une adresse dédiée (ex. `moka@votre-domaine`) reçue par Cloudflare Email Routing. Moka ne voit jamais le reste de votre boîte et n'a besoin d'aucun jeton Google. Il faut un nom de domaine.
2. **OAuth Google** avec la seule permission `gmail.readonly`. C'est une permission « restreinte » : en mode test, les jetons expirent au bout de 7 jours ; en production sans vérification Google, un avertissement s'affiche. Plus intrusif et plus fragile que l'option 1.

**Migration des données** : import de `data/articles.json` + `data/formats.json`, de vos favoris exportés, et des assets éventuels. Les deux versions peuvent tourner en parallèle le temps de vérifier.

### C. Hybride (déconseillé)

Garder l'interface sur Artifacts et un serveur à côté exposé comme connecteur MCP personnalisé. Techniquement possible, mais complexe, et cumule les contraintes des deux mondes.

## Ce qui ne survivra pas à une sortie de claude.ai

- La connexion via votre compte Claude (remplacée par Cloudflare Access ou équivalent).
- Le connecteur Gmail de claude.ai (remplacé par le transfert ou OAuth).
- La rédaction « dans la page » par Claude (remplacée par l'API, payante à l'usage).
- L'hébergement gratuit et privé par défaut.

## Points d'accord nécessaires

1. Création du dépôt GitHub `moka` (par vous) puis push (par Claude).
2. Choix de la trajectoire A ou B.
3. Pour A : autorisation des domaines d'images ; création de la tâche planifiée.
4. Pour B : nom de domaine, compte Cloudflare, clé API Anthropic, choix transfert ou OAuth.
