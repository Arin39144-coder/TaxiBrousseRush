# models/road.py

import random


class RoadSegment:

    def __init__(self, index=0, difficulty=1):
        self.index = index
        self.length = 1000
        self.weather = None
        self.obstacles = []
        self.difficulty = difficulty

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)


class Route:

    def __init__(self):
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)

    def get_current_segment(self, position):
        # position = distance totale parcourue
        cumulative = 0
        for segment in self.segments:
            cumulative += segment.length
            if position < cumulative:
                return segment
        return self.segments[-1] if self.segments else None

    def get_total_length(self):
        return sum(segment.length for segment in self.segments)


class RouteGenerator:

    def generate_segment(self, index=0, difficulty=1):
        segment = RoadSegment(index=index, difficulty=difficulty)
        segment.weather = random.choice(["sunny", "rainy", "foggy"])
        return segment

    def generate_route(self, nb_segments, base_difficulty=1):
        route = Route()
        for i in range(nb_segments):
            # difficulté qui augmente progressivement
            difficulty = base_difficulty + (i // 3)
            segment = self.generate_segment(index=i, difficulty=difficulty)
            route.add_segment(segment)
        return route


class WeatherPattern:

    FRICTION_MODIFIERS = {
        "sunny": 1.0,
        "rainy": 0.7,
        "foggy": 0.9,
    }

    def __init__(self):
        self.current_weather = "sunny"
        self.timer = 0
        self.change_interval = 30  # secondes avant possible changement

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.change_interval:
            self.timer = 0
            self.current_weather = random.choice(list(self.FRICTION_MODIFIERS.keys()))

    def get_friction_modifier(self):
        return self.FRICTION_MODIFIERS.get(self.current_weather, 1.0)