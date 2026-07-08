# models/vehicle.py

from models.passenger import PassengerManager


class TaxiBrousse:

    def __init__(self):
        # Position
        self.x = 0
        self.y = 0

        # Conduite
        self.speed = 0
        self.max_speed = 120
        self.acceleration = 10
        self.deceleration = 15       # freinage
        self.friction = 5            # décélération naturelle
        self.direction = 0
        self.max_turn_angle = 45

        # Carburant
        self.fuel = 100
        self.max_fuel = 100
        self.fuel_consumption = 2    # unités / seconde en roulant

        # Dégâts
        self.damage = 0
        self.max_damage = 100

        # Passagers
        self.passenger_manager = PassengerManager()
        self.passengers = []
        self.max_passengers = 4

        # Effets temporaires
        self.slow_factor = 1.0
        self.slow_timer = 0
    
    def _initialize_passengers(self, passengers):
        for p in passengers[:self.max_passengers]:
            self.passenger_manager.add_passenger(p)

    def get_passenger_count(self):
        return len(self.passenger_manager.passengers)

    def update_passenger_stress(self, amount):
        for p in self.passenger_manager.passengers:
            p.increase_stress(amount)
        self.passenger_manager.update()  # applique aussi les interactions

    def lose_passenger(self):
        if self.passenger_manager.passengers:
            self.passenger_manager.remove_passenger(self.passenger_manager.passengers[0])

    # ----- Conduite -----

    def accelerate(self, dt):
        if self.fuel <= 0 or self.is_stalled():
            return
        self.speed += self.acceleration * dt
        self.speed = min(self.speed, self.max_speed)

    def brake(self, dt):
        self.speed -= self.deceleration * dt
        self.speed = max(self.speed, 0)

    def turn(self, angle):
        self.direction += angle
        self.direction = max(-self.max_turn_angle, min(self.max_turn_angle, self.direction))

    def update_physics(self, dt):
        # Friction naturelle si on n'accélère pas
        if self.speed > 0:
            self.speed -= self.friction * dt
            self.speed = max(self.speed, 0)

        # Application du ralentissement temporaire
        effective_speed = self.speed * self.slow_factor

        # Mise à jour position selon direction (simplifié)
        self.x += effective_speed * dt
        self.y += self.direction * 0.1 * dt

        # Décompte de l'effet de ralentissement
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slow_factor = 1.0

        # Consommation de carburant
        if self.speed > 0:
            self.fuel -= self.fuel_consumption * dt
            self.fuel = max(self.fuel, 0)

    # ----- Passagers -----

    def _initialize_passengers(self, passengers):
        self.passengers = passengers[:self.max_passengers]

    def get_passenger_count(self):
        return len(self.passengers)

    def update_passenger_stress(self, amount):
        for passenger in self.passengers:
            passenger.stress += amount

    def lose_passenger(self):
        if self.passengers:
            self.passengers.pop(0)

    # ----- Dégâts -----

    def take_damage(self, amount):
        self.damage += amount
        self.damage = min(self.damage, self.max_damage)

    def repair(self, amount):
        self.damage -= amount
        self.damage = max(self.damage, 0)

    def get_damage_level(self):
        return self.damage

    # ----- État -----

    def is_stalled(self):
        return self.damage >= self.max_damage

    def is_moving(self):
        return self.speed > 0

    def get_speed_ratio(self):
        return self.speed / self.max_speed

    # ----- Effets -----

    def apply_slow(self, factor, duration):
        self.slow_factor = factor
        self.slow_timer = duration

    def refuel(self, amount):
        self.fuel += amount
        self.fuel = min(self.fuel, self.max_fuel)

    # ----- Sauvegarde -----

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "direction": self.direction,
            "fuel": self.fuel,
            "damage": self.damage,
            "passenger_count": self.get_passenger_count(),
        }

    @classmethod
    def from_dict(cls, data):
        vehicle = cls()
        vehicle.x = data.get("x", 0)
        vehicle.y = data.get("y", 0)
        vehicle.speed = data.get("speed", 0)
        vehicle.direction = data.get("direction", 0)
        vehicle.fuel = data.get("fuel", 100)
        vehicle.damage = data.get("damage", 0)
        return vehicle