"""
debug_sky_only.py — Sky() tout seul, aucune autre entité, caméra par défaut.
Lance avec : python debug_sky_only.py
Regarde bien le FOND : bleu clair uni, ou blanc ?
"""
from ursina import Ursina, Sky, color

app = Ursina()
sky = Sky(color=color.rgb32(140, 190, 230))
app.run()
