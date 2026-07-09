"""
debug_cross_test.py — 4 cubes pour isoler la vraie cause :
  1. rouge (petit)                          <- référence connue : marche
  2. couleur marron du projet (petit)       <- teste la VALEUR de couleur
  3. rouge (échelle énorme et plate)        <- teste l'ÉCHELLE seule
  4. couleur marron du projet (échelle énorme) <- reproduit le bug du road

Lance avec : python debug_cross_test.py
Utilise clic droit + souris pour bouger la caméra (EditorCamera) et
regarde bien chaque cube. Dis-moi lesquels sont colorés et lesquels
sont blancs.
"""
from ursina import Ursina, Entity, color, EditorCamera

app = Ursina()

# 1. Référence : petit cube rouge
Entity(model='cube', color=color.red, scale=2, x=-15)

# 2. Petit cube avec la couleur exacte du road.py
Entity(model='cube', color=color.rgb32(150, 70, 40), scale=2, x=-5)

# 3. Cube énorme et plat, mais ROUGE (teste l'échelle seule)
Entity(model='cube', color=color.red, scale=(10, 0.2, 40), x=5, z=20)

# 4. Cube énorme et plat, couleur du road.py (reproduit le bug d'origine)
Entity(model='cube', color=color.rgb32(150, 70, 40), scale=(10, 0.2, 40), x=25, z=20)

EditorCamera(rotation_x=30, y=10, z=-20)
app.run()
