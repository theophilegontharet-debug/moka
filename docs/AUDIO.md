# Moka Audio : conception technique

Rien n'est développé pour l'instant : aucun lecteur n'existe dans l'app.

## Deux usages

1. **Écouter un article** dans le format choisi (Express, Comprendre, Approfondir).
2. **Briefing du matin** : 5 à 8 minutes réunissant les actualités prioritaires, comme un mini-podcast.

## Principe : écrire pour l'oreille, puis synthétiser

Lire à voix haute le texte écrit sonne mal. Chaque version audio part d'un **script oral** rédigé par Claude :

- phrases courtes, chiffres arrondis et dits en toutes lettres (« un peu plus de cent quatre-vingts millions de dollars ») ;
- sigles expliqués, pas de parenthèses ni de listes ;
- transitions (« Restons en Afrique, mais changeons de secteur… ») ;
- sources citées oralement (« selon The Big Deal ») ;
- les incertitudes dites clairement (« c'est ce que rapporte le Wall Street Journal, rien n'est confirmé »).

Le script est enregistré avec l'article, comme les formats écrits, pour ne pas le régénérer.

## Synthèse vocale : options réalistes

| Option | Qualité | Coût | Contraintes |
|---|---|---|---|
| Voix du navigateur (Web Speech API) | Variable selon l'appareil ; correcte sur iPhone récent | Gratuit | Pas de fichier, pas de lecture écran verrouillé fiable ; bon pour un prototype |
| Service de synthèse (ElevenLabs, OpenAI, Google Cloud, Azure…) | Naturelle, voix française de qualité | Payant à l'usage | Nécessite une clé API côté serveur ; fichiers audio à stocker |

Recommandation : prototype avec la voix du navigateur pour valider l'usage, puis service de synthèse pour le briefing quotidien.
Note Artifacts : les assets acceptent les conteneurs MP4 et WebM, pas le MP3 ; le format exact pour l'audio reste à tester.

## Lecteur

- Élément `<audio>` standard : lecture, pause, avance de 15 s, retour de 15 s, vitesse 0,8× à 2×.
- **Media Session API** : commandes sur l'écran verrouillé et le casque.
- **Reprise** : position enregistrée toutes les 15 s dans `data/users/<id>/audio` (par article et format), lecture reprise au même endroit sur tous les appareils.
- Briefing : liste de segments (un par article) avec chapitres ; passer au suivant, revenir à l'article écrit.
- Mini-lecteur fixe au-dessus de la barre d'onglets, qui suit la navigation.

## Données

```
audio/<articleId>-<format>  { script, voice, duration_s, asset, source_hash, generated_at }
briefings/<date>            { segments: [{articleId, start_s}], asset, duration_s }
data/users/<id>/audio       { "<articleId>-<format>": position_s, … }
```

`source_hash` permet de régénérer l'audio seulement si le texte a changé.

## Limite à vérifier avant de développer

La lecture en arrière-plan et sur écran verrouillé depuis une page affichée dans l'app Claude n'est pas garantie. Pour un vrai usage podcast, une app indépendante installable (trajectoire B) est plus sûre.
