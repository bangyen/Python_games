"""The classic retro game pong"""
"""Author: Kristofer Gauti"""

import random 
import time
import os
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
        self.velocity = 5
        self.img = red_pixel_pong_ball
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, down, right):
        if down:
            self.x += 0
            self.y += self.velocity
        else:
            self.x += 0
            self.y -= self.velocity

        if right:
            self.x += self.velocity
            self.y += 0
        else:
            self.x -= self.velocity
            self.y += 0

    def increase_velocity(self):
        self.velocity += 0.25
            
    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


def collide(obj1, obj2):
    """This function uses pygame mask's overlap to check if obj1 hits the obj2"""
    offset_x = obj2.x - obj1.x #The difference between obj1 and obj 2
    offset_y = obj2.y - obj1.y  
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None # (x,y)


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
    plank_velocity = 5
   
    #The ball variables
    ball_list = []
    move_down = True
    ball_left_direction = True

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
        if len(ball_list) == 1:
            for ball in ball_list:
                ball.draw(WIN)
    
        pygame.display.update()

    def collide_ball_player2(player2, ball):
        if collide(player2, ball):
            ball.increase_velocity()
            ball.move(True, False)
            return True 
        return False

    def collide_ball_player1(player1, ball):
        if collide(player1, ball):
            ball.increase_velocity()
            ball.move(True, True)
            return True
        return False

    while run:
        clock.tick(FPS)
        redraw_window()

        if ball_list == []:
            ball = Ball(WIDTH / 2, random.randrange(5, HEIGHT - 5))
            ball_list.append(ball)

        if ball.x + ball.get_width() <= 0:
            ball_list.remove(ball)
            score_2 += 1
        elif ball.x >= WIDTH:
            ball_list.remove(ball)
            score_1 += 1

        """If the ball does not collide with player2 (arrow keys),  
        the ball goes to the left and it moves down then set its boundaries for moving up and down
        If the ball does not collide with player2 (arrow keys) and the ball goes to the right then 
        set its up and down boundaries. If the ball does collide with either player1 or player2 then
        ball_left_direction = True or False otherwise"""
        for ball in ball_list:
            if not collide_ball_player2(player2, ball): #player2's turn (arrow keys)
                if ball_left_direction:
                    if move_down:
                        if ball.y + ball.get_height() < HEIGHT + 35: 
                            ball.move(True, True)
                        else:
                            move_down = False
                    else:
                        if ball.y > -35: #-35 because of the margin of the ball png
                            ball.move(False, True)
                        else:
                            move_down = True
                else:
                    if collide_ball_player1(player1, ball): #player1's turn (w and s)
                        ball_left_direction = True
                    else:
                        if move_down:
                            if ball.y + ball.get_height() < HEIGHT + 35: 
                                ball.move(True, False)
                            else:
                                move_down = False
                        else:
                            if ball.y > -35: #-35 because of the margin of the ball png
                                ball.move(False, False)
                            else:
                                move_down = True
            else:
                ball_left_direction = False

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
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_b]:
            main_menu()

def main_menu():
    main_menu_font = pygame.font.SysFont("comicsans", 70)
    instruction_font = pygame.font.SysFont("comicsans", 30)

    run = True
    while run:
        WIN.fill((0,0,0))

        title_label = main_menu_font.render("Main menu", 1, (255,255,255))
        instruction_label_p1 = instruction_font.render("Player 1: Move up (arrow key up) | Move down (arrow key down)", 1, (255,255,255))
        instruction_label_p2 = instruction_font.render("Player 2: Move up (w) | Move down (s)", 1, (255,255,255))
        mouse_click_label = instruction_font.render("Click anywhere on the screen to begin the game!", 1, (255,255,255))
        WIN.blit(title_label,(WIDTH / 2 - title_label.get_width() / 2, 10))
        WIN.blit(instruction_label_p1, (WIDTH / 10, 2*HEIGHT / 7))
        WIN.blit(instruction_label_p2, (WIDTH / 10, 2*HEIGHT / 5))
        WIN.blit(mouse_click_label, (WIDTH / 2 - mouse_click_label.get_width() / 2, 3*HEIGHT / 4))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            quit()

main_menu()
        