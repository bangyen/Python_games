"""Enemy sprites are from https://szadiart.itch.io/animated-character-pack?download"""
"""Main character is from https://jesse-m.itch.io/jungle-pack"""

import pygame
import random
import os
from time import sleep

from game_settings import *
from sprites import *

class Game():
    def __init__(self):
        self.running = True
        self.playing = True
        self.dead = False
        self.play_dead_sound = True
        self.__dirname = os.path.dirname(__file__)
        self.__sound_dir = os.path.join(self.__dirname, "sounds")
        self.spritesheet_dir = os.path.join(self.__dirname, "spritesheet")
        self.game_over_text = ""
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.lavas = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group() 


        self._load_data()

    def _load_data(self):
        self.main_sprite_sheet = SpritesheetParser(os.path.join(self.spritesheet_dir, "spritesheet.png"))
        self.traps_sprite_sheet = SpritesheetParser(os.path.join(self.spritesheet_dir, "traps_rip_joe_spritesheet.png"))

        #load sounds 
        self.scream_sound = pygame.mixer.Sound(os.path.join(self.__sound_dir, "man_scream.wav"))
        self.burning_sound = pygame.mixer.Sound(os.path.join(self.__sound_dir, "burning.wav"))
        self.ohh_sound = pygame.mixer.Sound(os.path.join(self.__sound_dir, "classic_hurt.wav"))

    def _play_sound(self, wav_file):
        if isinstance(wav_file, list):
            if self.play_dead_sound:
                wav_file[0].play()
                sleep(0.2) #from the time module
                wav_file[1].play()
                self.play_dead_sound = False
        else:
            if self.play_dead_sound:
                wav_file.play()
                self.play_dead_sound = False
        
    def _draw_text(self, x, y, text, font_size, color):
        font = pygame.font.SysFont(FONT, font_size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        WIN.blit(text_surface, text_rect)

    def _events(self):
        """Event handlers"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_SPACE:
                    self.main_player.jump()
            if event.type == pygame.KEYUP:
                #Main character short jump
                pass
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #event.button == 1 is the leftmousebutton
                mouse_pos = pygame.mouse.get_pos()
                if self.play_again_btn.collidepoint(mouse_pos):
                    main()
                
    def _update(self):
        self.all_sprites.update()
        
        #Collision with the platform and stop the main_player if he hits the top of the plaform
        hits_platform = pygame.sprite.spritecollide(self.main_player, self.platforms, False)
        if self.main_player.velocity.y > 0: #going down due to gravity
            if hits_platform:
                if self.main_player.position.y < hits_platform[0].rect.bottom:
                    self.main_player.position.y = hits_platform[0].rect.top
                    self.main_player.velocity.y = 0 # stop the main character
                    self.main_player.jumping = False


        #Game over scenarios
        if self.main_player.position.y - self.main_player.get_height() > HEIGHT:
            self.main_player.kill()
            self._play_sound(self.scream_sound)
            self.dead = True
            self.game_over_text = "fell"
            self.game_over_screen()

        lava_hits = pygame.sprite.spritecollide(self.main_player, self.lavas, False, pygame.sprite.collide_mask)
        if lava_hits:
            #self.burning_sound.play() if self.play_dead_sound else None
            self._play_sound([self.ohh_sound, self.burning_sound])
            self.dead = True
            self.game_over_text = "was burned to death"
            self.game_over_screen()
      
           
    def _draw(self):
        WIN.fill(SKYBLUE)
        self.all_sprites.draw(WIN)
        #Display score and coins later

        if self.dead:
            button_width = 200
            button_height = 70
            self.play_again_btn = pygame.draw.rect(WIN, BUTTON_COLOR, (WIDTH / 2 - button_width / 2, HEIGHT / 2 - 20, button_width, button_height))

            self._draw_text(WIDTH / 2, 140, "Game Over!", 40, WHITE)
            self._draw_text(WIDTH / 2, 170, "Joe {}!".format(self.game_over_text), 40, WHITE)
            self._draw_text(WIDTH / 2, HEIGHT / 2, "Play Again!", 40, WHITE)

        pygame.display.flip()

    def new_game(self):
        self.main_player = MainCharacter(self)

        #Initial platforms for the main character
        grass_platform = Platform(self.main_player.position.x, self.main_player.position.y + 8, self)
        Platform(self.main_player.position.x - grass_platform.get_size(), self.main_player.position.y + 8, self)
        
        for i in range(20):
            if 9 <= i <= 11:
                Lava(self.main_player.position.x + (grass_platform.get_size() * i), self.main_player.position.y + 2, self)
            else:
                Platform(self.main_player.position.x + (grass_platform.get_size() * i), self.main_player.position.y + 8, self)
        

    def run(self):
        """Game loop"""

        while self.playing:
            CLOCK.tick(FPS)
            self._events()
            self._update()
            self._draw()

    def game_over_screen(self):
        if self.dead:
            GraveStone(self.main_player.position.x - 100, self.main_player.position.y - 150, self)
            self.main_player.kill()



def main():
    obsticle_game = Game()

    while obsticle_game.running:
        obsticle_game.new_game()
        obsticle_game.run()

main()
        

