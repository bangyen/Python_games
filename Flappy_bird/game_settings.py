import pygame

#Game initialization
TITLE = "Flappy Bird"
HIGHSCORE_FILE = "highscore.txt"
WIDTH, HEIGHT = 400, 650
FPS = 60
FONT_NAME = "arial"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

#Layers for the sprites
BIRD_LAYER = 2

#Bird properties
BIRD_ACCELERATION = 0.5
#BIRD_FRICTION = -0.08 #Depends on how fast your computer is, increase the friction if your computer is fast
BIRD_GRAVITY = 0.8
BIRD_AIR_RESISTANCE = -0.09
BIRD_FLY_UP = -14

#pygame intit and display functions
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

#colors
BGCOLOR = (65, 105, 225)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)