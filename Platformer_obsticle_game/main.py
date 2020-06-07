"""Enemy sprites are from https://szadiart.itch.io/animated-character-pack?download"""
"""Main character is from https://jesse-m.itch.io/jungle-pack"""

import pygame
import random
import os

from game_settings import *
from sprites import *

class Game():
    def __init__(self):
        self.running = True
        self.playing = True
        self.__dirname = os.path.dirname(__file__)
        self.__spritesheet_dir = os.path.join(self.__dirname, "spritesheet")
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()


        self._load_data()

    def _load_data(self):
        self.main_sprite_sheet = SpritesheetParser(os.path.join(self.__spritesheet_dir, "spritesheet.png"))

    def _draw_text_(self, x, y, text, font_size, color):
        font = pygame.font.Font(FONT, font_size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        WIN.blit(text_surface, text_rect)

    def _events(self):
        """Event handlers"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.main_player.jump()
            if event.type == pygame.KEYUP:
                #Main character short jump
                pass
                

    def _update(self):
        self.all_sprites.update()
        hits_platform = pygame.sprite.spritecollide(self.main_player, self.platforms, False)

        if self.main_player.velocity.y > 0: #going down due to gravity
            if hits_platform:
                self.main_player.position.y = hits_platform[0].rect.top
                self.main_player.velocity.y = 0 # stop the main character
                self.main_player.jumping = False




    def _draw(self):
        WIN.fill(SKYBLUE)
        self.all_sprites.draw(WIN)
        #Display score and coins
        pygame.display.flip()

    def new_game(self):
        self.main_player = MainCharacter(self)

        #Initial platform for the main character
        Platform(self.main_player.position.x - 20, self.main_player.position.y + 2, self)

    def run(self):
        """Game loop"""

        while self.playing:
            CLOCK.tick(FPS)
            self._events()
            self._update()
            self._draw()

    def game_over_screen(self):
        pass

def main():
    obsticle_game = Game()

    while obsticle_game.running:
        obsticle_game.new_game()
        obsticle_game.run()
        obsticle_game.game_over_screen()

main()
        

