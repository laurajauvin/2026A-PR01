# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    # Mettez à jour la vitesse verticale puis la position verticale
    # du Doodle à partir de GRAVITY.
    doodle_dict["vel_y"]+= GRAVITY #applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y)
    doodle_dict["y"]+= doodle_dict["vel_y"] #met à jour la position y du Doodle selon la nouvelle vitesse
    return

# ===========================================================


# ======================== PARTIE 1.2 ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    # Gérez les déplacements gauche/droite et mettez à jour
    # simultanément la direction et l'image du Doodle.
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        doodle_dict["x"] -= DOODLE_SPEED
        doodle_dict["direction"] = "left"
        doodle_dict["image"] = doodle_left_img

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        doodle_dict["x"] += DOODLE_SPEED
        doodle_dict["direction"] = "right"
        doodle_dict["image"] = doodle_right_img


    #Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.

    if doodle_dict["x"] < - DOODLE_WIDTH: #si le doodle est complètement sorti à gauche (-60), 
        doodle_dict["x"] = SCREEN_WIDTH   #le remet à la droite (position SCREEN_WIDTH (576))

    elif doodle_dict["x"] > SCREEN_WIDTH: #si le doodle est complètement sorti à droite (576),
        doodle_dict["x"] = -DOODLE_WIDTH #le remet à la gauche (position -DOODLE_WIDTH (-60))
        

    return

# ===========================================================


# ======================== PARTIE 2.3 ========================
def move_platforms():
    for platform in PLATFORMS: 
        if platform["type"] == "blue":
            platform["x"] += (platform["vx"])
            if platform["x"] >= SCREEN_WIDTH - PLATFORM_WIDTH:
                (platform["vx"]) = -(platform["vx"])
                platform["x"] = SCREEN_WIDTH - PLATFORM_WIDTH
            if platform["x"] <= 0:
                (platform["vx"]) = -(platform["vx"])
                platform["x"] = 0
    return
    
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """

# ===========================================================


# ======================== PARTIE 3.2 ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
   
    # Implémentez la détection d'un atterrissage.
    #
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.
    for platform in PLATFORMS:
        if platform["active"] and doodle_dict["vel_y"] > 0: # vérifie que Doodle descend (va vers le bas)
            #crée les rectangles du Doodle et des plateformes selon leurs caractéristiques
            doodle_rect = pygame.Rect( 
                doodle_dict["x"],
                doodle_dict["y"],
                DOODLE_WIDTH,
                DOODLE_HEIGHT
            )
            platform_rect = pygame.Rect(
                platform["x"],
                platform["y"],
                platform["width"],
                platform["height"]
            )
            if rects_collide(doodle_rect, platform_rect): #vérifie si doodle et la plateforme se touchent
                pieds_actuels = doodle_dict["y"] + DOODLE_HEIGHT #calcule la position des pieds sur la plateforme
                #doodle_dict["y"]: "tête" du Doodle (coin supérieur gauche de son rectangle), en additionnant avec DOODLE_HEIGHT: donne position de ses pieds 
                pieds_avant = pieds_actuels - doodle_dict["vel_y"] #retire le déplacement causé par la vitesse pour retrouver position précédente des pieds 
                
                if (platform["y"] -14 <= pieds_actuels <= platform["y"] + 14) and pieds_avant <= platform["y"] + 14: #vérifie si Doodle est actuellement dans les bornes acceptées de distance de la plateforme ET s'il était au dessus de la plateforme avant
                    #platform["y"] - 14: max, platform["y"] + 14: min
                    if platform["type"] == "spring":
                        doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY

                    elif platform["type"] == "brown":
                        doodle_dict["vel_y"] = JUMP_VELOCITY
                        platform["active"] = False # quand la plateforme est brown, elle deient inactive après avoir appliqué JUMP_VELOCITY

                    else: # si la plateform est green ou blue, donne la vélocité de base
                        doodle_dict["vel_y"] = JUMP_VELOCITY 

                    return # permet qu'un seul rebond soit traité par appel de la fonction
                            # évite que le Doodle rebondisse sur plusieurs plateformes en même temps s’il est en collision avec plusieurs


# ===========================================================


# ======================== PARTIE 3.3 ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    # Lorsque le Doodle dépasse le seuil de caméra, il doit rester
    # visuellement au seuil pendant que les plateformes sont déplacées vers
    # le bas de la même distance.
    #
    # Le score doit représenter la distance verticale ainsi parcourue et le
    # meilleur score doit être mis à jour. Les plateformes sorties sous
    # l'écran doivent être retirées, puis de nouvelles plateformes générées.

    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD: #lorsque le doodle est plus haut que le seuil de caméra
        defilement = CAMERA_SCROLL_THRESHOLD - doodle_dict["y"] #calcule distance de défilement nécessaire pour prochaines étapes

        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD #repositionne le doodle au seuil de caméra
        doodle_dict["score"] += defilement # mise à jour du score selon le défilement vertical
        
        if doodle_dict["score"] > doodle_dict["high_score"]: # si le score est plus grand que high score, 
            doodle_dict["high_score"] = doodle_dict["score"] # high score est mis à jour
        
                
        for platform in PLATFORMS:
            platform["y"] += defilement #fait descendre toutes les plateformes de la distance de défilement 

        PLATFORMS[:] = [platform for platform in PLATFORMS if platform["y"] < SCREEN_HEIGHT] # on veut enlever les platformes qui sont en dessous de SCREEN_HEIGHT,
        # copie ce contenu dans la liste originale PLATFORMS sans en créer une nouvelle      # donc on garde celles qui sont au-dessus de SCREEN_HEIGHT

        generate_new_platforms() #on appelle la fonction qui va générer de nouvelles plateformes au-dessus de l'écran

    return



# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """

    # Changement de probabilité pour qu'elles correspondent aux contraintes des nouvelles plateformes
    green_prob = 55/100
    blue_prob = 20/100
    spring_prob = 13/100

    """ Assignation d'une coordonnée y de base pour highest_platform au bas de l'écran pour que n'importe 
        quelle plateforme soit plus haute """

    highest_platform = {"x" : SCREEN_WIDTH/2, "y": SCREEN_HEIGHT} 


    """ for loop pour déterminer la plateforme la plus haute en comparant la coordonnée y de la plateforme
        précédente de la loop avec la nouvelle """
    
    for platform in PLATFORMS:
        if platform["y"] < highest_platform["y"]:
            highest_platform = platform

    """ Assignation des coordonnées de base de x et y à celles de la plateforme la plus haute """
    
    current_x = highest_platform["x"]
    current_y = highest_platform["y"]

    """ Utilisation de la logique de la section 2.2 (créer les plateformes initiales). La seule chose modifiée
        est l'ordre: on assigne une nouvelle valeur aléatoire à current_x et current_y avant d'ajouter la 
        nouvelle plateforme à la liste pour ne pas créer une plateforme par dessus highest_platform"""

    while (current_y +  MIN_PLATFORM_GAP) > 0:
        current_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        current_y = current_y - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
        type_platform = choose_platform_type(green_prob,blue_prob,spring_prob)
        nouv_platform = create_platform(current_x,current_y,type_platform)
        PLATFORMS.append(nouv_platform)

    return PLATFORMS

    # Retourner la nouvelle liste de plateforme créée à mesure que les plateformes descendent

# ===========================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
        r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
        r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )
