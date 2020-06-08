import pygame
import random
import os
from game_settings import *

vector = pygame.math.Vector2

class SpritesheetParser():
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, height, width, scale_num, scale_up=True):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if scale_up:
            image = pygame.transform.scale(image, (int(width * scale_num), int(height * scale_num)))
        else:
            image = pygame.transform.scale(image, (width // scale_num, height // scale_num))

        return image

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = MAIN_CHAARACTER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.stand_left = False
        self.current_frame_index = 0
        self.last_update_time = 0
        self._load_images()
        self.image = self.standing_frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2) #maybe uneccecary
        self.position = vector(40, HEIGHT - 50)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def _load_images(self):
        self.standing_frames_right = [self.game.main_sprite_sheet.get_image(17, 448, 34, 19, 2), self.game.main_sprite_sheet.get_image(36, 448, 34, 19, 2)]
        self.standing_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.standing_frames_right]
        self.right_walking_frames = [self.game.main_sprite_sheet.get_image(55, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(76, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(97, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(97, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(118, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(139, 448, 33, 21, 2), 
                                     self.game.main_sprite_sheet.get_image(160, 448, 33, 21, 2)]
        self.left_walking_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_walking_frames]
        self.jumping_frames_right = [self.game.main_sprite_sheet.get_image(0, 448, 34, 17, 2), self.game.main_sprite_sheet.get_image(448, 384, 35, 20, 2)]
        self.jumping_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.jumping_frames_right]

        joined_frames_list = [*self.standing_frames_right, *self.standing_frames_left, *self.right_walking_frames, *self.left_walking_frames, *self.jumping_frames_right, *self.jumping_frames_left]
        for frame in joined_frames_list:
            frame.set_colorkey(BLACK)

    def __change_jumping_frame(self, right_image, left_image):
        if not self.stand_left:
            self.image = right_image
        else:
            self.image = left_image

    def _animate(self):
        time_now = pygame.time.get_ticks()

        if int(self.velocity.x) != 0:
            self.walking = True
        else:
            self.walking = False

        #Standing animation
        if not self.walking and not self.jumping: #nearly the same code @@, put in a function later
            if time_now - self.last_update_time > 320:
                self.last_update_time = time_now
                self.current_frame_index = (self.current_frame_index + 1) % len(self.standing_frames_right)
                last_image_bottom = self.rect.bottom
                if self.stand_left:
                    self.image = self.standing_frames_left[self.current_frame_index]
                else:
                    self.image = self.standing_frames_right[self.current_frame_index]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_image_bottom

        if self.walking: #nearly the same code @@
            if time_now - self.last_update_time > 90:
                self.last_update_time = time_now
                self.current_frame_index = (self.current_frame_index + 1) % len(self.left_walking_frames)
                last_image_bottom = self.rect.bottom
                if self.velocity.x > 0: #Player going to the right direction
                    self.image = self.right_walking_frames[self.current_frame_index]
                else:
                    self.image = self.left_walking_frames[self.current_frame_index]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_image_bottom

        if int(self.velocity.y) < 0:
            self.__change_jumping_frame(self.jumping_frames_right[0], self.jumping_frames_left[0])
        elif int(self.velocity.y) > 0:
            self.__change_jumping_frame(self.jumping_frames_right[1], self.jumping_frames_left[1])
            

    def update(self):
        self._animate()
        # print(self.velocity.x, self.velocity.y)

        self.acceleration = vector(0, GRAVITY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -ACCELERATION
            self.stand_left = True
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = ACCELERATION
            self.stand_left = False

        #Friction phisics equations
        self.acceleration.x += self.velocity.x * FRICTION
        self.velocity += self.acceleration
        #Motion phisics equation
        self.position += self.velocity + (0.5 * self.acceleration)
        
        self.rect.midbottom = self.position

        
    def jump(self):
        self.rect.x += 10
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 10
        if hits and not self.jumping:
            self.jumping = True
            self.velocity.y += PLAYER_JUMP

    def cut_jump(self):
        pass

    def get_height(self):
        return self.image.get_height()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, game, grass=True):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        super().__init__(self.groups)
        self.game = game
        if grass:
            self.image = self.game.main_sprite_sheet.get_image(128, 0, 128, 128, 3, False)
        else:
            self.image = self.game.main_sprite_sheet.get_image(0, 0, 128, 128, 3, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_width(self):
        return self.image.get_width()

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.lavas
        super().__init__(self.groups)
        self.game = game
        self._load_images()
        self.last_update_time = 0
        self.current_frame_index = 0
        self.image = self.lava_bubbles_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def _load_images(self):
        self.lava_bubbles_images = [self.game.main_sprite_sheet.get_image(181, 448, 32, 32, 1.5),
                                    self.game.main_sprite_sheet.get_image(213, 448, 32, 32, 1.5),
                                    self.game.main_sprite_sheet.get_image(245, 448, 32, 32, 1.5)]

        for lava_frame in self.lava_bubbles_images:
            lava_frame.set_colorkey(BLACK)

    def _animate(self):
        time_now = pygame.time.get_ticks()

        if time_now - self.last_update_time > 100:
            self.last_update_time = time_now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.lava_bubbles_images)
            self.image = self.lava_bubbles_images[self.current_frame_index]

    def update(self):
        self._animate()

class GraveStone(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = MAIN_CHAARACTER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(game.spritesheet_dir, "rip_joe.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y









