# models/obstacle.py

from abc import ABC, abstractmethod


class Obstacle(ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    @abstractmethod
    def apply_effect(self, vehicle):
        pass


class Pothole(Obstacle):

    def apply_effect(self, vehicle):
        vehicle.take_damage(5)
        vehicle.apply_slow(0.8, 2)


class BrokenBridge(Obstacle):

    def apply_effect(self, vehicle):
        vehicle.take_damage(15)


class TrafficJam(Obstacle):

    def apply_effect(self, vehicle):
        vehicle.apply_slow(0.3, 5)


class Animal(Obstacle):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = 1
        self.move_speed = 20

    def move(self, dt):
        self.y += self.direction * self.move_speed * dt
        # rebondit entre deux limites simples de la route
        if self.y > 50 or self.y < -50:
            self.direction *= -1

    def apply_effect(self, vehicle):
        vehicle.take_damage(10)


class ObstacleFactory:

    _TYPES = {
        "pothole": Pothole,
        "bridge": BrokenBridge,
        "traffic": TrafficJam,
        "animal": Animal,
    }

    @staticmethod
    def create(obstacle_type, x, y):
        obstacle_class = ObstacleFactory._TYPES.get(obstacle_type)
        if obstacle_class is None:
            raise ValueError(f"Type d'obstacle inconnu : {obstacle_type}")
        return obstacle_class(x, y)


class ObstacleManager:

    def __init__(self):
        self.obstacles = []

    def update(self, dt):
        for obstacle in self.obstacles:
            if isinstance(obstacle, Animal):
                obstacle.move(dt)

    def add(self, obstacle):
        self.obstacles.append(obstacle)

    def remove(self, obstacle):
        if obstacle in self.obstacles:
            self.obstacles.remove(obstacle)

    def get_active(self):
        return [o for o in self.obstacles if o.active]

    def clear(self):
        self.obstacles = []