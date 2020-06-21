import pygame

#pygame basic variables stuff
TITLE = "Adventurous Joe"
WIDTH, HEIGHT = 1100, 500
CLOCK = pygame.time.Clock()
FPS = 60
FONT = "comicsans" 

#pygame init stuff
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Adventurous Joe")

#Layers
PLATFORM_LAYER = 2
MAIN_CHARACTER_LAYER = 3
TRAP_LAYER = 1
FIREBALL_LAYER = 1
TITLE_LAYER = 2
PIXEL_SIGN_LAYER = 2

#Main character's properties
GRAVITY = 0.8
ACCELERATION = 0.345 #0.4
FRICTION = -0.09 # 0.07
PLAYER_JUMP = -18

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKYBLUE = (50, 153, 204)
BUTTON_COLOR = (14, 47, 146)

#traps properties
SPIKE_HEIGHT = 40
LAVA_BALL_FRICTION = -0.09

#Additional constants
PLAY_BTN_WIDTH = 200
PLAY_BTN_HEIGHT = 70
CAMERA_FOCUSPOINT_X_POS = 230 #Can change to 130 otherwise not
BOTTOM_PLATFORM_Y_COORDINATE = HEIGHT - 40
