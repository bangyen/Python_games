"""Flappy Bird remake"""
"""Author Kristofer Gauti"""
"""The sprites are from a git repo: https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites"""

import pygame
import os
import random 
from sprites import *
from game_settings import *

class Game():
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.dirname = os.path.dirname(__file__)
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(os.path.join(self.dirname, "sprite_img"),"background_night.png")),(WIDTH, HEIGHT))
        self.running = True
        self.playing = True
        self.score = 0
        self.font = pygame.font.match_font(FONT_NAME) 
        self.all_sprites = pygame.sprite.LayeredUpdates() #Group all the sprites with layers for blitting on the screen
        self.pipes = pygame.sprite.Group() #Group all the pipes
        self.sprite_dir = os.path.join(self.dirname, "sprite_img")

    def _load_data(self):
        """Load the high score -> os.path.join(another_folder_name/folder_name, file_name) is
            the same as dir = os.path.dirname(__file__) and os.path.join(dir, file_name)"""

        #Load the high score
        with open(os.path.join(self.dirname,"highscore.txt"), "r") as file: #open the highscore.txt file, "r" for reading only. It closes the file when the block has executed completely
            try:
                self.highscore = int(file.read())
            except:
                self.hightscore = 0

    def _draw_text(self, x, y, text, font_size, color):
        font = pygame.font.Font(self.font, font_size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.window.blit(text_surface, text_rect)

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

    def new_game(self):
        """This function runs if self.running = True"""
        self.bird = Bird(self)
        self.grass = Grass(self)

    def run(self):
        """Game loop"""
        
        while self.playing:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.fly_up()
                if event.key == pygame.K_ESCAPE:
                    quit()

    def _update(self):
        self.all_sprites.update()



    def _draw(self):
        #self.window.fill(BGCOLOR)
        self.window.blit(self.background, (0,0))
        self.all_sprites.draw(self.window)
        self._draw_text(WIDTH / 2, 15, str(self.score), 70, WHITE)
        pygame.display.flip() 

   
    def show_start_screen(self):
        self.window.fill(BGCOLOR)
        self._draw_text(WIDTH / 2, HEIGHT / 4, TITLE, 40, YELLOW)
        self._draw_text(WIDTH / 2, HEIGHT * 3/4, "Press any key to start", 30, WHITE)
        pygame.display.flip()
        self._wait_for_key_pressed()

    def show_game_over_screen(self):
        pass


def main():
    flappy = Game()

    flappy.show_start_screen()
    while flappy.running:
        flappy.new_game()
        flappy.run()
        flappy.show_game_over_screen()


main()