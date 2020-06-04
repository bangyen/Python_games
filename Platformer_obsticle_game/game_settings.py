import pygame

#pygame basic variables stuff
TITLE = "Adventurous Joe"
WIDTH, HEIGHT = 800, 500
CLOCK = pygame.time.Clock()
FPS = 60
FONT = "comicsans" 

#pygame init stuff
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Adventurous Joe")

#Layers
MAIN_CHAARACTER_LAYER = 2

#Main character's properties
GRAVITY = 0.8
ACCELERATION = 0.4
FRICTION = -0.07

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKYBLUE = (50, 153, 204)
