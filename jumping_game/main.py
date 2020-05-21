"""Jumping Game: run this game where the root folder is Python_games, otherwise it wont run"""
"""This code was improvised from a pygame tutorial jumpy from the youtube channel KidsCanCode"""
"""The background, the game over and the title music is from the Super Mario World"""
"""The wav sound files are from https://www.bfxr.net/"""

import pygame
import random
import os
from game_settings import *
from sprites import *

class Game():
    def __init__(self):
        self.running = True
        self.playing = True
        self.score = 0
        self.enemy_timer = 0
        self.__dirname = os.path.dirname(__file__)
        self._load_data()
        self.font = pygame.font.match_font(FONT_NAME) #if FONT_NAME does not exist on the computer's system
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jumping Game")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates() #Spritegroup which we can specify what order the sprite (enemy) will be drawn by giving the sprite a layer
        self.platforms = pygame.sprite.Group() #Group all the platforms
        self.powerups = pygame.sprite.Group() #Group all the powerups
        self.enemies = pygame.sprite.Group() 
        self.clouds = pygame.sprite.Group() 
        
    def _reset_init(self):
        """It is a bad practice to reset the 
        init function using self.__init__()"""

        self.running = True
        self.playing = True
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates() #Group all the sprites
        self.platforms = pygame.sprite.Group() #Group all the platforms
        self.powerups = pygame.sprite.Group() #Group all the powerups
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()

    def _load_data(self):
        """Load the high score -> os.path.join(another_folder_name/folder_name, file_name) is
         the same as dir = os.path.dirname(__file__) and os.path.join(dir, file_name)"""

        #Load the high score
        with open(os.path.join(self.__dirname,"highscore.txt"), "r") as file: #open the highscore.txt file, "r" for reading only. It closes the file when the block has executed completely
            try:
                self.highscore = int(file.read())
            except:
                self.hightscore = 0

        #Load the spritesheet
        self.spritesheet = Spritesheet(os.path.join(self.__dirname + "/spritesheet_images", "spritesheet_jumper.png")) #/spritesheets_images on macOS \spritesheets_images on window 

        #load the sounds
        self.sound_dir = os.path.join(self.__dirname, "sounds")
        self.jump_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, JUMP_SOUND))
        self.jump_boost_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, JUMP_BOOST_SOUND))

        #Load the cloud images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pygame.image.load(os.path.join(self.__dirname + "/spritesheet_images", "cloud{}.png".format(i))).convert()) #3:44       

    def _draw_text(self, x, y, text, font_size, color):
        font = pygame.font.Font(self.font, font_size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.window.blit(text_surface, text_rect)

    def _wait_for_key_pressed(self):
        waiting = True

        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    self._reset_init()
                    waiting = False
                    self.playing = True

                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False

    def _events(self):
        #Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.KEYUP:
                self.player.cut_jump()

    def _update(self):
        """Game loop - update"""
        self.all_sprites.update() #update function from sprites.py
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False) #spritecollide(single_object, group_object, dokill) dokill is deleting the object from the spritegroup

        #Spawn an enemy
        now = pygame.time.get_ticks()
        if now - self.enemy_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.enemy_timer = now
            FlyingEnemy(self)

        #Enemy collision
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if enemy_hits:
            self.playing = False 

        if self.player.velocity.y > 0: #if player is going down due to gravity -number: y is going up, +number: y is going down
            if hits:
                lowest_platform = hits[0]
                for hit in hits: #Must check if hits has two or more platforms, if so than we must find the lowest platform
                    if hit.rect.bottom > lowest_platform.rect.bottom: 
                        lowest_platform = hit 

                if self.player.pos.x < lowest_platform.rect.right + 10 and self.player.pos.x > lowest_platform.rect.left - 10: #Check if the player's rect midbottom has gone off the lowest platform
                    if self.player.pos.y < lowest_platform.rect.bottom:
                        self.player.pos.y = lowest_platform.rect.top #midbottom.y = the top position of the platform's rectangle
                        self.player.velocity.y = 0 #Stop the player on the platform 
                        self.player.jumping = False

        #If player reaches the 1/4th of the screen then scroll every object animation
        if self.player.rect.top <= HEIGHT / 4: 
            #Spawn clouds 
            if random.randrange(0, 100) < 5:
                Cloud(self)

            #move the clouds
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.velocity.y / 3), 2)

            #smooth moving animation for the platforms with respect to the player's velocity 
            self.player.pos.y += max(abs(self.player.velocity.y), 2) 

            #move the platforms
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.velocity.y), 2)
                #if the platform goes off the screen remove it or kill it :)
                if plat.rect.y >= HEIGHT:
                    plat.kill() #Remove the platform to spare memory, make the game more efficient
                    self.score += 10
            
            for enemy in self.enemies:
                enemy.rect.y += max(abs(self.player.velocity.y), 2)

        #If the player collides with a powerup
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True) #dokill=True delete powerup after collision with the player
        for powerup in powerup_hits:
            if powerup.type == "boost":
                self.jump_boost_sound.play()
                self.player.velocity.y -= BOOST_POWER_JUMP
                self.player.jumping = False

        #If the player dies
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.velocity.y, 10)
                if sprite.rect.bottom < 0: #if the sprite goes off the top of the screen
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False


        #Spawn new platforms to keep the same average number of platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(random.randrange(0, WIDTH - width), random.randrange(-75, -30), self)
                 
    def _draw(self):
        self.window.fill(BGCOLOR)
        self.all_sprites.draw(self.window)
        self._draw_text(WIDTH / 2, 15, str(self.score), 25, WHITE)
        pygame.display.flip()

    def new_game(self):
        self.player = Player(self) #pass the Game object into the Player object

        for plat in PLATFORM_COORDINATES_LIST:
            Platform(*plat, self) #*plat instead of typing plat[0],plat[1], self is the Game object
            
        pygame.mixer.music.load(os.path.join(self.sound_dir, BACKGROUND_MUSIC))
        for _ in range(6):
            c = Cloud(self)
            c.rect.y += 500
    
    def run(self):
        """This is the game loop"""

        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()
        
        pygame.mixer.music.fadeout(500) #fade out the music in the span of a half second

    def show_start_screen(self):
        pygame.mixer.music.load(os.path.join(self.sound_dir, TITLE_MUSIC))
        pygame.mixer.music.play(loops=-1)
        self.window.fill(BGCOLOR)
        self._draw_text(WIDTH / 2, HEIGHT / 4, TITLE, 48, WHITE)
        self._draw_text(WIDTH / 2, HEIGHT / 2,"Left or right arrow keys to move, Space to jump", 22, WHITE)
        self._draw_text(WIDTH / 2, HEIGHT * 3/4, "Press any key to begin the game!", 22, WHITE)
        self._draw_text(WIDTH / 2, 15, "Hight Score: {}".format(self.highscore), 22, WHITE)
        pygame.display.flip()
        self._wait_for_key_pressed()
        pygame.mixer.music.fadeout(500)

    def show_game_over_screen(self):
        if self.running == False:
            return
  
        game_over_music = pygame.mixer.Sound(os.path.join(self.sound_dir, GAMEOVER_MUSIC))
        game_over_music.play()

        self.window.fill(BGCOLOR)
        self._draw_text(WIDTH / 2, HEIGHT / 4, "GAME OVER!", 48, WHITE)
        self._draw_text(WIDTH / 2, HEIGHT / 2,"Score: {}".format(self.score), 22, WHITE)
        self._draw_text(WIDTH / 2, HEIGHT * 3/4, "Press any key to play again!", 22, WHITE)

        if self.score > self.highscore:
            self.highscore = self.score
            self._draw_text(WIDTH / 2, HEIGHT / 2 + 40, "NEW HIGH SCORE!!!", 22, WHITE)
            with open(os.path.join("jumping_game","highscore.txt"),"w") as file:
                file.write(str(self.score))
        else:
            self._draw_text(WIDTH / 2, HEIGHT / 2 + 40, "High score: {}".format(self.highscore), 22, WHITE)

        pygame.display.flip()
        self._wait_for_key_pressed()

def main():
    jump_game = Game()
    jump_game.show_start_screen()

    while jump_game.running:
        jump_game.new_game()
        jump_game.run()
        jump_game.show_game_over_screen()

main()