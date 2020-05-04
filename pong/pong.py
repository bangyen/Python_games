import random 
import time
import os
import math
import pygame

#Window setup
pygame.font.init()
WIDTH, HEIGHT = 800, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Classic Pong Game")

#load pixel images
orange_pixel_plank = pygame.image.load(os.path.join("pong/assets", "blue_pixel_plank.png"))
blue_pixel_plank = pygame.image.load(os.path.join("pong/assets", "orange_pixel_plank.png"))
red_pixel_pong_ball = pygame.image.load(os.path.join("pong/assets", "red_pixel_pong_ball.png"))


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
        self.mask = pygame.mask.from_surface(self.img)

class Player_2(Plank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = blue_pixel_plank
        self.x = WIDTH - self.get_width() / 2 - 20 #the x coordinate is a constant
        self.mask = pygame.mask.from_surface(self.img)

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = red_pixel_pong_ball
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move_south_north(self, velocity, south_bool):
        if south_bool:
            self.x += 0
            self.y += velocity
        else:
            self.x += 0
            self.y -= velocity

    def move_east_west(self, velocity, east_bool):
        if east_bool:
            self.x += velocity
            self.y += 0
        else:
            self.x -= velocity
            self.y += 0
            
    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


def collide(obj1, obj2):
    """This function uses pygame mask's overlap to check if obj1 hits the obj2"""
    offset_x = obj2.x - obj1.x #The difference between obj1 and obj 2
    offset_y = obj2.y - obj1.y  
    return obj1.mask.overlap(obj2.mask, (math.floor(offset_x), math.floor(offset_y))) != None # (x,y)


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
    plank_velocity = 7

    #The ball variables
    move_down = True
    ball_plank_collistion = False
    ball = Ball(WIDTH / 2, random.randrange(5, HEIGHT - 5))
    ball_velocity = 2

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

        #Draw the dotted line 
        for i in range(0,HEIGHT, 10):
            if i % 4 == 0:
                pygame.draw.rect(WIN, (0,0,0), (WIDTH / 2, i, 5, 30))
            else:
                pygame.draw.rect(WIN, (255,255,255), (WIDTH / 2, i, 5, 30))

        #Draw the players
        player1.draw(WIN)
        player2.draw(WIN)

        #Draw the ball at with a random height position 
        ball.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        print(ball.y)

        if move_down:
            if ball.y + ball.get_height() < HEIGHT + 35: 
                ball.move_south_north(ball_velocity, True)
            else:
                move_down = False
        else:
            if ball.y > -35: #-35 because of the margin of the ball png
                ball.move_south_north(ball_velocity, False)
            else:
                move_down = True

        
        if collide(player2, ball): #collision works
            ball.move_east_west(ball_velocity, False)
        elif collide(player1, ball):
            ball.move_east_west(ball_velocity, True)
    
            
            
        #Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        #Key handlers
        keys = pygame.key.get_pressed()
        #for player1
        if keys[pygame.K_w] and player1.y > 0:
            player1.move_up(plank_velocity)
        if keys[pygame.K_s] and player1.y < HEIGHT - player1.get_height():
            player1.move_down(plank_velocity) 
        #for player2
        if keys[pygame.K_UP] and player2.y > 0:
            player2.move_up(plank_velocity) 
        if keys[pygame.K_DOWN] and player2.y < HEIGHT - player2.get_height():
            player2.move_down(plank_velocity)


main()
    

