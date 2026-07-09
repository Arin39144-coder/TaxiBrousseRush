"""
main_debug1.py — Bissection : SKY + ROAD uniquement, rien d'autre.
Lance avec : python main_debug1.py

Si ça s'affiche correctement : le bug vient de car/obstacles/weather/UI.
Si ça ne s'affiche PAS correctement : le bug vient de road.py lui-même.
"""
from ursina import Ursina, Entity, Sky, color, camera, window

from road import build_road, ROAD_LENGTH, ROAD_WIDTH

app = Ursina()
window.title = "DEBUG 1 - sky + road"

sky = Sky(color=color.rgb32(140, 190, 230))
road = build_road()

camera.position = (0, 15, -20)
camera.rotation_x = 25
camera.fov = 90

app.run()
