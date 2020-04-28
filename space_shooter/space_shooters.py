import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

#Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("space_shooter/assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("space_shooter/assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("space_shooter/assets", "pixel_ship_blue_small.png"))

#Main character 
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("space_shooter/assets", "pixel_ship_yellow.png"))

#Load lasers
RED_LASER = pygame.image.load(os.path.join("space_shooter/assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("space_shooter/assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("space_shooter/assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("space_shooter/assets", "pixel_laser_red.png"))

HEART = pygame.image.load(os.path.join("space_shooter/assets", "pixel_heart.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("space_shooter/assets", "background-black.png")),(WIDTH, HEIGHT))

class Heart():
    def __init__(self, x, y):
        self.x = y
        self.y = y
        self.img = HEART
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)

class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity
    
    def offscreen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj) #Pass the whole obj and the whole laser object into the collide function


#Parent class
class Ship():
    COOLDOWN = 30 #8 With cheats activated
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, velocity, obj):
        self._cool_down()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.offscreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj): #check if the laser has hit the obj
                obj.health -= 10
                self.lasers.remove(laser)

    def _cool_down(self):
        """half second cooldown before shooting again"""
        if self.cool_down_counter >= self.COOLDOWN: #self.COOLDOWN = 30
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        """If the user presses space, when self.lasers
         is empty the ship cant shoot laser"""

        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

#Children of the Ship class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) #pygame.mask handles the ships collision
        self.max_health = health
        self.healthbar_size = 10

    def move_lasers(self, velocity, objs):
        self._cool_down()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.offscreen(HEIGHT): #if the laser is off the screen
                self.lasers.remove(laser)
            else: #if the laser is not off the screen
                for obj in objs: #run through the object list
                    if laser.collision(obj): #if the laser has collided with the object
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def _healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), self.healthbar_size))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), self.healthbar_size))

    def draw(self, window):
        """Overwrite the draw method from the parent class Ship"""
        super().draw(window)
        self._healthbar(window)

    def get_player_healthbar_height(self):
        return self.healthbar_size


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP,RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        """When the enemy shoots"""
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img) #-15 to center the shoot
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    """This function uses pygame mask's overlap to check if obj1 hits the obj2"""
    offset_x = obj2.x - obj1.x #The difference between obj1 and obj 2
    offset_y = obj2.y - obj1.y  
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None # (x,y)

class Cheats():
    def __init__(self):
        self.cheat_lives = 0
        self.activation_fastshot = "Deactivated" 
        self.activation_endlesslife = "Deactivated"

    def display_cheet_menu(self):
        title_font = pygame.font.SysFont("comicsans", 70)
        back_font = pygame.font.SysFont("comicsans", 25)
        setting_font = pygame.font.SysFont("comicsans", 25)

        title_label = title_font.render("Options", 1, (255,255,255))
        back_label = back_font.render("Press b to go back on the main menu screen", 1, (255,255,255))
        no_cooldown_label = setting_font.render("Press 1 to activate a faster shooting gun for the main player ship: " + self.activation_fastshot, 1, (255,255,255))
        endless_lives_label = setting_font.render("Press 2 to activate endless lives: " + self.activation_endlesslife, 1, (255,255,255))
        reset_label = setting_font.render("Press r to reset everything", 1, (255,255,255))
        
        WIN.blit(title_label,(WIDTH / 2 - title_label.get_width() / 2, 10))
        WIN.blit(back_label,(WIDTH / 2 - back_label.get_width() / 2, 80))

        #Blit the cheat code text
        WIN.blit(no_cooldown_label, (WIDTH / 2 - no_cooldown_label.get_width() / 2, HEIGHT / 3))
        WIN.blit(endless_lives_label, (WIDTH / 2 - no_cooldown_label.get_width() / 2, HEIGHT / 3 + 20))
        WIN.blit(reset_label, (WIDTH / 2 - reset_label.get_width() / 2, HEIGHT - 50))
        

