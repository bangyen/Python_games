import pygame
import os
import math
from random import choice, randrange
from game_settings import *

vector = pygame.math.Vector2

class Grass(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = GRASS_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.game.dirname, "sprite_img/base.png")), (WIDTH, 100)) #/ on mac \ on windows
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 100

    def get_height(self):
        return self.image.get_height()

class Bird(pygame.sprite.Sprite):
    def __init__(self, game, grass):
        self._layer = BIRD_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.grass = grass
        self.current_frame = 0
        self.last_update_time = 0 #What time we did the last change, set up the animation speed (framerate)
        self.dead = False
        self.gravity = 0.8
        self._load_images_and_blit()
        self.image = self.bird_sprites[0] #self.image is required in the sprite class
        self.rotation_45 = [pygame.transform.rotate(image, 315) for image in self.bird_sprites]
        self.rotation_90 = [pygame.transform.rotate(image, 270) for image in self.bird_sprites]
        self.flying_imgs = [pygame.transform.rotate(image, 45) for image in self.bird_sprites]
        self.rect = self.image.get_rect() #self.rect is required in the sprite class and this puts a rectangle over the image
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(WIDTH / 2 - 150, HEIGHT / 2) #Vector where the position of the player is
        self.velocity = vector(0, 0) #Player's velocity vector
        self.acceleration = vector(0, 0) #Player acceleration vector
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

    def __change_frames(self, frames, img_list):
        self.current_frame = (self.current_frame + 1) % len(frames)
        last_image_bottom = self.rect.bottom 
        self.image = img_list[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.bottom = last_image_bottom

    def animate(self):
        time_now = pygame.time.get_ticks()
    
        if time_now - self.last_update_time > 170: #Do this after 170 ms interval
            self.last_update_time = time_now
            if self.velocity.y < 0:
                self.__change_frames(self.frames, self.flying_imgs) #45 degrees counter clockwise
            elif 0 <= self.velocity.y < 4:
                self.__change_frames(self.frames, self.bird_sprites) #0 degrees regular flying bird
            elif 4 <= self.velocity.y < 8:
                self.__change_frames(self.frames, self.rotation_45) #45 degrees clockwise
            else:
                self.__change_frames(self.frames, self.rotation_90) #90 degrees clockwise

    def _calculate_flying_distance(self):
        self.animate()
        self.acceleration = vector(0, self.gravity)

        self.velocity += self.acceleration

        #Motion physic equations
        self.pos += self.velocity + (0.5 * self.acceleration)   #looks like s = v0 * t + 1/2 at^2 lineal motion
        self.rect.midbottom = self.pos #player's rectangle middlepoint is our (x,y) 
    
        
    def update(self):
        """This function executes when it is called sprite_obj.update"""
        if self.dead:
            self.grass._layer = 1
            self.gravity = 11
            self.velocity = vector(0, 0)
            self.acceleration = vector(0, 0)
       
        self._calculate_flying_distance()

        #Boundaries
        if self.pos.y < 0 - self.rect.height / 2:
            self.pos.y = 40
        elif self.pos.y > HEIGHT - 100 + self.rect.height / 2:
            if self.dead:
                self.pos.y = HEIGHT - 100 + self.rect.height / 2 - 15
                self.image = self.rotation_90[0]
            else:
                self.dead = True
                self.grass._layer = 1
                self.gravity = 0
                self.velocity = vector(0, 0)
                self.acceleration = vector(0, 0)
            
    def fly_up(self):
        self.velocity.y = BIRD_FLY_UP

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, game, downwardspipe=False):
        self._layer = PIPE_LAYER
        self.groups = game.all_sprites, game.pipes
        super().__init__(self.groups)
        self.game = game
        self._load_pipe()
        self.pipe_list = [self.pipe_sprite, pygame.transform.rotate(self.pipe_sprite, 180)] #2 pipesprites 
        self.image = self.pipe_list[0] if not downwardspipe else self.pipe_list[1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def _get_img(self, x, y, sprite, width, height):
        """This function is blits the image and gets its rect"""

        image = pygame.Surface((width, height))
        image.blit(sprite, (0, 0))
        image.set_colorkey(BLACK)
        #image = pygame.transform.scale(image, (width * 2 , height * 2)) #scale the image by 1/2
        return image

    def _load_pipe(self):
        self.pipe_img = pygame.image.load(os.path.join(self.game.sprite_dir, "pipe_green.png"))
        self.pipe_sprite = self._get_img(0, 0, self.pipe_img, self.pipe_img.get_width(), self.pipe_img.get_height())

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = SCORE_BOARD_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(game.sprite_dir, "score_square.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PlayButton(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = PLAYBTN_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(game.sprite_dir, "playbtn.png")), (120, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class DeadBird(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = DEAD_BIRD_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.game.sprite_dir, "fly_dead.png")), (100, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y







            
            


      

    