# Alimentation quotidienne de Moka

## Ajouter une sélection (manuel, sans coût récurrent)
1. Créer `data/auto-AAAA-MM-JJ.json` (liste d'articles, même schéma que `auto-2026-11-11.json`, `collected_at` en ISO UTC).
2. `python3 tools/build_site.py` : charge tous les `data/auto-*.json`, refuse les identifiants ou titres en double, calcule le jour d'ajout (`added`, fuseau Africa/Abidjan).
3. Commit + push sur `main` : Vercel redéploie. Les fichiers des jours précédents ne sont jamais réécrits.

## Règles
- Vue par semaine (lundi → dimanche), regroupée par jour d'ajout ; la date de publication de la source reste visible dans l'article.
- Consulter une ancienne semaine ne lance aucun traitement. Une semaine vide affiche un état vide.
- Les 32 articles initiaux ont tous `collected_at = 2026-11-07` : ils sont classés au 7 novembre (semaine du 2 au 8).
- Patrick est en pause (`audio/pause.json`) ; Google Chirp est retiré. Pas de bouton d'écoute sans MP3.

## Reste à activer pour l'alimentation automatique
Rien n'est planifié. Il faudrait une tâche planifiée Claude qui rédige le fichier du jour et le pousse sur `main` : elle consommerait le quota Claude. Une route par API (script + clé) serait facturée séparément.
