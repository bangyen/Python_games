"""Flappy Bird remake"""
"""Author Kristofer Gauti"""
"""The sprites are from a git repo: https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites"""
"""The game over square is from Kenney: https://kenney.nl/assets/tappy-plane"""

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
        self.highscore = 0
        self._load_highscore_data()
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(os.path.join(self.dirname, "sprite_img"),"background_night.png")),(WIDTH, HEIGHT))
        self.running = True
        self.playing = True
        self.beet_highscore_msg = False
        self.score = 0
        self.sprite_dir = os.path.join(self.dirname, "sprite_img")
        self.font = pygame.font.match_font(FONT_NAME) 
        self.all_sprites = pygame.sprite.LayeredUpdates() #Group all the sprites with layers for blitting on the screen
        self.pipes = pygame.sprite.Group() #Group all the pipes

    def _load_highscore_data(self):
        """Load the high score -> os.path.join(another_folder_name/folder_name, file_name) is
            the same as dir = os.path.dirname(__file__) and os.path.join(dir, file_name)"""

        #Load the high score
        with open(os.path.join(self.dirname, "highscore.txt"), "r") as highscore_file: #open the highscore.txt file, "r" for reading only. It closes the file when the block has executed completely
            try:
                self.highscore = int(highscore_file.read())
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
        self.beet_highscore_msg = False
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates() #Group all the sprites
        self.pipes = pygame.sprite.Group() #Group all the platforms
        

    def new_game(self):
        """This function runs if self.running = True"""
        self.grass = Grass(self)
        self.bird = Bird(self, self.grass)

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #event button = 1 is the left mousebutton being pressed
                mouse_pos_tuple = pygame.mouse.get_pos()
                if self.playbtn.rect.collidepoint(mouse_pos_tuple):
                    self._reset_init()
                    self.new_game()
                    self.run()
                    
    def _update(self):
        self.all_sprites.update()

        #Pipes collision 
        hits = pygame.sprite.spritecollide(self.bird, self.pipes, False, pygame.sprite.collide_mask)
        if hits:
            self.bird.dead = True 
        else:
            for pipe in self.pipes:
                if int(self.bird.pos.x) == int(pipe.rect.x) or int(self.bird.rect.x) == int(pipe.rect.x):
                    self.score += 0.5
          
        #Move the pipes 
        if self.bird.dead:
            for pipe in self.pipes:
                pipe.rect.x += 0
            self.game_over_screen()
        else:
            for pipe in self.pipes:
                pipe.rect.x -= PIPE_MOVING_VELOCITY
                if pipe.rect.left < 0:
                    pipe.kill()

        #Spawn more pipes while the pipe group container < 6
        while len(self.pipes) < 6:
            x_space_between = WIDTH + SPACE_BETWEEN_PIPES
            new_coordinates_list = [ #fix the gap between pipe 3
                                    (x_space_between, SKY_CONSTANT, x_space_between, GROUND_CONSTANT + 230), #3,5cm gap between pipes
                                    (x_space_between, SKY_CONSTANT - 240, x_space_between, GROUND_CONSTANT),
                                    (x_space_between, SKY_CONSTANT - 130, x_space_between, GROUND_CONSTANT + 100), 
                                    (x_space_between, SKY_CONSTANT - 50, x_space_between, GROUND_CONSTANT + 190),
                                    (x_space_between, SKY_CONSTANT, x_space_between, GROUND_CONSTANT + 240)
                                   ]
            spawn_new_coordinates = random.choice(new_coordinates_list)
            Pipe(spawn_new_coordinates[0], spawn_new_coordinates[1], self, True)
            Pipe(spawn_new_coordinates[2], spawn_new_coordinates[3], self )


    def _draw(self):
        self.window.blit(self.background, (0, 0))
        self.all_sprites.draw(self.window)
        self._draw_text(WIDTH / 2, 15, str(int(self.score)), 70, WHITE)

        if self.bird.dead:
            if self.beet_highscore_msg:
                self._draw_text(WIDTH / 2, HEIGHT / 2 - 90, "Congratulations!", 35, BLACK)
                self._draw_text(WIDTH / 2, HEIGHT / 2 - 50, "A new highscore!", 35, BLACK)
            else:
                DeadBird(WIDTH / 2 - 45, HEIGHT / 2 - 90, self)

            self._draw_text(WIDTH / 2, HEIGHT / 2 + 20, "The highscore: {}".format(str(int(self.highscore))), 35, BLACK)
            self._draw_text(WIDTH / 2, HEIGHT / 2 + 80, "Your score: {}".format(str(int(self.score))), 35, BLACK)

        pygame.display.flip() 

    def show_start_screen(self):
        self.window.blit(self.background, (0, 0))
        self._draw_text(WIDTH / 2, HEIGHT / 4, TITLE, 40, YELLOW)
        self._draw_text(WIDTH / 2, HEIGHT * 3/4, "Press any key to start", 30, WHITE)
        pygame.display.flip()

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

    def game_over_screen(self):
        ScoreBoard(WIDTH / 2 - 131, HEIGHT / 4 + 30, self)
        self.playbtn = PlayButton(WIDTH / 2 - 57, HEIGHT * 3/4 - 20, self)
        
        #update highscore
        if self.score > self.highscore:
            self.highscore = self.score
            self.beet_highscore_msg = True
            with open(os.path.join(self.dirname, "highscore.txt"), "w") as highscore_file:
                highscore_file.write(str(int(self.score)))

def main():
    flappy = Game()

    
    flappy.show_start_screen()
    while flappy.running:
        flappy.new_game()
        flappy.run()
 
main()