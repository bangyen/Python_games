EMPTY = " "
QUIT = "q"

class Board():
    def __init__(self, dim=3):
        self.dim_num = dim
        self.row = [EMPTY] * self.dim_num
        self.board = [self.row[:] for _ in range(self.dim_num)]

    def __str__(self):
        print("\n")
        string = ""
        for index, spot in enumerate(self.board):
            if index == len(self.board) - 1:
                string += " | ".join(spot) + "\n"
            else:
                string += " | ".join(spot) + "\n"
                string += "---" * self.dim_num  + "\n"
                
        return string

    def _check_occupied(self, col, row):
        """Checks if a spot is taken"""
        if self.board[row - 1][col - 1] == EMPTY:
            return False
        else:
            return True

    def _out_of_range(self, col, row):
        if col > self.dim_num or row > self.dim_num:
            return True
        else:
            return False

    def switch(self, col, row, player):
        """Switch the EMPTY spot to either x or o. 
        If the spot is out of range return 0, occupied return 1
        The integers are for the switch turn function in the game_loop"""

        if self._out_of_range(col, row):
            print("The spot that you have chosen is out of range")
            return 0
        if self._check_occupied(col, row):
            print("This spot is taken!")
            return 1
        else:
            self.board[row - 1][col - 1] = player
            
class Game():
    def __init__(self):
        self.p1 = "o"
        self.p2 = "x"
        self.turn = None
        self.winner = None

    def check_win(self, board_object):
        the_winner = None
        col_list_1 = []
        col_list_2 = []
        col_list_3 = []
        diagonal_from_left = [board_object.board[0][0], board_object.board[1][1], board_object.board[2][2]]
        diagonal_from_right = [board_object.board[0][2], board_object.board[1][1], board_object.board[2][0]]
        
        for row in board_object.board:
            col_list_1.append(row[0])
            col_list_2.append(row[1])
            col_list_3.append(row[2])

            row_set = set(row)
            if len(row_set) == 1 and list(row_set)[0] == self.turn:
                the_winner = self.turn

        if len(set(col_list_1)) == 1 and col_list_1[0] == self.turn:
            the_winner = self.turn
        if len(set(col_list_2)) == 1 and col_list_2[0] == self.turn:
            the_winner = self.turn
        if len(set(col_list_3)) == 1 and col_list_3[0] == self.turn:
            the_winner = self.turn

        if len(set(diagonal_from_left)) == 1 and diagonal_from_left[0] == self.turn:
            the_winner = self.turn
        if len(set(diagonal_from_right)) == 1 and diagonal_from_right[0] == self.turn:
            the_winner = self.turn

        tie_board = col_list_1 + col_list_2 + col_list_3
        if EMPTY not in tie_board:
            the_winner = "It's a tie!"
        
        return the_winner
        
    def switch_turn(self):
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1
        return self.turn

    def whose_turn(self):
        import random 
        randnum = random.randint(0,1)
        if randnum == 0:
            self.turn = self.p1
        else:
            self.turn = self.p2
        return self.turn

    def game_loop(self, the_board, the_player):
        player_input = str(input("Input two numbers seperated with a comma (x,y): "))

        while player_input != QUIT:
            coordinate_list = player_input.split(",")
            new_board = the_board.switch(int(coordinate_list[0]),int(coordinate_list[1]), the_player)
            print(the_board)

            winner = self.check_win(the_board)
            if winner:
                if len(winner) > 1:
                    print(winner) 
                else:  
                    print("The winner is {}".format(self.turn))
                break

            if new_board == 0: #zero means that the spot was out of range
                pass
            elif new_board == 1: #one means that the spot was occupied
                pass
            else:
                the_player = self.switch_turn() #if new board returns none (no integer values), switch the player
        
            player_input = str(input("Input two numbers seperated with a comma (x,y): "))

    def start(self):
        players_turn = self.whose_turn()
        the_board = Board()
        print("Welcome to Tic Tac Toe!\n\nInstructions:")
        print("The board is like a cartasian coordinate system.\n(1,1) is the top left spot, (2,2) is the middle spot and so on.\nThe x coordinate's direction is to the right and the y coordinate's direction is down")
        print(the_board)
        print("{} starts the game".format(players_turn))
        self.game_loop(the_board, players_turn)

def main():
    tic_tac_toe = Game()
    tic_tac_toe.start()

main()