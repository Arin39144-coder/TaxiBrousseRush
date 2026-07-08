# models/passenger.py

import random


class PassengerPreference:

    def __init__(self, likes_music=True, temperature=22, likes_speed=False):
        self.likes_music = likes_music
        self.temperature = temperature
        self.likes_speed = likes_speed


class PassengerItem:

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


class Passenger:

    MAX_STRESS = 100

    def __init__(self, name, destination=None):
        self.name = name
        self.stress = 0
        self.money = 0
        self.destination = destination
        self.preferences = PassengerPreference()
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def increase_stress(self, amount):
        self.stress = min(self.stress + amount, self.MAX_STRESS)

    def calm_down(self, amount):
        self.stress = max(self.stress - amount, 0)

    def is_panicked(self):
        return self.stress >= self.MAX_STRESS

    def pay(self, base_fare):
        # Un passager stressé paie moins (pourboire réduit)
        stress_penalty = self.stress / self.MAX_STRESS
        self.money = base_fare * (1 - 0.5 * stress_penalty)
        return self.money


class PassengerInteraction:

    def __init__(self, passenger1, passenger2):
        self.passenger1 = passenger1
        self.passenger2 = passenger2

    def update(self):
        # Conflit simple : préférences musique opposées = stress pour les deux
        if self.passenger1.preferences.likes_music != self.passenger2.preferences.likes_music:
            self.passenger1.increase_stress(1)
            self.passenger2.increase_stress(1)


class PassengerManager:

    def __init__(self):
        self.passengers = []
        self.interactions = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        # Crée des interactions avec les passagers déjà présents
        for other in self.passengers[:-1]:
            self.interactions.append(PassengerInteraction(passenger, other))

    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
        self.interactions = [
            i for i in self.interactions
            if i.passenger1 is not passenger and i.passenger2 is not passenger
        ]

    def update(self):
        for interaction in self.interactions:
            interaction.update()

    def get_total_stress(self):
        return sum(p.stress for p in self.passengers)

    def get_panicked_passengers(self):
        return [p for p in self.passengers if p.is_panicked()]


class PassengerGenerator:

    NAMES = ["Rakoto", "Rasoa", "Naina", "Tiana", "Hery", "Voahangy", "Fara", "Njaka"]
    DESTINATIONS = ["Antananarivo", "Antsirabe", "Fianarantsoa", "Toliara", "Mahajanga", "Toamasina"]

    def generate_passenger(self):
        name = random.choice(self.NAMES)
        destination = random.choice(self.DESTINATIONS)
        passenger = Passenger(name, destination)
        passenger.preferences = PassengerPreference(
            likes_music=random.choice([True, False]),
            temperature=random.randint(18, 28),
            likes_speed=random.choice([True, False]),
        )
        return passenger

    def generate_group(self, size):
        return [self.generate_passenger() for _ in range(size)]