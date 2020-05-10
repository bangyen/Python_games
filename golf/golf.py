import pygame
import random
import time
import os
import math

#Window setup
pygame.font.init()
WIDTH, HEIGHT = 1200, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golf Game")

#load the game assets
golf_man = pygame.image.load(os.path.join("golf/assets/golf_man.png"))
background = pygame.transform.scale(pygame.image.load(os.path.join("golf/assets/background_pixel_golf.png")), (WIDTH, HEIGHT))

class GolfPlayer():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.power = 0
        self.img = golf_man
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

class Ball():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, window):
        pygame.draw.circle(window, (0,0,0), (self.x, self.y), self.radius)
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius - 1)

    @staticmethod
    def ball_path(start_x, start_y, power, angle, time):
        """Projectile motion"""
        gravity_constant = -9.8

        velocity_x = math.cos(angle) * power #(r*cos(theta), r*sin(theta))
        velocity_y = math.sin(angle) * power

        dist_x = velocity_x * time # s = v * t the first ever physic equation that I learned
        dist_y = (velocity_y * time) + (((gravity_constant / 2) * (time)**2) / 2)

        new_x = round(dist_x + start_x)
        new_y = round(start_y - dist_y)
        print(power)
        #print(angle)
        #print(time)
        print(new_x, new_y)

        return (new_x, new_y)



def collide(obj1, obj2):
    """This function uses pygame mask's overlap to check if obj1 hits the obj2"""
    offset_x = obj2.x - obj1.x #The difference between obj1 and obj 2
    offset_y = obj2.y - obj1.y  
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None # (x,y)

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    #Golf character variables
    golf_stickman_x_margin = 13
    golf_stickman_y_margin = 86
    golf_stickman = GolfPlayer(golf_stickman_x_margin, HEIGHT - golf_stickman_y_margin)

    #Golf ball variables
    golf_ball = Ball(100, HEIGHT - 8 , 8, (255,255,255))
    ball_start_x = 0
    ball_start_y = 0
    time = 0
    power = 0
    angle = 0
    shoot = False

    def find_angle(pos):
        """Takes a pos = tuple which is the mouse position and returns 
        the angle of the golf startx and starty which is the 
        x and y pos of the golf ball and"""

        start_x = golf_ball.x
        start_y = golf_ball.y

        try:
            angle = math.atan((start_y - pos[1]) / (start_x - pos[0])) 
        except: #Goes to the except clause because arctan(x) goes to pi/2 when x goes to infinity
            angle = math.pi / 2 #arctan(x) highest value is pi/2

        if pos[1] > start_x and pos[1] > start_y: #First quadrant
            angle = (2 * math.pi) - angle
        elif pos[0] < start_x and pos[1] > start_y: #Second quadrant
            angle = math.pi + abs(angle)
        elif pos[0] < start_x and pos[1] < start_y: #Third quadrant
            angle = math.pi - angle
        elif pos[0] > start_x and pos[1] < start_y: #Fourth quadrant 
            angle = abs(angle)
        
        return angle
        
    def redraw_window():
        """This function draws all the objects 
        and blits the text on the window"""

        WIN.blit(background, (0,0))

        golf_stickman.draw(WIN)
        golf_ball.draw(WIN)

        if shoot:
            pass
        else:
            pygame.draw.line(WIN, (255,255,255), line[0], line[1])

        pygame.display.update()

    while run:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        line = [(golf_ball.x, golf_ball.y), (mouse_x, mouse_y)]
        redraw_window()

        if shoot:
            """Still need to figure out to stop the ball when 
            it hits a rectangle or another surface"""
    
            time += 0.2 #how fast the ball goes, depends on how fast your computer is
            if golf_ball.y < HEIGHT:
                next_position = Ball.ball_path(ball_start_x, ball_start_y, power, angle, time)
                golf_ball.x = next_position[0]
                golf_ball.y = next_position[1]
                print(next_position)
            else:
                shoot = False
                golf_ball.y = HEIGHT - golf_ball.radius
                golf_stickman.x, golf_stickman.y = golf_ball.x - 90, golf_ball.y - golf_stickman_y_margin


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("SHOOT")
                if shoot == False:
                    shoot = True
                    ball_start_x = golf_ball.x
                    ball_start_y = golf_ball.y
                    time = 0
                    vector = [line[1][0] - line[0][0], line[1][1] - line[0][1]]
                    power = (math.sqrt((vector[0])**2 + (vector[1])**2)) / 8 #get the length of the line, divide by 8 so it is not a big number
                    angle = find_angle((mouse_x, mouse_y))
        

main()

        


        
    

