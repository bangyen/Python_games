#Sprite classes for our jumping game
import pygame
from random import choice 
from game_settings import *


#initialize vectors from pygame 2 for 2 dimentional vectors
vector = pygame.math.Vector2

class Spritesheet():
    """A utility class for parsing spritesheets"""
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        """This function cuts the image on the spritesheet"""

        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2 -10, height // 2 -10)) #scale the image by 1/2
        return image



class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game #access all the variables from the Game class
        self.walking = False
        self.jumping = False 
        self.current_frame = 0
        self.last_update_time = 0 #What time we did the last change, set up the animation speed (framerate)
        self._load_images()
        self.image = self.standing_frames[0] #self.image is required in the sprite class
        self.rect = self.image.get_rect() #self.rect is required in the sprite class and this puts a rectangle over the image
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(40, HEIGHT - 100) #Vector where the position of the player is
        self.velocity = vector(0, 0) #Player's velocity vector
        self.acceleration = vector(0, 0) #Player acceleration vector

    def _load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191), self.game.spritesheet.get_image(690, 406, 120, 201)]
        self.right_walking_frames = [self.game.spritesheet.get_image(678, 860, 120, 201), self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.left_walking_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_walking_frames]
        self.jump_frame = self.game.spritesheet.get_image(381, 763, 150, 181)

        joined_list_of_frames = [*self.standing_frames, *self.right_walking_frames, *self.left_walking_frames, self.jump_frame]
        for frame in joined_list_of_frames:
            frame.set_colorkey(BLACK) #remove the black background

    def _animate(self):
        #print(int(self.velocity.x))
        time_now = pygame.time.get_ticks()
        if int(self.velocity.x) != 0: #self.velocity.x is approching to 0 ex. 0.0000000123243 due to friction
            self.walking = True
        else:
            self.walking = False

        #Walking animation
        if self.walking:
            if time_now - self.last_update_time > 170:
                self.last_update_time = time_now
                self.current_frame = (self.current_frame + 1) % len(self.left_walking_frames)
                last_image_bottom = self.rect.bottom
                if self.velocity.x > 0: #Player going to the right direction
                    self.image = self.right_walking_frames[self.current_frame]
                else:
                    self.image = self.left_walking_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_image_bottom
                
        #Standing animation
        if not self.walking and not self.jumping:
            if time_now - self.last_update_time > 350: #wait 350 millisec (framerate, time changing between images)
                self.last_update_time = time_now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames) #(0+1) mod 2 = 1 and (1+1) mod 2 = 0 -> 2 sprites standing animation
                last_image_bottom = self.rect.bottom 
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_image_bottom
                
    def update(self):
        self._animate()
        self.acceleration = vector(0, PLAYER_GRAVITY) #PLAYER_GRAVITY number in game_settings.py acceleration downwards gravity

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION

        if keys[pygame.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION

        #x-position boundaries if the player goes off the screen 
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
        elif self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        
        #Friction added to the acceleration
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        self.velocity += self.acceleration
        
        #Motion physic equations
        self.pos += self.velocity + (0.5 * self.acceleration) #looks like s = v0 * t + 1/2 at^2 lineal motion

        self.rect.midbottom = self.pos #player's rectangle middlepoint is our (x,y) 

    def jump(self):
        """Let the player jump only when the player is on a platform"""
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False) #spritecollide(single_object, group_object, dokill=False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.velocity.y += PLAYER_JUMP

    def cut_jump(self):
        """Cut jump (mini jump) the player by dividing the total jump height by 4"""
        if self.jumping:
            if self.velocity.y < PLAYER_JUMP // 4: 
                self.velocity.y = PLAYER_JUMP // 4



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game #access all the variables from the Game class
        self.image = self._choose_random_platform_image()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _choose_random_platform_image(self):
        platform_image_list = [self.game.spritesheet.get_image(0, 288, 380, 94), self.game.spritesheet.get_image(213, 1662, 201, 100)]
        return choice(platform_image_list)


 




        
        


