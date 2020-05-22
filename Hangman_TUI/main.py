"""Goal: 1) Make an usual hangman with 60.000 random words
         2) Make hangman with academic word list and when the user 
         has guessed the right word, he gets the definition
         put the definition in the same bucket in the hashmap"""

"""Author: Kristofer Gauti"""

import os
from random import randrange
from hash_table import *

RANDOMWORDLIST = "wordlist.txt"
DASHES = "_"

class DashLines():
    def __init__(self, filename):
        self.__dirname = os.path.dirname(__file__)
        self.file = open(os.path.join(self.__dirname, filename), "r")
        self.word_to_guess = self._choose_word()
        self.dashes = [DASHES for x in range(len(self.word_to_guess))]
        
    def __str__(self):
        string = ""

        for letter in self.dashes:
            string += str(letter) + " "

        return string[:-1]

    def __len__(self):
        return len(self.dashes)

    def _choose_word(self):
        word_list = [word.strip() for word in self.file]
        index = randrange(0, len(word_list))
        self.word = word_list[index]
        return str(self.word)

class Game():
    def __init__(self):
        self.starting_appending = False
        self.lives = 8
        self.board = DashLines(RANDOMWORDLIST)
        self.list_with_dashes = self.board.dashes
        self.word = self.board.word_to_guess
        self.guessed_letters = []
        self._load_hangman_ascii()

    def _load_hangman_ascii(self):
        self.hangman_now = ""
        self.hang_1 = "\n🟥\n🟥\n🟥\n🟥\n🟥"
        self.hang_2 = "🟥 🟥 🟥 🟥 🟥" + self.hang_1
        self.hang_3 = "🟥 🟥 🟥 🟥 🟥\n🟥       🟥\n🟥       😁\n🟥       \n🟥\n🟥\n🟥"
        self.hang_4 = "🟥 🟥 🟥 🟥 🟥\n🟥       🟥\n🟥       😂\n🟥       ||\n🟥       ||\n🟥\n🟥"
        self.hang_5 = "🟥 🟥 🟥 🟥 🟥\n🟥       🟥\n🟥       😅\n🟥       ||\\\ \n🟥       ||\n🟥\n🟥"
        self.hang_6 = "🟥 🟥 🟥 🟥 🟥\n🟥       🟥\n🟥       😰\n🟥     //||\\\ \n🟥       ||\n🟥\n🟥"
        self.hang_7 = "🟥 🟥 🟥 🟥 🟥\n🟥       🟥\n🟥       😱\n🟥     //||\\\ \n🟥       ||\n🟥         \\ \n🟥"
        self.hang_8 = "🟥 🟥 🟥 🟥 🟥\n🟥       🟥\n🟥       😵\n🟥     //||\\\ \n🟥       ||\n🟥      /  \\ \n🟥"
        
    def _print_hangman(self):
        if self.lives == 7:
            self.hangman_now = self.hang_1
            print(self.hang_1)
        elif self.lives == 6:
            self.hangman_now = self.hang_2
            print(self.hang_2)
        elif self.lives == 5:
            self.hangman_now = self.hang_3
            print(self.hang_3)
        elif self.lives == 4:
            self.hangman_now = self.hang_4
            print(self.hang_4)
        elif self.lives == 3:
            self.hangman_now = self.hang_5
            print(self.hang_5)
        elif self.lives == 2:
            self.hangman_now = self.hang_6
            print(self.hang_6)
        elif self.lives == 1:
            self.hangman_now = self.hang_7
            print(self.hang_7)
        elif self.lives == 0:
            self.hangman_now = self.hang_8
            print(self.hang_8)

    def _correct_letter(self, player_letter):
        found_letter = False
        for index, letter in enumerate(self.word):
            if letter == player_letter:
                self.list_with_dashes[index] = letter
                found_letter = True
        return found_letter

    def _duplicate_guesses(self, player_letter):
        if player_letter in self.guessed_letters or player_letter in self.list_with_dashes:
            return True

        return False

    def _check_win(self):
        if DASHES not in self.list_with_dashes:
            return 1
        if self.lives == 0:
            return 2
        return 3


    def regular_start(self):
        print("\nWelcome to Hangman")
        print("Input any number to quit the game\n")
        print(self.board)

        player_input = str(input("Guess a letter and press enter: "))
        while player_input.isalpha():
            if self._duplicate_guesses(player_input):
                print("\nYou have already guessed on that letter!")
                player_input = str(input("Guess a letter "))
            else:
                if self._correct_letter(player_input):
                    print(self.hangman_now)
                    print("\nYou guessed correctly!")
                else:
                    self.starting_appending = True
                    self.guessed_letters.append(player_input)
                    self.lives -= 1
                    self._print_hangman()
                    print("\nToo bad! You guessed incorrectly")

                print(self.board)
                if self.starting_appending:
                    print("\nGuessed incorrect letters: " + ", ".join(self.guessed_letters))
                else:
                    print("\nGuessed incorrect letters: None")

                if self._check_win() == 1:
                    print("Congratulations! You guessed the right word.")
                elif self._check_win() == 2:
                    print("Oh, better luck next time!")
                    print("The correct word was: {}".format(self.word))
                    break
                
                player_input = str(input("Guess a letter "))

    def academic_start(self):
        print("Implement later :)")

def main():
    hangman = Game()
    print("Hangman")
    for i in range(1,3):
        if i == 1: 
            var = "random"
        else:
            var = "academic"
        print("If you want to play a regular hangman with {} english words input {}".format(var, i))
    print()

    invalid_input = True
    while invalid_input:
        try:
            answer = int(input("Your input: "))
            invalid_input = False
        except ValueError:
            print("This is a string input!")
            invalid_input = True

        if answer == 1:
            hangman.regular_start()
            invalid_input = False
        elif answer == 2:
            hangman.academic_start()
            invalid_input = False
        else:
            print("Wrong input!")
            invalid_input = True
        
main()


