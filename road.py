"""
road.py — Génère une route rurale simple (piste en terre).

Pour 2 jours : UNE route droite avec une texture de couleur "terre rouge"
et des bas-côtés verts. Pas de courbes, pas de terrain procédural.
Si le temps le permet en fin de journée 2, on peut ajouter des virages
(voir TODO en bas du fichier).
"""

from ursina import Entity, color


ROAD_LENGTH = 400
ROAD_WIDTH = 10


def build_road():
    """Crée le sol : route + bas-côtés. Retourne l'entité route (pour référence)."""

    # Route principale (terre rouge, typique des pistes malgaches)
    road = Entity(
        model="cube",
        color=color.rgb32(150, 70, 40),
        scale=(ROAD_WIDTH, 0.2, ROAD_LENGTH),
        position=(0, 0, ROAD_LENGTH / 2 - 20),
        collider=None,
    )

    # Bas-côtés (végétation stylisée en vert, juste pour le décor)
    for side in (-1, 1):
        Entity(
            model="cube",
            color=color.rgb32(60, 110, 50),
            scale=(30, 0.15, ROAD_LENGTH),
            position=(side * (ROAD_WIDTH / 2 + 15), -0.05, ROAD_LENGTH / 2 - 20),
            collider=None,
        )

    return road

# TODO (si le temps le permet) :
# - remplacer la route droite par une succession de segments avec un léger
#   décalage en x pour simuler des virages
# - ajouter des entités "case"/"hutte" (cubes marron+toit triangle) le long
#   de la route pour renforcer l'ambiance Madagascar
