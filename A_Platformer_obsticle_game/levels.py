from sprites import *
from game_settings import *


"""Functions for blitting the next levels"""
def opening_level_part2(main_player, initial_platform, game):
    for i in range(3):
        Platform(WIDTH + 100 + (initial_platform.get_size() * i), HEIGHT - 100, game)
        Platform(WIDTH + 300 + (initial_platform.get_size() * i), HEIGHT / 2, game)
        Platform(WIDTH + 600 + (initial_platform.get_size() * i), HEIGHT - 50, game)

    Platform(2*WIDTH - 300, BOTTOM_PLATFORM_Y_COORDINATE, game)


def level_1(main_player, initial_platform, game):
    """Level 1 and the opening level are together. 
    When the camera's x position reaches WIDTH - 50 
    the next level is blit on the window with the coordinates 
    x = WIDTH + some number, y = some number"""

    for i in range(24):
        if 17 <= i <= 19:
            if i == 18 or i == 19:
                Lava(WIDTH + (initial_platform.get_size() * i), BOTTOM_PLATFORM_Y_COORDINATE, game, True)
            else:
                Lava(WIDTH + (initial_platform.get_size() * i), BOTTOM_PLATFORM_Y_COORDINATE, game, False)
        else:
            Platform(WIDTH + (initial_platform.get_size() * i), BOTTOM_PLATFORM_Y_COORDINATE, game)
    
    #Spawn a boulder
    SingleFrameSpriteTrap(2*WIDTH, HEIGHT / 4, game, True, False, True)

    #Spawn an axes
    SingleFrameSpriteTrap(WIDTH + 200, 70, game, True, False, False, True)
    SingleFrameSpriteTrap(WIDTH + 400, 10, game, True, False, False, True)

def level_2(main_player, initial_platform, game):
    for i in range(3):
        Platform(WIDTH + 150 + (initial_platform.get_size() * i), HEIGHT / 2 + 100, game)





    


