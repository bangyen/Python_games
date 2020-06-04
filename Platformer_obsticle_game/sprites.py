import pygame
import random
from game_settings import *

vector = pygame.math.Vector2

class SpritesheetParser():
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, height, width, scale_num):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width * scale_num, height * scale_num))
        return image

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = MAIN_CHAARACTER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame_index = 0
        self.last_update_time = 0
        self._load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2) #maybe uneccecary
        self.position = vector(100, HEIGHT - 30)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def _load_images(self):
        self.standing_frames = [self.game.main_sprite_sheet.get_image(17, 448, 34, 19, 2), self.game.main_sprite_sheet.get_image(36, 448, 34, 19, 2)]
        self.right_walking_frames = [self.game.main_sprite_sheet.get_image(55, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(76, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(97, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(97, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(118, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(139, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(160, 448, 33, 21, 2)]
        self.left_walking_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_walking_frames]

        joined_frames_list = [*self.standing_frames, *self.right_walking_frames, *self.left_walking_frames]
        for frame in joined_frames_list:
            frame.set_colorkey(BLACK)

    def _animate(self):
        going_left = True
        time_now = pygame.time.get_ticks()

        if int(self.velocity.x) != 0:
            self.walking = True
        else:
            self.walking = False

        #Standing animation
        if not self.walking and not self.jumping:
            if time_now - self.last_update_time > 400:
                self.last_update_time = time_now
                self.current_frame_index = (self.current_frame_index + 1) % len(self.standing_frames)
                last_image_bottom = self.rect.bottom
                if going_left:
                    standing_left_sprite_list = [pygame.transform.flip(frame, True, False) for frame in self.standing_frames]
                    self.image = standing_left_sprite_list[self.current_frame_index]
                else:
                    self.image = self.standing_frames[self.current_frame_index]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_image_bottom

        if self.walking:
            if time_now - self.last_update_time > 170:
                self.last_update_time = time_now
                self.current_frame_index = (self.current_frame_index + 1) % len(self.left_walking_frames)
                last_image_bottom = self.rect.bottom
                if self.velocity.x > 0: #Player going to the right direction
                    going_left = False
                    self.image = self.right_walking_frames[self.current_frame_index]
                else:
                    going_left = True
                    self.image = self.left_walking_frames[self.current_frame_index]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_image_bottom

    def update(self):
        self._animate()

        self.acceleration = vector(0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = ACCELERATION

        #Friction phisics equations
        self.acceleration.x += self.velocity.x * FRICTION
        self.velocity += self.acceleration
        #Motion phisics equation
        self.position += self.velocity + (0.5 * self.acceleration)
        
        self.rect.midbottom = self.position

        
    def jump(self):
        pass

    def cut_jump(self):
        pass





