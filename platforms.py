# ======================== platforms.py ========================

import os
import random
import pygame
from config import ASSETS_DIR, PLATFORM_SIZE, MOVING_PLATFORM_SPEED

# Chargement des différentes images de plateformes
platform_green_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_green.png"))
platform_green_img = pygame.transform.scale(platform_green_img, PLATFORM_SIZE)

platform_blue_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_blue.png"))
platform_blue_img = pygame.transform.scale(platform_blue_img, PLATFORM_SIZE)

platform_brown_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_brown.png"))
platform_brown_img = pygame.transform.scale(platform_brown_img, PLATFORM_SIZE)

platform_spring_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_spring.png"))
platform_spring_img = pygame.transform.scale(platform_spring_img, (PLATFORM_SIZE[0], PLATFORM_SIZE[1] + 10))

# Dictionnaire d'accès aux images selon le type de plateforme
platform_images = {
    "green": platform_green_img,
    "blue": platform_blue_img,
    "brown": platform_brown_img,
    "spring": platform_spring_img
}


# ======================== PARTIE 2.1 ========================
def create_platform(x, y, platform_type):
    """
    Crée et retourne un dictionnaire représentant une plateforme.

    Le dictionnaire ci-dessous représente pour l'instant correctement une
    plateforme verte. Votre travail consiste à le généraliser afin qu'il
    représente aussi correctement les plateformes bleues, marron et à ressort.
    """

    platform = {
        "x": float(x),
        "y": float(y),
        "type": platform_type,    # Remplace "green" par platform_type pour que le type change selon la plateforme
        "image": platform_images[platform_type],  # Remplace plateform_image["green"] par platform_image[plateform_type]
        "vx": 0.0,                      
        "active": True,
        "width": PLATFORM_SIZE[0],
        "height": PLATFORM_SIZE[1]          
    }
    
    if platform_images == "blue": 
        platform["vx"]= MOVING_PLATFORM_SPEED
    if platform_images == "spring":
        platform["height"] += 10

    #if pour si la plateforme est bleue, sa vitesse horizontale correspond à MOVING_PLATFORM_SPEED
    #if pour si la plateforme est un spring, sa on ajoute 10px à sa hauteur
        
    # TODO : Modifiez le dictionnaire ci-dessus pour qu'il dépende réellement
    # de l'argument platform_type.
    #
    # Contraintes :
    # - l'image doit être obtenue à partir de platform_images ;
    # - une plateforme bleue se déplace à MOVING_PLATFORM_SPEED ;
    # - une plateforme à ressort est 10 pixels plus haute ;
    # - les autres plateformes sont immobiles et gardent la hauteur normale.

# ===========================================================


# ======================== PARTIE 2.2 ========================
def choose_platform_type(green_probability, blue_probability, spring_probability):
    nombre = random.random()
    if nombre <= green_probability:
        return "green"
    elif nombre <= green_probability + blue_probability:
        return "blue"
    elif nombre <= green_probability + blue_probability + spring_probability:
        return "spring"
    else:
        return "brown"

    """
    Question pour la Prof: Est-ce qu'on inclut la probabilité de chaque dans le premier interval
    ou dans le prochain?
    """

    """
    Description code:
    1. random.random() donne un nombre entre 0 et 1
    2. Si le nombre est entre 0 et la probabilité de la plateforme verte 
       (incluant 0 et prob. verte), on retourne "green"
    3. Si le nombre est entre la probabilité de la plateforme verte et celle de la bleue 
       (excluant prob. verte et incluant prob.bleue), on retourne "blue"
    4. Si le nombre est entre la probabilité de la plateforme bleue et celle de la spring 
       (excluant prob. bleue et incluant prob. spring), on retourne "spring"
    5. Sinon, (le nombre est plus grand grand que les trois premières probabilités réunies), 
       on retourne "brown"
    """
    # Attention : les seuils utilisés avec random.random() doivent être
    # cumulatifs.

# ===========================================================