def main(cheat):
    run = True
    FPS = 60 #60 frames per second
    
    #Display scores
    level = 0
    lives = 5 + cheat.cheat_lives

    #fonts
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    #enemy variables
    enemies = []
    wave_length = 5
    enemy_velocity = 1

    #Player variables
    player_heart_collected = False
    player_velocity = 5
    laser_velocity = 5  
    player = Player(150, 325)

    #heart object for increasing the player's health
    heart_list = []

    #Variables for the lost functionality
    lost = False
    lost_count = 0
    
    clock = pygame.time.Clock()
    def redraw_window():
        """Draws objects and blits text on the window"""

        WIN.blit(BG,(0,0))
        
        lives_label = main_font.render("Lives: {}".format(lives), 1, (255,255,255))
        level_label = main_font.render("Level: {}".format(level), 1, (255,255,255))

        #Draw text
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)

        if len(heart_list) == 1:
            for heart in heart_list:
                heart.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2))

        player.draw(WIN)
        pygame.display.update()
    
    while run:
        """The game loop has all the game's functionality"""
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3: #waits 3 seconds and then quits the game
                run = False
            else:
                continue

        if len(enemies) == 0: #The user has beaten the level
            level += 1
            wave_length += 5 #add 5 enemies to the next wave
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"])) #Span location of the enemies
                enemies.append(enemy)

        #Heart spawner
        if len(heart_list) == 0:
            if level % 2 == 0: #Change 2 to 5 for extreme difficulty 
                if player_heart_collected:
                    pass
                else:
                    heart = Heart(random.randrange(10, WIDTH - 10), random.randrange(30, HEIGHT - 30)) 
                    heart_list.append(heart)
            else:
                player_heart_collected = False
            
        #Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        #Key handler
        keys = pygame.key.get_pressed() #Gets a dictionary of all of the keys on the keyboard
        #Moves the player and sets boundaries for the player
        if keys[pygame.K_a] and player.x - player_velocity > 0: #Move left
            player.x -= player_velocity 
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH: #Move right
            player.x += player_velocity 
        if keys[pygame.K_w] and player.y - player_velocity > 0: #Move up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + player.healthbar_size + 5 < HEIGHT: #Move right
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_b]:
            main_menu(cheat)
        if keys[pygame.K_ESCAPE]:
            quit()

        #enemies functionality
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player) #laser's velocity is positive (moves downwards)

            if enemy.y + enemy.get_height() > HEIGHT: #When the enemy ship has hit the ground
                lives -= 1
                enemies.remove(enemy)
            
            if collide(enemy, player): #When the enemy and the player has collided 
                player.health -= 10
                enemies.remove(enemy)

            if random.randrange(0, 2*FPS) == 1: #probability of 1 shot every 2 seconds 
                enemy.shoot()

        #heart functionality
        for heart in heart_list[:]:
            if collide(heart, player):
                player.health += 30
                if player.health > 100:
                    player.health = 100
                heart_list.remove(heart)
                player_heart_collected = True

        player.move_lasers(-laser_velocity, enemies) #laser's velocity is negative (moves upwards)


def options(cheat):
    """This is the cheat menu. All the windows take the cheat 
    object as an attribute so the cheat window saves its data"""

    run = True
    while run:
        WIN.blit(BG, (0,0))

        cheat.display_cheet_menu() #Cheat menu object
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            main_menu(cheat)
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_1]:
            Player.COOLDOWN = 8 
            cheat.activation_fastshot = "Activated"
        if keys[pygame.K_2]:
            cheat.cheat_lives = 9999999994
            cheat.activation_endlesslife = "Activated"
        if keys[pygame.K_r]:
            Player.COOLDOWN = 30 #default cooldown speed
            cheat.cheat_lives = 0
            cheat.activation_fastshot = "Deactivated"
            cheat.activation_endlesslife = "Deactivated"
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pygame.display.update()

def main_menu(cheat):
    click = False
    main_menu_font = pygame.font.SysFont("comicsans", 70)

    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = main_menu_font.render("Main menu", 1, (255,255,255))
        play_label = main_menu_font.render("Play", 1, (255,255,255))
        option_label = main_menu_font.render("Options", 1, (255,255,255))
        
        #mouse event handler
        mx, my = pygame.mouse.get_pos()

        #Menu buttons
        button_width = 250
        button_height = 100
        play_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 3 - button_height / 2 + 20, button_width, button_height)
        option_button = pygame.Rect(WIDTH / 2 - button_width / 2 , HEIGHT / 3 + button_height / 2 + 60, button_width, button_height)

        #Draw the buttons and rect color for mouseover
        rect_color = (29,41,81)
        pygame.draw.rect(WIN, rect_color, play_button)
        pygame.draw.rect(WIN, rect_color, option_button)

        #Blit the title, play and option text
        WIN.blit(title_label,(WIDTH / 2 - title_label.get_width() / 2, 10))
        WIN.blit(play_label, (WIDTH / 2 - play_label.get_width() / 2, HEIGHT / 3 + button_height / 2 - 50))
        WIN.blit(option_label, (WIDTH / 2 - option_label.get_width() / 2, HEIGHT / 3 + button_height / 2 + 85))

        if play_button.collidepoint((mx, my)):
            if click:
                main(cheat)
        if option_button.collidepoint((mx, my)):
            if click:
                options(cheat)

        click = False
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            quit()
            
    quit()

main_menu(Cheats())