import pygame

#Game initialization
TITLE = "Jumping Game"
HIGHSCORE_FILE = "highscore.txt"
WIDTH, HEIGHT = 480, 600
FPS = 60
FONT_NAME = "arial"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#pygame inti and display functions
pygame.font.init()
pygame.display.set_caption("Jump Game")
clock = pygame.time.Clock()

#Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.08 #Depends on how fast your computer is, increase the friction if your computer is fast
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -20

#platforms
PLATFORM_COORDINATES_LIST = [
                            (0, HEIGHT - 40), #(x, y)
                            (WIDTH / 2, HEIGHT * 3/4),
                            (WIDTH / 2 + 40, HEIGHT / 2),
                            (WIDTH * 3/4, HEIGHT * 1/4), 
                            (175, 100)
                            ]



#colors
BGCOLOR = (0, 204, 169)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)