import random 
import time
import os
import pygame

#Window setup
pygame.font.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Classic Pong Game")

#load pixel images
orange_pixel_plank = pygame.image.load(os.path.join("pong/assets", "blue_pixel_plank.png"))
blue_pixel_plank = pygame.image.load(os.path.join("pong/assets", "orange_pixel_plank.png"))

class Plank():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = None

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move_up(self):
        pass

    def move_down(self):
        pass

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class Player_1(Plank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = orange_pixel_plank
        self.x = - 24


class Player_2(Plank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = blue_pixel_plank
        self.x = WIDTH - self.get_width() / 2 - 20 #the x coordinate is a constant

class Ball():
    pass

def main():
    run = True
    FPS = 60

    #score variables
    score_1 = 0
    score_2 = 0

    #players
    player1 = Player_1(0, HEIGHT / 2 - 50)
    player2 = Player_2(200, HEIGHT / 2 - 50)

    
    clock = pygame.time.Clock()
    def redraw_window():
        """This function draws the objects and
         blits the text on the window"""
        WIN.fill((0,0,0))


        player1.draw(WIN)
        player2.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()




        #Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        #Key handlers
        keys = pygame.key.get_pressed()


main()
    

