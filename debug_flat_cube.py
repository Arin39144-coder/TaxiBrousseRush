"""
debug_flat_cube.py — Un seul cube très étiré (comme dans road.py),
SANS Sky, pour voir si c'est cette forme d'entité qui pose problème.
Lance avec : python debug_flat_cube.py
Regarde : le rectangle marron s'affiche-t-il, coloré et visible ?
"""
from ursina import Ursina, Entity, color, camera

app = Ursina()

flat = Entity(
    model="cube",
    color=color.rgb32(150, 70, 40),
    scale=(10, 0.2, 400),
    position=(0, 0, 180),
    collider=None,
)

camera.position = (0, 15, -20)
camera.rotation_x = 25
camera.fov = 90

app.run()
