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
        self.sprite_dir = os.path.join(self.dirname, "sprite_img")
        self.font = pygame.font.match_font(FONT_NAME) 
        self.all_sprites = pygame.sprite.LayeredUpdates() #Group all the sprites with layers for blitting on the screen
        self.pipes = pygame.sprite.Group() #Group all the pipes

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
        self.pipes = pygame.sprite.Group() #Group all the platforms

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


        for pipe_upward_coordinate in PIPE_UPWARD_COORDINATES:
            Pipe(pipe_upward_coordinate[0], pipe_upward_coordinate[1], self, True)
        for pipe_downward_coordinate in PIPE_DOWNWARD_COORDINATES:
            Pipe(pipe_downward_coordinate[0], pipe_downward_coordinate[1], self)

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

    def _check_hit_from_pipes(self):
        hits = pygame.sprite.spritecollide(self.bird, self.pipes, False, pygame.sprite.collide_mask)
        if hits:
            print("U ded")
        else:
            for pipe in self.pipes:
                if int(self.bird.pos.x) == int(pipe.rect.x) or int(self.bird.rect.x) == int(pipe.rect.x):
                    print("collision detection started")
                    self.score += 0.5
            

    def _update(self):
        self.all_sprites.update()
      
                    
        #Move the pipes 
        for pipe in self.pipes:
            pipe.rect.x -= PIPE_MOVING_VELOCITY
            if pipe.rect.left < 0:
                pipe.kill()

        #print(self.pipes)

        while len(self.pipes) < 6:
            x_space_between = WIDTH + SPACE_BETWEEN_PIPES
            new_coordinates_list = [ #fix the gap between pipe 3
                                    (x_space_between, SKY_CONSTANT, x_space_between, GROUND_CONSTANT + 230), #3,5cm op
                                    (x_space_between, SKY_CONSTANT - 240, x_space_between, GROUND_CONSTANT), #3,5cm op
                                    (x_space_between, SKY_CONSTANT - 130, x_space_between, GROUND_CONSTANT + 100), 
                                    (x_space_between, SKY_CONSTANT - 50, x_space_between, GROUND_CONSTANT + 190),
                                    (x_space_between, SKY_CONSTANT, x_space_between, GROUND_CONSTANT + 240)
                                   ]
            spawn_new_coordinates = random.choice(new_coordinates_list)
            Pipe(spawn_new_coordinates[0], spawn_new_coordinates[1], self, True)
            Pipe(spawn_new_coordinates[2], spawn_new_coordinates[3], self )

        self._check_hit_from_pipes()

    def _draw(self):
        #self.window.fill(BGCOLOR)
        self.window.blit(self.background, (0,0))
        self.all_sprites.draw(self.window)
        self._draw_text(WIDTH / 2, 15, str(int(self.score)), 70, WHITE)
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