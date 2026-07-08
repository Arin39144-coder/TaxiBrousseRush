"""
obstacles.py — Les deux types d'obstacles du MVC (2 jours) :

1. Pothole   : nid-de-poule statique posé sur la route -> ralentit le taxi.
2. Zebu      : animal qui traverse la route de façon imprévisible
               -> collision = pénalité de sécurité + petit recul.

Chaque classe expose `check_collision(car)` appelé depuis main.py à
chaque frame. Pas de moteur physique complexe : simple distance/AABB.
"""

import random
from ursina import Entity, color, time, Vec3, distance


class Pothole(Entity):
    def __init__(self, position=(0, 0.05, 0), **kwargs):
        super().__init__(
            model="cube",
            color=color.rgb(40, 30, 20),
            scale=(1.8, 0.1, 1.8),
            position=position,
            collider=None,  # collision gérée manuellement (plus simple à ajuster)
        )
        self.triggered = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def check_collision(self, car):
        if self.triggered:
            return None
        if distance(self.position, car.position) < 1.3:
            self.triggered = True
            car.apply_pothole_slow()
            self.color = color.rgb(70, 50, 35)  # feedback visuel : "déjà touché"
            return "pothole"
        return None


class Zebu(Entity):
    """Animal qui traverse la route perpendiculairement."""

    def __init__(self, position=(0, 0.6, 0), road_width=10, **kwargs):
        super().__init__(
            model="cube",
            color=color.rgb(120, 90, 60),
            scale=(1.2, 1.2, 2.2),
            position=position,
            collider=None,
        )
        self.road_width = road_width
        self.speed = random.uniform(1.5, 3)
        # Traverse de gauche à droite ou l'inverse au hasard
        self.direction = random.choice([-1, 1])
        self.triggered = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.x += self.direction * self.speed * time.dt
        # Repart de l'autre côté une fois hors route (boucle simple)
        if abs(self.x) > self.road_width / 2 + 2:
            self.direction *= -1
            self.triggered = False  # peut re-déclencher une collision au retour

    def check_collision(self, car):
        if self.triggered:
            return None
        if distance(self.position, car.position) < 1.6:
            self.triggered = True
            car.crash_bounce()
            return "zebu"
        return None
