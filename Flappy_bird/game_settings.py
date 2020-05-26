import pygame
import os
import random

#Game initialization
TITLE = "Flappy Bird"
HIGHSCORE_FILE = "highscore.txt"
WIDTH, HEIGHT = 410, 650 #650
FPS = 60
FONT_NAME = "arial"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

#Bakcground
BG = pygame.transform.scale(pygame.image.load(os.path.join(os.path.join(os.path.dirname(__file__), "sprite_img"),"background_night.png")),(WIDTH, HEIGHT))

#Layers for the sprites
GRASS_LAYER = 2
START_BIRD_LAYER = 2
BIRD_LAYER = 2
PIPE_LAYER = 1
GAME_OVER_LAYER = 3
SCORE_BOARD_LAYER = 3
PLAYBTN_LAYER = 3
DEAD_BIRD_LAYER = 4

#pygame intit and display functions
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

#Bird properties
BIRD_FLY_UP = -11
BIRD_START_GRAVITY = 0.8
BIRD_START_POS_X = WIDTH / 2 - 150
BIRD_START_POS_Y = HEIGHT / 2

#Pipe properties
SPACE_BETWEEN_PIPES = 200
PIPE_MOVING_VELOCITY = 2.5
GROUND_CONSTANT = 230
SKY_CONSTANT = 0 

#colors
BGCOLOR = (65, 105, 225)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)