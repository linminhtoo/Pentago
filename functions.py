import numpy as np
import random
import math
from typing import Optional, Tuple, List
import time

from tqdm import tqdm

def find_longest(game_board: np.ndarray,
                 current_player: int,
                 row: Optional[int] = None,
                 col: Optional[int] = None,
                 neg_diag: Optional[int] = None,
                 #diag can be a number from 1 to (2*game_size - 3)
                 pos_diag: Optional[int] = None) -> int:
    #first, convert to bool --> if current_player = 1, piece = True
    board_copy = game_board.copy()
    check_piece_on_board = board_copy == current_player #returns boolean array
    game_size = check_piece_on_board.shape[0]
    
    if row != None:
        line_to_check = check_piece_on_board[row, :]
    elif col != None:
        transposed_board = np.transpose(check_piece_on_board)
        line_to_check = transposed_board[col, :]
        
    elif neg_diag != None: #diag will describe the offset from main diagonal in np.diagonal
        line_to_check = np.diagonal(check_piece_on_board, int(neg_diag-(game_size-1)))   
    
    elif pos_diag != None: 
        flipped_board = np.fliplr(check_piece_on_board) #horizontal flip of board_copy
        line_to_check = np.diagonal(flipped_board, int(-(pos_diag-(game_size-1))))
        
    else: #all none
        raise ValueError("Error! Please input a row, column, neg_diag, or pos_diag to check")
    
    check_matrix = np.diff(
                             (
                                np.concatenate(
                                    (
                                     [line_to_check[0]],
                                     line_to_check[:-1] != line_to_check[1:],
                                     [True]
                                    )
                                                   )
                                    ).nonzero()[0])[::2]

    if len(check_matrix) == 0:
        return 0
    else:
        return max(check_matrix)


def check_player_victory(game_board: np.ndarray,
                         current_player: int,
                         num_consecutive: Optional[int] = None) -> bool:
    ''' checks whether current_player satisfies victory condition 
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the current game board 
    current_player : int [1, 2]
        the player for whom to check for victory condition
    num_consecutive : Optional[int] (Default = None)
        number of consecutive. If None, defaults to game_size - 1
    
    Returns
    -------
    bool
        whether victory condition is satisfied for the current player 
    
    Also see: check_victory    
    '''
    game_size = game_board.shape[0] 
    if num_consecutive is None:
        num_consecutive = game_size - 1
     
    for row_idx in range(game_size):
        hori_count = 0
        for col_idx in range(game_size):
            if game_board[row_idx][col_idx] == current_player:
                hori_count += 1
                if hori_count >= num_consecutive:
                    return True 
            elif hori_count >= num_consecutive:
                return True

            # previous cols of same row have player's piece, but this col doesn't, and also haven't win, 
            # no point checking further, since we broke the consecutive criteria, so break the loop 
            elif hori_count > 0: 
                break

    # check vertical columns
    for col_idx in range(game_size):
        vert_count = 0
        for row_idx in range(game_size):
            if game_board[row_idx][col_idx] == current_player:
                vert_count += 1
                if vert_count >= num_consecutive:
                    return True  
            elif vert_count >= num_consecutive:
                return True 
            elif vert_count > 0:
                break

    # check positive diagonal (0-(game_size-num_consecutive), (game_size-num_consecutive +1))
    for idx in range((num_consecutive-1), (2*game_size - num_consecutive)): 
        # start range should be range(-(game_size-num_consecutive), (2*game_size-6))
        if find_longest(game_board, current_player, None, None, None, idx) >= num_consecutive:
            # if longest line in diagonal >= num_consecutive, WIN
            return True

    # check negative diagonal
    for idx in range((num_consecutive-1), (2*game_size - num_consecutive)): 
        # start range should be range(-(game_size-num_consecutive), (2*game_size-6))
        if find_longest(game_board, current_player, None, None, idx, None) >= num_consecutive:
            # if longest line in diagonal >= num_consecutive, WIN
            return True
        
    return False


