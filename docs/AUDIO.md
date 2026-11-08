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

## Version 1 (8 novembre 2026) : synthèse vocale du navigateur

Module `MokaAudio` dans `app/index.html`. Aucun serveur, aucun frais, aucun quota Claude.

- Bouton « Écouter » sous les formats de chaque article : lit le format choisi
  (Express, Comprendre, Approfondir ; à défaut Comprendre).
- Le texte est assemblé depuis les données (titre, chapeau, corps, analyse, « pourquoi ça compte »,
  inconnues), normalisé pour l'oral (« M$ » → « millions de dollars », « T3 » → « troisième trimestre »…)
  et lu phrase par phrase.
- Mini-lecteur au-dessus de la barre d'onglets : lecture/pause (reprise à la phrase en cours),
  arrêt, vitesse 0,85× à 1,5×, choix parmi les voix françaises de l'appareil.
- Préférences : `localStorage` `moka.audio.voice` et `moka.audio.rate` (les favoris ne sont pas touchés).

Limites connues : la voix dépend de l'appareil (sur iPhone, Réglages → Accessibilité → Contenu énoncé →
Voix → Français permet de télécharger des voix « améliorées ») ; sur iPhone, la synthèse s'arrête
généralement quand l'écran se verrouille ou quand on change d'application, et il n'y a pas de
contrôles sur l'écran verrouillé.

## Étape suivante : vrais fichiers audio

Pour une écoute écran verrouillé, avec les contrôles du centre de contrôle : générer un MP3 par
article et par format (API de synthèse vocale : OpenAI TTS, ElevenLabs, Google Cloud TTS, Azure),
le stocker avec le site ou sur Vercel Blob, et le lire avec un élément `<audio>` + Media Session API.
C'est aussi la base du briefing quotidien narré.
