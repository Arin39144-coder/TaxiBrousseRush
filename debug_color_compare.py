"""
debug_color_compare.py — 3 cubes rouges, construits différemment, côte à côte.
Lance avec : python debug_color_compare.py

Les 3 cubes DEVRAIENT être rouges. Dis-moi lesquels le sont vraiment et
lesquels apparaissent blancs :
  - cube de GAUCHE  : color.red (couleur prédéfinie Ursina)
  - cube du MILIEU  : color.rgb32(255, 0, 0)   <- comme dans notre projet
  - cube de DROITE  : Color(1, 0, 0, 1) construit à la main, sans passer par rgb()
"""
from ursina import Ursina, Entity, color, camera, Color, EditorCamera

app = Ursina()

Entity(model='cube', color=color.red, x=-3)
Entity(model='cube', color=color.rgb32(255, 0, 0), x=0)
Entity(model='cube', color=Color(1, 0, 0, 1), x=3)

EditorCamera()
app.run()
