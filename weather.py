"""
weather.py — Système météo pour TaxiBrousse Rush.

Deux états : CLEAR (temps clair) et RAIN (pluie).
La pluie :
  - réduit l'adhérence du taxi-brousse (friction augmentée,
    virages plus lents, vitesse de pointe légèrement réduite)
  - assombrit la scène (brouillard + ciel plus gris)
  - fait apparaître des particules de pluie qui tombent autour du véhicule

Deux modes de déclenchement, au choix :
  - PAR ZONE (recommandé, plus simple à démontrer à l'oral) : chaque
    tronçon de route a un état météo fixe.
  - ALÉATOIRE dans le temps : change d'état toutes les 15-25s.

--- Utilisation dans main.py ---

    from weather import WeatherSystem

    weather = WeatherSystem(car)

    def update():
        ...
        weather.update(car.z)          # pilotage par zone (recommandé)
        # OU, à la place :
        # weather.update_random()      # pilotage aléatoire
"""

import random
from ursina import Entity, color, scene, time


CLEAR = "clear"
RAIN = "rain"

# Zones du parcours (axe Z) -> état météo associé.
# Si vous refondez road.py en 3 segments (ville/forêt/piste, voir le plan
# section 4/5), gardez ces bornes cohérentes avec celles de road.py.
ZONES = [
    {"name": "ville", "z_start": 0,   "z_end": 130, "weather": CLEAR},
    {"name": "foret", "z_start": 130, "z_end": 270, "weather": RAIN},
    {"name": "piste", "z_start": 270, "z_end": 400, "weather": CLEAR},
]


def get_current_zone(z):
    for zone in ZONES:
        if zone["z_start"] <= z < zone["z_end"]:
            return zone
    return ZONES[-1]


class RainDrop(Entity):
    """Une particule de pluie : un fin cube qui tombe puis se replace en haut."""

    def __init__(self, **kwargs):
        super().__init__(
            model="cube",
            color=color.rgba(180, 200, 255, 140),
            scale=(0.03, 0.6, 0.03),
            collider=None,
        )
        self.fall_speed = random.uniform(14, 20)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        # Appelé automatiquement chaque frame par Ursina tant que
        # l'entité est enabled=True.
        self.y -= self.fall_speed * time.dt
        if self.y < -1:
            self.y = random.uniform(6, 10)
            self.x = random.uniform(-6, 6)


class WeatherSystem:
    def __init__(self, car, num_raindrops=60):
        self.car = car
        self.state = CLEAR
        self.raindrops = []
        self.num_raindrops = num_raindrops

        # Valeurs "normales" de conduite, sauvegardées pour pouvoir
        # les restaurer quand la pluie s'arrête.
        self.base_friction = car.friction
        self.base_turning_speed = car.turning_speed
        self.base_topspeed = car.topspeed

        # Minuteur pour le mode aléatoire (optionnel)
        self.random_timer = random.uniform(15, 20)

    # ---------- Déclenchement par zone (recommandé) ----------
    def update(self, car_z):
        zone = get_current_zone(car_z)
        if zone["weather"] != self.state:
            self._set_state(zone["weather"])
        if self.state == RAIN:
            self._reposition_raindrops()

    # ---------- Déclenchement aléatoire (alternative) ----------
    def update_random(self):
        self.random_timer -= time.dt
        if self.random_timer <= 0:
            self.random_timer = random.uniform(15, 25)
            self._set_state(RAIN if self.state == CLEAR else CLEAR)
        if self.state == RAIN:
            self._reposition_raindrops()

    # ---------- Logique interne ----------
    def _set_state(self, new_state):
        self.state = new_state
        if new_state == RAIN:
            self._start_rain()
        else:
            self._stop_rain()

    def _start_rain(self):
        # Effet sur la conduite : route glissante
        self.car.friction = self.base_friction * 0.6
        self.car.turning_speed = self.base_turning_speed * 0.7
        self.car.topspeed = self.base_topspeed * 0.85

        # Ambiance visuelle
        scene.fog_density = 0.02
        scene.fog_color = color.rgb32(150, 150, 160)

        if not self.raindrops:
            for _ in range(self.num_raindrops):
                self.raindrops.append(
                    RainDrop(
                        position=(
                            random.uniform(-6, 6),
                            random.uniform(0, 10),
                            self.car.z + random.uniform(-6, 40),
                        )
                    )
                )
        else:
            for drop in self.raindrops:
                drop.enabled = True

    def _stop_rain(self):
        # Restaure la conduite normale
        self.car.friction = self.base_friction
        self.car.turning_speed = self.base_turning_speed
        self.car.topspeed = self.base_topspeed

        scene.fog_density = 0

        for drop in self.raindrops:
            drop.enabled = False

    def _reposition_raindrops(self):
        # Garde le "nuage" de pluie centré autour du véhicule le long
        # de l'axe Z, sans le recréer (le RainDrop.update() gère déjà
        # la chute en Y tout seul, appelé automatiquement par Ursina).
        for drop in self.raindrops:
            if drop.z < self.car.z - 15:
                drop.z = self.car.z + random.uniform(15, 45)