def check_victory(game_board: np.ndarray,
                  current_player: int,
                  num_consecutive: Optional[int] = None) -> int:
    ''' checks for victory for either player or tie or to keep playing
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the current game board 
    current_player : int [1, 2]
        the current player who just made a move. 
        Needed to account for cases when a rotation causes both player 1 and 2 to win at the same time. 
        In this case, the player who made the move loses. 
        Example: player 1 rotates quadrant 2 clockwise, resulting in both players 1 and 2 satisfying
        victory condition simultaneously. Since player 1 made this 'mistake', we consider player 2 to win. 
    num_consecutive : Optional[int] (Default = None)
        number of consecutive. If None, defaults to game_size - 1
    
    Returns
    -------
    int 
        integer corresponding to 4 possible game states
            0: no winning/draw situation
            1: player 1 wins
            2: player 2 wins
            3: game draw 

    Also see: check_player_victory
    '''
    game_size = game_board.shape[0] 
    if num_consecutive is None:
        num_consecutive = game_size - 1

    if current_player == 1:
        other_player = 2
    else:
        other_player = 1

    if check_player_victory(game_board, current_player, num_consecutive):
        if check_player_victory(game_board, other_player, num_consecutive): # both win simultaneously
            return other_player # other_player wins, since current_player made the 'mistake'
        else:
            return current_player

    elif check_player_victory(game_board, other_player, num_consecutive):
        if check_player_victory(game_board, current_player, num_consecutive):  # both win simultaneously
            return current_player # current_player wins, since other_player made the 'mistake'
        else:
            return other_player

    else: # no one has won yet
        if np.all(game_board): # no non-zero values left on game board, it's a tie 
            return 3
        else: # game continues 
            return 0 


