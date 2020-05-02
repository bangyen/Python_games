import random 
import time
import os
import pygame

#Window setup
pygame.font.init()
WIDTH, HEIGHT = 700, 450
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

    def move_up(self, velocity):
        self.y -= velocity

    def move_down(self, velocity):
        self.y += velocity

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

    #fonts
    score_font = pygame.font.SysFont("comicsans", 70)

    #score variables
    score_1 = 0
    score_2 = 0

    #players
    player1 = Player_1(0, HEIGHT / 2 - 50)
    player2 = Player_2(200, HEIGHT / 2 - 50)
    velocity = 7

    
    clock = pygame.time.Clock()
    def redraw_window():
        """This function draws the objects and
         blits the text on the window"""
        WIN.fill((0,0,0))

        score_1_label = score_font.render("{}".format(score_1),1, (255,255,255))
        score_2_label = score_font.render("{}".format(score_2),1, (255,255,255))

        #Draw the text
        WIN.blit(score_1_label, (WIDTH / 4, 40))
        WIN.blit(score_2_label, ((3 * WIDTH) / 4, 40))

        #draw the dotted line 
        space_margin = 0
        for i in range(0,HEIGHT):
            space_margin += 50
            pygame.draw.line(WIN, (255,255,255), (WIDTH / 2, 0), (WIDTH / 2, i))
            pygame.draw.line(WIN, (0,0,0), (WIDTH / 2, space_margin), (WIDTH / 2, i)) #nope :(

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
        #for player1
        if keys[pygame.K_w] and player1.y > 0:
            player1.move_up(velocity)
        if keys[pygame.K_s] and player1.y < HEIGHT - player1.get_height():
            player1.move_down(velocity) 
        #for player2
        if keys[pygame.K_UP] and player2.y > 0:
            player2.move_up(velocity) 
        if keys[pygame.K_DOWN] and player2.y < HEIGHT - player2.get_height():
            player2.move_down(velocity)


main()
    

