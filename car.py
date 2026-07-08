"""
car.py — Contrôleur du taxi-brousse.

Physique simplifiée : accélération, freinage, friction, direction.
Pas de modèle 3D externe : une simple boîte colorée (à remplacer plus
tard par un .obj si le temps le permet — voir README section "Assets").
"""

from ursina import Entity, color, held_keys, time, clamp, Vec3


class Car(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model="cube",
            color=color.azure,
            scale=(1.6, 1, 3),
            collider="box",
            position=(0, 0.5, 0),
        )

        # Cosmétique simple : "toit" pour distinguer l'avant du taxi-brousse
        self.roof = Entity(
            parent=self,
            model="cube",
            color=color.white,
            scale=(0.8, 0.5, 1.4),
            position=(0, 0.7, -0.2),
        )

        # --- Paramètres de conduite ---
        self.speed = 0
        self.topspeed = 22
        self.reverse_topspeed = -8
        self.acceleration = 14      # unités / s^2
        self.braking_strength = 30
        self.friction = 10          # décélération naturelle
        self.turning_speed = 90     # degrés / s à pleine vitesse
        self.min_speed_to_turn = 0.5

        # État
        self.is_slowed = False      # affecté par un nid-de-poule
        self.slow_timer = 0
        self.crashed_recently = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        dt = time.dt

        # --- Accélération / freinage ---
        accel_input = 0
        if held_keys["w"] or held_keys["up arrow"]:
            accel_input += 1
        if held_keys["s"] or held_keys["down arrow"]:
            accel_input -= 1

        if accel_input > 0:
            self.speed += self.acceleration * dt
        elif accel_input < 0:
            self.speed -= self.braking_strength * dt
        else:
            # Friction naturelle ramène la vitesse à 0
            if self.speed > 0:
                self.speed = max(0, self.speed - self.friction * dt)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.friction * dt)

        # Ralentissement temporaire (nid-de-poule)
        effective_topspeed = self.topspeed
        if self.slow_timer > 0:
            self.slow_timer -= dt
            effective_topspeed *= 0.4

        self.speed = clamp(self.speed, self.reverse_topspeed, effective_topspeed)

        # --- Direction ---
        if abs(self.speed) > self.min_speed_to_turn:
            turn_input = 0
            if held_keys["a"] or held_keys["left arrow"]:
                turn_input -= 1
            if held_keys["d"] or held_keys["right arrow"]:
                turn_input += 1

            # Inverse la direction en marche arrière (comme une vraie voiture)
            direction = 1 if self.speed > 0 else -1
            speed_ratio = min(abs(self.speed) / self.topspeed, 1)
            self.rotation_y += (
                turn_input * self.turning_speed * direction * speed_ratio * dt
            )

        # --- Déplacement ---
        self.position += self.forward * self.speed * dt

    def apply_pothole_slow(self, duration=1.2):
        """Appelé par obstacles.py quand le taxi touche un nid-de-poule."""
        self.slow_timer = duration

    def crash_bounce(self):
        """Petit recul + perte de vitesse lors d'une collision (animal, etc.)."""
        self.speed *= -0.3
        self.crashed_recently = True
