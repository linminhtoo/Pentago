import numpy as np
import random
import math
from typing import Optional, Tuple, List
import time

from tqdm import tqdm

def check_input_row_and_col(row: int, 
                            col: int, 
                            game_size: int = 6
                           ) -> Tuple[bool, 
                                      Optional[int], 
                                      Optional[int]]:
    ''' checks user input for row and col for integers of correct values

    Parameters
    ----------
    row : int
        row to place piece (1-indexed)
    col : int
        col to place piece (1-indexed)
    game_size : int (Default = 6)
        length of a side of the game board

    Returns
    -------
    (is_valid, row, col) : Tuple[bool, Optional[int], Optional[int]]
        is_valid: whether the user input is valid or not
        row: row to place piece (0-indexed), only returned if is_valid, else None
        col: col to place piece (0-indexed), only returned if is_valid, else None
    '''
    try:
        row = int(row)
        col = int(col)
    except:
        print("\nValueError! Row & column must all be integers.")
        print(f"You entered {row} for row and {col} for column.")
        return False, None, None
        
    if row < 1 or row > game_size:
        print(f"\nValueError! Row should be between 1 to {game_size}.")
        print(f"You entered {row} for row.")
        return False, None, None
    if col < 1 or col > game_size: 
        print(f"\nValueError! Column should be between 1 to {game_size}.")
        print(f"You entered {col} for column")
        return False, None, None
     
    return True, row - 1, col - 1

def check_input_rot(rot: str
                   ) -> Tuple[bool, 
                              Optional[int]]:
    ''' checks user input for rot for an integer of correct value
    
    Parameters
    ----------
    rot : int
        rotation to perform. must be between 1 and 8
    game_size : int (Default = 6)
        length of a side of the game board
    
    Returns
    -------
    (is_valid, rot) : Tuple[bool, Optional[int]]
        is_valid : whether the user input is valid or not
        rot : rotation to make, only returned if is_valid, else None
    '''
    valid_rots = set([
        '1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R'
    ])
    
    if rot in valid_rots:
        return True, rot
    else:
        print("\nValueError!")
        print(f"You entered {rot} for rot.")
        return False, None