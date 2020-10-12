import numpy as np
from typing import List, Optional

class Game:
    def __init__(self, num_humans: int, game_size: int, win_length: int, 
                 first_player: str, sec_player: str,
                 level: Optional[int]=None):
        self.num_humans = num_humans
        self.game_size = game_size
        self.win_length = win_length
        self.first_player = first_player
        self.sec_player = sec_player 
        
        self.level = level # will be 1 or 2 only if computer is playing, otherwise None
        
        self.game_board = np.zeros((self.game_size, self.game_size))
        
        self.turn = 1 # counter for turn, see self.increment_turn() 
        self.turn_to_name = {
            1 : first_player,
            2 : sec_player 
        } # keep track of player name and order of player, see self.increment_turn() 
        
        self.state = 0 # 0 = game is running, 1 = player 1 wins, 2 = player 2 wins, 3 = tie, 4 = quit 
        self.state_full = 'Game is running!'
    
    def update_state(self, new_state: int):
        ''' Also see: self.check_victory() 
        '''
        self.state = new_state 
        
        if self.state == 1:
            self.state_full = f'{first_player} has won!'
        elif self.state == 2:
            self.state_full = f'{sec_player} has won!'
        elif self.state == 3:
            self.state_full = "It's a tie!"
        else:
            raise ValueError('Error! self.state is not 1, 2, or 3, and yet the game is still running... Please debug!')
        
    def increment_turn(self):
        ''' Alternates value of self.turn between 1 and 2 every time this is run. 
        Run once at the end of every turn, from main().
        '''
        self.turn %= 2 
        self.turn += 1
        
        print(f"It's {self.turn_to_name[self.turn]}'s turn'")
        
    def apply_move(self, row: int, col: int, rot: int):
        ''' To implement!!!  
        
        This function's role is to apply a player’s move to the game_board. The parameters are:
        game_board: the current game board
        turn: 1: player 1’s turn to play; 2: player 2’s turn to play
        row: the row index to place marble
        col: the col index to place marble
        rot:
        1: rotate the first quadrant clockwise at 90 degree
        2: rotate the first quadrant anticlockwise at 90 degree
        3: rotate the second quadrant clockwise at 90 degree
        4: rotate the second quadrant anticlockwise at 90 degree
        5: rotate the third quadrant clockwise at 90 degree
        6: rotate the third quadrant anticlockwise at 90 degree
        7: rotate the fourth quadrant clockwise at 90 degree
        8: rotate the fourth quadrant anticlockwise at 90 degree

        It will return the updated game_board after applying player’s move.

        '''
        pass 
        
    def check_victory(self):
        ''' To implement!!! 
        
        This function’s role is to check the current situation of the game after one of the players has made a move 
        to place marble and rotate quadrant. 
        
        The meaning of the parameters to this function are: 
        game_board: the current game board
        turn: 1: player 1’s turn to play; 2: player 2’s turn to play

        in other word, when it is called, game_board, turn, and rot are passed in. It will return an integer:
            0: no winning/draw situation
            1: player 1 wins
            2: player 2 wins
            3: game draw 
            
        Also see: self.update_state()             
        '''
        # new_state is the output of this class function (0, 1, 2, or 3)
        self.update_state(new_state) 
        pass
    
    def check_move(self, row: int, col: int):
        ''' To implement!!!
        
        This function's role is to check if a certain move is valid. The parameters are:
        game_board: the current game board
        row: the row index to place marble
        col: the col index to place marble

        If a place defined by row and col is occupied, the move is invalid, otherwise, it is valid.

        This function will return True for a valid move and False for an invalid move.        
        
        '''
        pass
    
    def computer_move(self):
        ''' To implement!!! 
        
        This function is to generate computer move. The parameters are:
        game_board: the current game board
        turn: 1 or 2 depending on whether computer to play first or secondly.
        level: the strategy of computer player
        1. computer play in a random placing style
        2. computer can search possible positions and analyse the game_board to find a good move to win (Option!)

        The function returns three values: row, col, and rot.        
        '''
        # check level 1 or 2, then carry out the appropriate move 
        # better idea is to set this to random or recursive search at self.__init__() 
        # i.e. define self.computer_random() & self.computer_recursive() 
        
    def display_board(self):
        print('\n') # new line, for cleaner printing
        print(self.game_board)