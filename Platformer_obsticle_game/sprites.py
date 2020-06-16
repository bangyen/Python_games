import pygame
import random
import os
from time import sleep
from game_settings import *

vector = pygame.math.Vector2

class SpritesheetParser():
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, height, width, scale_num, scale_up=True):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if scale_up:
            image = pygame.transform.scale(image, (int(width * scale_num), int(height * scale_num)))
        else:
            image = pygame.transform.scale(image, (width // scale_num, height // scale_num))
        image.set_colorkey(BLACK)

        return image

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
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
        self.position = vector(x, y)
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

    def get_size(self, width=True, height=False):
        if width:
            return self.image.get_width()
        if height:
            return self.image.get_height()

class GraveStone(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = MAIN_CHAARACTER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = game.traps_sprite_sheet.get_image(388, 3458, 100, 100, 2)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class FireBall(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = FIREBALL_LAYER
        self.groups = game.all_sprites, game.fireballs
        super().__init__(self.groups)
        self.game = game
        self.go_up = True
        self.random_time = random.choice([3000, 4000, 5000, 6000])
        self.last_update_time = 0
        self.last_update_time_lava_ball = 0
        self.current_frame_index = 0
        self._load_images()
        self.image = self.fireball_images_go_up[0]
        self.rect = self.image.get_rect()
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def _load_images(self):
        images_list = [self.game.traps_sprite_sheet.get_image(260, 1970, 124, 220, 3, False),
                       self.game.traps_sprite_sheet.get_image(260, 2330, 124, 220, 3, False), 
                       self.game.traps_sprite_sheet.get_image(260, 2206, 124, 220, 3, False),
                       self.game.traps_sprite_sheet.get_image(260, 1846, 124, 220, 3, False),
                       self.game.traps_sprite_sheet.get_image(260, 2566, 124, 220, 3, False)]

        self.fireball_images_go_up = [pygame.transform.rotate(frame, 270) for frame in images_list]
        self.fireball_images_go_down = [pygame.transform.rotate(frame, 90) for frame in images_list]

    def _animate(self):
        time_now = pygame.time.get_ticks()

        if time_now - self.last_update_time > 100:
            self.last_update_time = time_now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.fireball_images_go_up)
            if self.velocity.y < 0:
                self.image = self.fireball_images_go_up[self.current_frame_index]
            elif self.velocity.y > 0:
                self.image = self.fireball_images_go_down[self.current_frame_index]
        
    def update(self):
        self._animate()
        time_now = pygame.time.get_ticks()

        #calculate the upwards and downwards motion with respect to gravity and friction
        self.acceleration = vector(0, GRAVITY)
        self.acceleration.y += self.velocity.y * LAVA_BALL_FRICTION
        self.velocity += self.acceleration
        
        self.position += self.velocity + (0.5 * self.acceleration)
        self.rect.midtop = self.position #midtop is a tuple (x, y). Note: self.rect does not take a tuple with floats
        
        if self.go_up:
            self.velocity.y -= 45
            self.go_up = False

        #check if the lavaball goes into the lavapool, if so remove the lavaball sprite
        for lava in self.game.lavas:
            if lava.rect.y < self.position.y:
                self.position.y = lava.rect.centery
                if time_now - self.last_update_time_lava_ball > self.random_time: #let the fireball wait in the lava for 3, 4, 5 or 6 secs before going upwards again
                    self.last_update_time_lava_ball = time_now
                    self.velocity.y -= 18
                    self.go_up = True

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, game, fireball=False):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.lavas
        super().__init__(self.groups)
        self.game = game
        self.spawn_fireball = fireball
        self._load_images()
        self.last_update_time = 0
        self.current_frame_index = 0
        self.image = self.lava_bubbles_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def _load_images(self):
        self.lava_bubbles_images = [self.game.main_sprite_sheet.get_image(181, 448, 32, 32, 1.5),
                                    self.game.main_sprite_sheet.get_image(213, 448, 32, 32, 1.5),
                                    self.game.main_sprite_sheet.get_image(245, 448, 32, 32, 1.5)]

    def _animate(self):
        time_now = pygame.time.get_ticks()

        if time_now - self.last_update_time > 250:
            self.last_update_time = time_now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.lava_bubbles_images)
            self.image = self.lava_bubbles_images[self.current_frame_index]

    def update(self):
        self._animate()
        if self.spawn_fireball:
            FireBall(self.rect.x, self.rect.y - self.get_height() - 20, self.game)
            self.spawn_fireball = False

    def get_height(self):
        return self.image.get_height()
        
class SingleFrameSpriteTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, game, animation=True, spike=True, stone=False, axe=False):
        self._layer = TRAP_LAYER
        self.groups = game.all_sprites, game.traps
        super().__init__(self.groups)
        self.last_update_time = 0
        self.spike_update_time_2 = 0
        self.update_frame_index = 0
        self.game = game
        self.animation = animation
        self.spike = spike
        self.stone = stone
        self.axe = axe
        if self.spike:
            self.spike_go_up = True
            self.spike_go_down = False 
            self.image = game.traps_sprite_sheet.get_image(260, 1486, 160, 164, 4, False)
            #self.image.set_colorkey(BLACK)

        if self.stone or self.axe:
            self.axe_down = True
            the_image = game.traps_sprite_sheet.get_image(0, 0, 394, 394, 5, False) if self.stone else game.traps_sprite_sheet.get_image(0, 394, 372, 248, 5, False)
            #the_image.set_colorkey(BLACK)
            self.stop_axe_image_list = [pygame.transform.rotate(the_image, angle) for angle in range(300, 360, 15)] #320
            self.random_num = random.randint(0, len(self.stop_axe_image_list) - 1)
            self.image_rotation_list = [pygame.transform.rotate(the_image, angle) for angle in range(0, 361, 90)]
            self.image = self.image_rotation_list[0]

        self.rect = self.image.get_rect()
        self.top = self.rect.top
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.starting_x_position = int(x)
        self.starting_y_position = int(y)

    def _animate(self):
        time_now = pygame.time.get_ticks()
        time_now_2 = pygame.time.get_ticks()

        if self.spike:
            #Spawn a platform underneath the spike
            Platform(self.starting_x_position, self.starting_y_position, self.game) #grass platform

            #Make the spikes go up and down 300, 200, 400, 100 ms per frame 
            if time_now - self.last_update_time > random.choice([300, 200, 400, 100]):
                self.last_update_time = time_now
                if self.spike_go_up:
                    self.rect.y -= 5
                if self.spike_go_down:
                    self.rect.y += 5
                if self.rect.y <= self.starting_y_position - SPIKE_HEIGHT:
                    self.spike_go_up = False
                    self.spike_go_down = True
                elif self.rect.y >= self.starting_y_position + 1: #when the spikes go behind the platform, hide the spikes behind the platform in 6 sec
                    self.rect.y -= 5
                    if time_now_2 - self.spike_update_time_2 > 6000: #6 sec
                        self.spike_update_time_2 = time_now_2
                        self.spike_go_up = True
                        self.spike_go_down = False
   
        if self.stone or self.axe:
            #Rotate the stone or axe image 90 degrees every 150 ms
            millisecs = 150 if self.stone else 70
            if time_now - self.last_update_time > millisecs:
                self.last_update_time = time_now
                self.update_frame_index = (self.update_frame_index + 1) % len(self.image_rotation_list)
                self.image = self.image_rotation_list[self.update_frame_index]

            self.rect.x -= 2

    def update(self):
        #check platform collsion
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        if self.animation:
            self._animate()
            
        if self.spike and not self.animation:
            #Display the platform beneath the spike
            Platform(self.starting_x_position, self.starting_y_position + SPIKE_HEIGHT, self.game) #grass platform change x, y

        if self.stone:
            self.rect.y += 1
            if hits:
                self.rect.y -= 1 #stop the ball's y position

            if self.rect.x + 100 <= 0:
                self.kill()
            
        if self.axe:
            self.rect.y += 2
            
            if hits:
                self.image = self.stop_axe_image_list[self.random_num]
                self.rect.x += 2
                self.rect.y -= 2


            
        
                
            

        