def split_into_quadrants(game_board: np.ndarray
                        ) -> Tuple[np.ndarray, np.ndarray,
                                  np.ndarray, np.ndarray]:
    ''' split array of size n x n into 4 equal quadrants of size n//2 x n//2 each 
    n must be even!
    
    Parameters
    ----------
    game_board : np.ndarray
        the current game board
        
    Returns
    -------
    quadrants : Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        a tuple of four elements (top_left, top_right, bottom_left, bottom_right)
        of size n//2 x n//2 each 
    '''
    n = game_board.shape[0] 
 
    return (
        game_board[:n//2, :n//2],
        game_board[:n//2, n//2:],
        game_board[n//2:, :n//2],
        game_board[n//2:, n//2:]
    )


def check_neutral_quadrants(game_board: np.ndarray) -> bool:
    ''' checks if there are any neutral quadrants on the game board. 
    Affects whether player is asked to do rotation (or if it is compulsory), 
    because if there is at least one neutral quadrant on the board, 
    rotation is optional. 
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the current game board 
    
    Returns
    -------
    bool
        whether there is at least one neutral quadrant on the game board 
    '''
    game_size = game_board.shape[0]
     
    quadrants = split_into_quadrants(game_board)    
    for quadrant in quadrants:
        if quadrant.nonzero()[0].shape[0] == 0:
            return True # found a neutral quadrant, no need to search further   
        if quadrant.nonzero()[0].shape[0] == 1:
            if quadrant.nonzero() == (1,1): # only non-zero value is the centre of the quadrant
                return True  # found a neutral quadrant, no need to search further
                
    return False # failed to find any neutral quadrants     


def rotate_quadrant(game_board: np.ndarray,
                   rot: int) -> np.ndarray:
    ''' rotates the desired quadrant using np.rot90 
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the current game board 
    rot : int
        which rotation to perform (between 1, inclusive and 8, inclusive): 
            1: rotate the first quadrant clockwise at 90 degree
            2: rotate the first quadrant anticlockwise at 90 degree
            3: rotate the second quadrant clockwise at 90 degree
            4: rotate the second quadrant anticlockwise at 90 degree
            5: rotate the third quadrant clockwise at 90 degree
            6: rotate the third quadrant anticlockwise at 90 degree
            7: rotate the fourth quadrant clockwise at 90 degree
            8: rotate the fourth quadrant anticlockwise at 90 degree
        
    Returns
    -------
    game_board : np.ndarray (dtype = int)
        the rotated game board
        
    Also see: apply_move() 
    '''
    game_board = game_board.copy() 
    # needed bcos numpy arrays are mutable and we need to keep previous state of game board in memory
    # when searching through possible game states for computer move level 2
    
    game_size = game_board.shape[0]
    
    if rot == 1:
        game_board[:game_size//2, 
                   :game_size//2] = np.rot90(game_board[:game_size//2, 
                                                        :game_size//2], 3) #rotate clockwise
    elif rot == 2:
        game_board[:game_size//2, 
                   :game_size//2] = np.rot90(game_board[:game_size//2, 
                                                        :game_size//2], 1) # rotate anti-clockwise 
    elif rot == 3:
        game_board[:game_size//2,
                   game_size//2:] = np.rot90(game_board[:game_size//2, 
                                                        game_size//2:], 3)
    elif rot == 4:
        game_board[:game_size//2,
                   game_size//2:] = np.rot90(game_board[:game_size//2, 
                                                        game_size//2:], 1)
    elif rot == 5:
        game_board[game_size//2:,
                   :game_size//2] = np.rot90(game_board[game_size//2:, 
                                                        :game_size//2], 3)
    elif rot == 6:
        game_board[game_size//2:,
                   :game_size//2] = np.rot90(game_board[game_size//2:, 
                                                        :game_size//2], 1)
    elif rot == 7:
        game_board[game_size//2:,
                   game_size//2:] = np.rot90(game_board[game_size//2:, 
                                                        game_size//2:], 3)
    elif rot == 8:
        game_board[game_size//2:,
                   game_size//2:] = np.rot90(game_board[game_size//2:, 
                                                        game_size//2:], 1)
#     print('Rotated:\n', game_board)
    return game_board    


def apply_move(game_board: np.ndarray,
               current_player: int,
               row: Optional[int] = None,
               col: Optional[int] = None,
               rot: Optional[int] = None) -> np.ndarray: 
    ''' applies player input move to game board 
    (assumes this move's validity has been checked by check_move() and check_input())
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the numpy array representing the current state of the game board. will be split into quadrants by split_board()
    current_player : int
        whose player's turn it is. Affects the piece to be placed 
        1 --> player 1's turn --> piece to place is 1 
        2 --> player 2's turn --> piece to place is 2
    row : int
        which row to place the piece (0-indexed)
    col : int
        which column to place the piece (0-indexed)
    rot : Optional[int] (Default = None)
        which rotation to perform (between 1, inclusive and 8, inclusive): 
            1: rotate the first quadrant clockwise at 90 degree
            2: rotate the first quadrant anticlockwise at 90 degree
            3: rotate the second quadrant clockwise at 90 degree
            4: rotate the second quadrant anticlockwise at 90 degree
            5: rotate the third quadrant clockwise at 90 degree
            6: rotate the third quadrant anticlockwise at 90 degree
            7: rotate the fourth quadrant clockwise at 90 degree
            8: rotate the fourth quadrant anticlockwise at 90 degree
        as rotation is optional, if player does not wish to rotate, the value of rot is None 
    
    Returns
    -------
    game_board : np.ndarray (dtype = int)
        the numpy array representing the new state of the game board after placing the piece and rotating the board 
    
    also see: check_input_row_and_col(), check_input_rot(), check_move(), rotate_quadrant() 
    '''  
    # only used for debugging. to be commented out later as these if statements slow the program down. 
#     if row is None and col is None and rot is None:
#         raise ValueError('No value provided for either (row, col) or rot. Unable to make any move!') 
    
    if row is not None and col is not None: # place piece
        game_board[row][col] = current_player

    if rot is not None:
        game_board = rotate_quadrant(game_board, rot)
 
    return game_board

def check_move(game_board: np.ndarray,
               row: int,
               col: int) -> bool:
    ''' Checks if provided move (row, col) is valid
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the numpy array representing the current state of the game board.
    row : int
        which row to place the piece (0-indexed)
    col : int
        which column to place the piece (0-indexed)
        
    Returns
    -------
    bool
        whether provided move (row, col) is valid
    '''
    if game_board[row, col] != 0: 
        return False 
    else:
        return True


def generate_random_move(game_board: np.ndarray
                        ) -> Tuple[int, int, int]:
    ''' 
    Randomly generates a valid move for computer level 1 to play
    
    Parameters
    ----------
    game_board : np.ndarray (dtype = int)
        the numpy array representing the current state of the game board.   
        
    Returns
    -------
    (row, col, rot) : Tuple[int, int, int]
        a randomly chosen move in the form of a tuple (row, col, rot) for computer to make 
        
    Also see: check_move
    '''
    game_size = game_board.shape[0]

    candidate_moves = [] # can set as class attribute, since this list is constant thruout game, no need to waste computation
    for row in range(game_size):
        for col in range(game_size):
            for rot in range(1, 9):
                candidate_moves.append((row, col, rot)) 
         
    random.shuffle(candidate_moves)
    for move in candidate_moves:
        row, col, rot = move
        if check_move(game_board, row, col): # found valid move 
            return row, col, rot 
    
    raise RuntimeError('Could not find valid move! Game board seems to be full, but game is still running. PLEASE DEBUG!')
    
