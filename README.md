# TaxiBrousse Rush — Prototype 2 jours

Jeu de course 3D minimaliste : conduisez un taxi-brousse sur une piste
malgache, évitez les nids-de-poule et les zébus, en 60 secondes.

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Contrôles

| Touche            | Action            |
|-------------------|-------------------|
| W / Flèche haut   | Accélérer         |
| S / Flèche bas    | Freiner / reculer |
| A / D             | Direction         |
| R                 | Recommencer (après game over) |

## Structure du projet

- `car.py` — physique du véhicule (accélération, friction, direction)
- `road.py` — génération de la route et des bas-côtés
- `obstacles.py` — `Pothole` (nid-de-poule, ralentit) et `Zebu` (animal, collision)
- `main.py` — assemble tout : score, timer, UI, game over/restart

## Répartition suggérée (4 personnes, 2 jours)

| Personne | Jour 1 | Jour 2 |
|---|---|---|
| A | Tester/ajuster la conduite dans `car.py` (vitesse, dérive) | Polish contrôles + game feel |
| B | Décor : remplacer les cubes de `road.py` par textures / huttes / virages | Skybox, ambiance visuelle Madagascar |
| C | `obstacles.py` : ajuster fréquence, ajouter un 3e type si le temps le permet (embouteillage = mur temporaire) | Équilibrage difficulté |
| D | UI (`main.py`) : timer, score, écran fin — déjà posé, à styliser | Tests bout en bout, prépa démo/vidéo |

## Idées d'amélioration si le temps le permet

- Remplacer les cubes par de vrais modèles low-poly (voir le repo Rally
  pour des assets de véhicule/piste réutilisables sous licence libre :
  https://github.com/mandaw2014/Rally)
- Ajouter des virages à la route (segments avec offset en x)
- Ajouter un troisième obstacle : embouteillage (mur qui force un
  contournement) — modèle simple : plusieurs `Entity` cubes statiques
  groupés sur une portion de route
- Musique de fond / bruitage collision (`Audio()` d'Ursina)

## Notes techniques

- Tout est construit avec des primitives Ursina (`model="cube"`), donc
  **aucun fichier lourd à télécharger** — clone/installation rapide pour
  toute l'équipe.
- Le score = distance parcourue - (nombre de zébus touchés × 10). Les
  nids-de-poule ne retirent pas de points mais ralentissent, donc il y a
  un vrai compromis vitesse/sécurité, comme demandé dans le sujet.
