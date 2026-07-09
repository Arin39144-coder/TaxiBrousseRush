"""
minimal_test.py — teste si Ursina affiche correctement en dehors de tout
notre code (sky/weather/car/lumières). Lance avec : python minimal_test.py

Utilise WASD/souris pour bouger la caméra (EditorCamera).
Si ce test affiche un cube ROUGE net sur fond gris/bleu normal : le
problème vient de quelque chose dans notre scène (lumières, sky sphere,
weather, etc.), pas du driver.
Si ce test affiche déjà un écran blanc/vide : c'est un souci
d'environnement (driver Intel, config Panda3D), indépendant de notre code.
"""
from ursina import Ursina, Entity, color, EditorCamera, Sky

app = Ursina()
Entity(model='cube', color=color.red, scale=2)
Sky(color=color.rgb32(140, 190, 230))
EditorCamera()
app.run()
