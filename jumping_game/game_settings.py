import pygame

#Game initialization
TITLE = "Jumping Game"
HIGHSCORE_FILE = "highscore.txt"
WIDTH, HEIGHT = 480, 600
FPS = 60
FONT_NAME = "arial"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#pygame intit and display functions
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Jump Game")
clock = pygame.time.Clock()

#Sound
TITLE_MUSIC = "Titlemusic_supermario.ogg"
BACKGROUND_MUSIC = "Supermariobonus.ogg"
GAMEOVER_MUSIC = "smb_gameover.wav"
JUMP_SOUND = "super_jump.wav"
JUMP_BOOST_SOUND = "Powerup_jump.wav"

#Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.08 #Depends on how fast your computer is, increase the friction if your computer is fast
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -20
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
JUMP_BOOST_LAYER = 1
ENEMY_LAYER = 2
CLOUD_LAYER = 0

#Game properties
BOOST_POWER_JUMP = 50
BOOST_POW_FREQUENCY_SPAWN_NUM = 7 #How likely every time that a platform spawns that it has a powerup
ENEMY_FREQUENCY = 5000 #milliseconds 

#platforms coordinates
PLATFORM_COORDINATES_LIST = [
                            (0, HEIGHT - 40), #(x, y)
                            (WIDTH / 2, HEIGHT * 3/4),
                            (WIDTH / 2 + 40, HEIGHT / 2),
                            (WIDTH * 3/4, HEIGHT * 1/4), 
                            (175, 100)
                            ]

#colors
BGCOLOR = (51, 154, 169)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)