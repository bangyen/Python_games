import pygame
import os
import math
from random import choice, randrange
from game_settings import *

vector = pygame.math.Vector2

class Grass(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = 1
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.game.dirname, "sprite_img/base.png")), (WIDTH, 100)) #/ on mac \ on windows
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 100

class Bird(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = BIRD_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.flapping = False
        self.current_frame = 0
        self.last_update_time = 0 #What time we did the last change, set up the animation speed (framerate)
        self._load_images_and_blit()
        self.image = self.bird_sprites[0] #self.image is required in the sprite class
        self.rect = self.image.get_rect() #self.rect is required in the sprite class and this puts a rectangle over the image
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(WIDTH / 2, HEIGHT / 2) #Vector where the position of the player is
        self.velocity = vector(0, 0) #Player's velocity vector
        self.acceleration = vector(BIRD_ACCELERATION, 0) #Player acceleration vector
        self.mask = pygame.mask.from_surface(self.image) #for pixel perfect collision


    def _get_img(self, x, y, sprite, width, height):
        """This function is blits the image and gets its rect"""

        image = pygame.Surface((width, height))
        image.blit(sprite, (0, 0))
        #image = pygame.transform.scale(image, (width * 2 , height * 2)) #scale the image by 1/2
        return image

    def _load_images_and_blit(self):
        self.bird_img = [os.path.join(self.game.sprite_dir, "fly_{}.png".format(i)) for i in range(1,4)]
        self.frames = [pygame.image.load(frame).convert() for frame in self.bird_img]
        self.bird_sprites = [self._get_img(0, 0, frame, frame.get_width(),frame.get_height()) for frame in self.frames]

        for bird in self.bird_sprites:
            bird.set_colorkey(BLACK)

    
    def _animate(self):
        time_now = pygame.time.get_ticks()
    
        if time_now - self.last_update_time > 170:
            self.last_update_time = time_now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            last_image_bottom = self.rect.bottom 
            self.image = self.bird_sprites[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = last_image_bottom
       

    def update(self):
        """This function executes when it is called sprite_obj.update"""
        self._animate()
        self.acceleration = vector(0, BIRD_GRAVITY)

        #move the bird foward at a constant speed
        self.acceleration.x += self.velocity.x * BIRD_AIR_RESISTANCE
        self.velocity += self.acceleration

        #Motion physic equations
        self.pos += self.velocity + (0.5 * self.acceleration) #looks like s = v0 * t + 1/2 at^2 lineal motion

        self.rect.midbottom = self.pos #player's rectangle middlepoint is our (x,y) 


    def fly_up(self):
        self.velocity.y = BIRD_FLY_UP
            
            


      

    