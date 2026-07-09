"""
main.py — TaxiBrousse Rush (prototype 2 jours)

Lancer avec : python main.py

Contrôles :
  W / Flèche haut   : accélérer
  S / Flèche bas     : freiner / reculer
  A / D ou flèches   : direction
  R                   : recommencer après un game over

Objectif du MVP :
  - conduire le plus loin possible en 60 secondes
  - éviter/subir les nids-de-poule (ralentissement) et les zébus (collision)
  - score = distance parcourue - pénalités de sécurité
"""
import random
from ursina import (
    Ursina, Entity, Sky, DirectionalLight, AmbientLight,
    Text, color, time, camera, Vec3, window, destroy
)

from car import Car
from road import build_road, ROAD_LENGTH, ROAD_WIDTH
from obstacles import Pothole, Zebu



app = Ursina()
window.title = "TaxiBrousse Rush"
window.fps_counter.enabled = True
window.exit_button.visible = False
print("GPU renderer:", base.win.getGsg().getDriverRenderer())
print("GPU vendor:", base.win.getGsg().getDriverVendor())
# --- Décor ---
sky = Sky(color=color.rgb32(140, 190, 230))

road = build_road()

# --- Voiture ---
car = Car(position=(0, 0.5, 0))

# --- Camera ---
camera_pivot = Entity(
    parent=car,
    position=(0, 0, 0),
    scale=(1 / car.scale_x, 1 / car.scale_y, 1 / car.scale_z),
)
camera.parent = camera_pivot
camera.position = (0, 5, -11)
camera.rotation_x = 18
camera.fov = 90

from weather import WeatherSystem

weather = WeatherSystem(car)  # après la création de `car`

# --- Génération des obstacles le long de la route ---
NUM_POTHOLES = 14
NUM_ZEBUS = 5

obstacles = []


def spawn_obstacles():
    obstacles.clear()

    for i in range(NUM_POTHOLES):
        z = random.uniform(20, ROAD_LENGTH - 10)
        x = random.uniform(-ROAD_WIDTH / 2 + 1, ROAD_WIDTH / 2 - 1)
        obstacles.append(Pothole(position=(x, 0.05, z)))

    for i in range(NUM_ZEBUS):
        z = random.uniform(30, ROAD_LENGTH - 10)
        x = random.uniform(-ROAD_WIDTH / 2 + 2, ROAD_WIDTH / 2 - 2)
        obstacles.append(Zebu(position=(x, 0.6, z), road_width=ROAD_WIDTH))


spawn_obstacles()

# --- Score / Timer / UI ---
GAME_DURATION = 60  # secondes

game_state = {
    "time_left": GAME_DURATION,
    "distance": 0,
    "penalties": 0,
    "start_z": car.z,
    "game_over": False,
}

timer_text = Text(text="60", position=(-0.15, 0.45), scale=2, origin=(0, 0))
score_text = Text(text="Score: 0", position=(-0.85, 0.45), scale=1.5)
warning_text = Text(text="", position=(0, 0.15), scale=2, origin=(0, 0), color=color.red)

game_over_text = Text(
    text="",
    position=(0, 0.05),
    scale=3,
    origin=(0, 0),
    color=color.yellow,
)
restart_text = Text(
    text="",
    position=(0, -0.1),
    scale=1.3,
    origin=(0, 0),
)


def flash_warning(msg):
    warning_text.text = msg
    warning_text.alpha = 1


def end_game():
    game_state["game_over"] = True
    final_score = max(0, int(game_state["distance"] - game_state["penalties"] * 10))
    game_over_text.text = "ARRIVÉE !" if car.z >= ROAD_LENGTH - 15 else "GAME OVER"
    game_over_text.text += f"\nScore final : {final_score}"
    restart_text.text = "Appuie sur R pour recommencer"


def restart_game():
    game_state["time_left"] = GAME_DURATION
    game_state["distance"] = 0
    game_state["penalties"] = 0
    game_state["game_over"] = False
    car.position = (0, 0.5, 0)
    car.rotation = (0, 0, 0)
    car.speed = 0
    game_over_text.text = ""
    restart_text.text = ""

    for e in obstacles:
        destroy(e)
    spawn_obstacles()


def update():
    if game_state["game_over"]:
        return
    weather.update(car.z)

    # --- Timer ---
    game_state["time_left"] -= time.dt
    if game_state["time_left"] <= 0:
        game_state["time_left"] = 0
        end_game()

    timer_text.text = f"{int(game_state['time_left'])}s"

    # --- Distance / Score ---
    game_state["distance"] = max(0, car.z - game_state["start_z"])
    live_score = max(0, int(game_state["distance"] - game_state["penalties"] * 10))
    score_text.text = f"Score: {live_score}"

    # --- Collisions ---
    for obstacle in obstacles:
        result = obstacle.check_collision(car)
        if result == "pothole":
            flash_warning("Nid-de-poule ! Ralenti...")
        elif result == "zebu":
            game_state["penalties"] += 1
            flash_warning("Zébu sur la route ! -10 points de sécurité")

    # Fade du message d'avertissement
    if warning_text.alpha > 0:
        warning_text.alpha -= time.dt * 0.5

    # Fin de piste = victoire anticipée
    if car.z >= ROAD_LENGTH - 15:
        end_game()

    # Garde-fou simple si le joueur sort trop de la route
    if abs(car.x) > ROAD_WIDTH / 2 + 12:
        car.speed *= 0.5


def input(key):
    if key == "r" and game_state["game_over"]:
        restart_game()


app.run()
