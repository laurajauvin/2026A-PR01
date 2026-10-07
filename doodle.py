# ======================== doodle.py ========================

import os
import pygame
from config import ASSETS_DIR, DOODLE_SIZE, DOODLE_START_X, DOODLE_START_Y, LIVES, doodle_dict

# Chargement et redimensionnement des images du Doodle (gauche et droite)
doodle_left_img = pygame.image.load(os.path.join(ASSETS_DIR, "doodle_left.png"))
doodle_left_img = pygame.transform.scale(doodle_left_img, DOODLE_SIZE)

doodle_right_img = pygame.image.load(os.path.join(ASSETS_DIR, "doodle_right.png"))
doodle_right_img = pygame.transform.scale(doodle_right_img, DOODLE_SIZE)

# ======================== PARTIE 1.1 ========================

# Initialisation du dictionnaire global du Doodle
doodle_dict.update({
    "x": DOODLE_START_X, #position de départ du Doodle (au-dessus de la plateforme verte)
    "y": DOODLE_START_Y,
    "vel_y": 0.0,
    "direction": "right",  # "left" ou "right"
    "score": 0,
    "high_score": 0,
    "lives": LIVES,
    "image": doodle_right_img
})

# ===========================================================
