import pygame

#Game initialization
TITLE = "Flappy Bird"
HIGHSCORE_FILE = "highscore.txt"
WIDTH, HEIGHT = 410, 650 #650
FPS = 60
FONT_NAME = "arial"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

#Layers for the sprites
GRASS_LAYER = 2
BIRD_LAYER = 2
PIPE_LAYER = 1

#pygame intit and display functions
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

#Bird properties
BIRD_GRAVITY = 0.8
BIRD_FLY_UP = -11

#Pipe properties
SPACE_BETWEEN_PIPES = 200
PIPE_MOVING_VELOCITY = 2.5
GROUND_CONSTANT = 230
SKY_CONSTANT = 0 
PIPE_UPWARD_COORDINATES = [
                          (WIDTH + WIDTH/2 + 1*SPACE_BETWEEN_PIPES, SKY_CONSTANT - 20),
                          (WIDTH + WIDTH/2 + 2*SPACE_BETWEEN_PIPES, SKY_CONSTANT - 110),
                          (WIDTH + WIDTH/2 + 3.01*SPACE_BETWEEN_PIPES, SKY_CONSTANT - 230)
                          #auka pipes fyrir random functionid i while lykkjunni i update
                          ]

PIPE_DOWNWARD_COORDINATES = [ 
                            (WIDTH + WIDTH/2 + 1*SPACE_BETWEEN_PIPES, GROUND_CONSTANT + 220),
                            (WIDTH + WIDTH/2 + 2*SPACE_BETWEEN_PIPES, GROUND_CONSTANT + 120), #gc=230 + something
                            (WIDTH + WIDTH/2 + 3.01*SPACE_BETWEEN_PIPES, GROUND_CONSTANT)
                            #auka pipes fyrir random functionid i while lykkjunni i update
                            ]

#colors
BGCOLOR = (65, 105, 225)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)