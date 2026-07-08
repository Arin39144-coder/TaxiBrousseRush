# models/level.py

import random
from enum import Enum


class LevelState(Enum):
    LOCKED = 0
    AVAILABLE = 1
    PLAYING = 2
    COMPLETED = 3
    FAILED = 4


class LevelDifficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXTREME = 4


DIFFICULTY_SETTINGS = {
    LevelDifficulty.EASY: {"traffic": 0.2, "damage": 0.5},
    LevelDifficulty.NORMAL: {"traffic": 0.5, "damage": 1.0},
    LevelDifficulty.HARD: {"traffic": 0.8, "damage": 1.5},
    LevelDifficulty.EXTREME: {"traffic": 1.0, "damage": 2.0},
}


class LevelTheme(Enum):
    CITY = "city"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    DESERT = "desert"
    RAIN_FOREST = "rain_forest"
    MADAGASCAR = "madagascar"


class LevelConfig:

    def __init__(self, name, difficulty, theme):
        self.name = name
        self.difficulty = difficulty
        self.theme = theme

        self.route = None
        self.obstacles = []
        self.passengers = []
        self.weather = None

    def get_settings(self):
        return DIFFICULTY_SETTINGS.get(self.difficulty, DIFFICULTY_SETTINGS[LevelDifficulty.NORMAL])


class LevelResult:

    def __init__(self, score, duration, passengers):
        self.score = score
        self.duration = duration
        self.passengers_saved = passengers
        self.damage = 0
        self.stars = 0

    def calculate_stars(self):
        if self.score >= 1000:
            self.stars = 3
        elif self.score >= 500:
            self.stars = 2
        else:
            self.stars = 1
        return self.stars


class Level:

    def __init__(self, config):
        self.config = config

        self.route = None
        self.obstacles = []
        self.passengers = []

        self.weather = None

        self.score = 0
        self.time = 0

        self.state = LevelState.LOCKED

    def load(self):
        self.route = self.config.route
        self.obstacles = self.config.obstacles
        self.passengers = self.config.passengers
        self.weather = self.config.weather
        self.state = LevelState.AVAILABLE

    def start(self):
        if self.state == LevelState.AVAILABLE:
            self.state = LevelState.PLAYING

    def update(self, dt):
        if self.state != LevelState.PLAYING:
            return
        self.time += dt

    def finish(self):
        self.state = LevelState.COMPLETED

    def fail(self):
        self.state = LevelState.FAILED

    def get_result(self):
        result = LevelResult(
            score=self.score,
            duration=self.time,
            passengers=len(self.passengers),
        )
        result.calculate_stars()
        return result


class LevelGenerator:

    def generate_random(self):
        config = LevelConfig(
            "Random",
            random.choice(list(LevelDifficulty)),
            random.choice(list(LevelTheme)),
        )
        return Level(config)

    def generate_campaign(self):
        levels = []
        cities = [
            "Antananarivo",
            "Antsirabe",
            "Fianarantsoa",
            "Toliara",
            "Mahajanga",
            "Toamasina",
        ]

        for i, city in enumerate(cities):
            # difficulté progressive selon l'avancement dans la campagne
            difficulty = list(LevelDifficulty)[min(i // 2, len(LevelDifficulty) - 1)]
            config = LevelConfig(city, difficulty, LevelTheme.MADAGASCAR)
            levels.append(Level(config))

        return levels

    def generate_madagascar_tour(self):
        routes = ["RN7", "RN2", "RN4", "RN5"]
        levels = []
        for route_name in routes:
            config = LevelConfig(route_name, LevelDifficulty.NORMAL, LevelTheme.MADAGASCAR)
            levels.append(Level(config))
        return levels