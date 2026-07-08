# TaxiBrousseRush
taxibrousse_rush/
│
├── main.py                 # Point d'entrée
├── config.py               # Constantes (couleurs, FPS, dimensions)
├── assets/
│   ├── images/             # Sprites (véhicules, obstacles, décors)
│   ├── sounds/             # Bruitages (moteur, klaxon, accident)
│   └── fonts/              # Polices
├── models/
│   ├── vehicle.py          # Classe TaxiBrousse
│   ├── road.py             # Classe RoadSegment
│   ├── obstacle.py         # Classes filles (NidPoule, Pont, Bouchon, Animal)
│   ├── passenger.py        # Classe Passenger
│   └── level.py            # Classe Level + générateur de niveaux
├── controllers/
│   ├── game_controller.py  # Boucle principale, états (menu, jeu, gameover)
│   ├── physics_engine.py   # Calculs de friction, adhérence, collisions
│   └── ai_controller.py    # Mouvement des obstacles animaux/voitures
├── views/
│   ├── renderer.py         # Dessin du décor, routes, HUD
│   ├── camera.py           # Suivi du véhicule (scroll)
│   └── ui.py               # Menus, boutons, indicateurs
└── utils/
    ├── score_manager.py    # Calcul du score, sauvegarde
    ├── weather_system.py   # Génération aléatoire de météo
    └── collision.py        # Détection de collision (AABB, cercle)

misafidiana entre assets, views, utils