
import numpy as np
import random
import math
from typing import Optional, Tuple, List
import time

from tqdm import tqdm

from functions import *

def generate_all_moves(game_board: np.ndarray
                ) -> List[Tuple[int, int, int]]:
    
    game_size = game_board.shape[0]

    possible_moves = [] #generate all possible moves
    possible_rots = list(range(1, 9))
    possible_rots.append(None)
    for col in range(game_size):
        for row in range(game_size):
            if game_board[row][col] != 0:
                continue 
            for rot in possible_rots:
                possible_moves.append((row, col, rot))                
    
    return possible_moves

def check_utility(game_board: np.ndarray,
                  current_player : int, AI_index : int, 
                  num_consecutive : Optional[int] = None) -> int:
    ''' 
        check if both players win --> see who is current player -->
        award current player with utility points (AI as maximizingPlayer)
        if there is only one winner, give winner utility points.
        if no winner, calculate max number of conseq pieces on board and allocate
        points to each player by utility = +-(20/num_consecutive*N)
    '''
    game_size = game_board.shape[0]
    
    if num_consecutive is None:
        num_consecutive = game_size - 1
    
    if check_player_victory(game_board, 1) and check_player_victory(game_board, 2): #both players win
        if current_player == AI_index: #AI's turn
            utility = -20 #human wins
        else: # human's turn
            utility = +20 #AI wins
        return utility
    elif check_player_victory(game_board, AI_index): #one winner scenario
        utility = +20 #AI wins 
        return utility
    elif check_player_victory(game_board, AI_index%2+1):
        return -20 # human wins 
    
   # no winners yet, so allocate temporary utility to game on a scale of -inf to +inf
    utility = 0 
    longest_lines = []
    for idx in range(game_size):
        longest_lines.append(find_longest(game_board, current_player, idx, None, None, None)) # rows
        longest_lines.append(find_longest(game_board, current_player, None, idx, None, None)) # cols
    for idx in range(num_consecutive-1, (2*game_size-num_consecutive)-1):  
        longest_lines.append(find_longest(game_board, current_player, None, None, idx, None))
        longest_lines.append(find_longest(game_board, current_player, None, None, None, idx))

    N = max(longest_lines) # N is max consec pieces on board for current_player 

    if N != 0:
        if current_player != AI_index: # current_player is human 
            utility = -(20/num_consecutive*N) # from AI's POV, minimise human's utility
        else: 
            utility = +(20/num_consecutive*N) # from AI's POV, maximise AI's own utility
    return utility

def minimax(game_board : np.ndarray,
            depth : int,
            current_player : int,
            AI_index : int
            ) -> list: #currentplayer = 2
    next_player = current_player%2 + 1
   
    if np.all(game_board): # tie
        return 0    

    elif abs(check_utility(game_board, current_player, AI_index)) >= 20:
        if current_player == AI_index:
            return +20
        else: # human
            return -20
        
    elif depth == 0: # max depth  
        utility = check_utility(game_board, current_player, AI_index)
        return utility
    
    if next_player == AI_index: # AI, maximise utility
        utility = -math.inf  
        possible_moves = generate_all_moves(game_board) # generates possible moves for AI to make 
        
        for i in possible_moves: 
            rowi = i[0]
            coli = i[1]
            roti = i[2]
            new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) 
            # simulate moves by AI
            
            evaluation = minimax(new_board, depth - 1, next_player, AI_index) 
            utility = max(utility, evaluation)
        return utility
    
    else: # human, minimising player
        utility = +math.inf
        possible_moves = generate_all_moves(game_board)  # generate all moves by human
        
        for i in possible_moves:
            rowi = i[0]
            coli = i[1]
            roti = i[2]
            new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti)
            # simulates move made by human 
            
            evaluation = minimax(new_board, depth - 1, next_player, AI_index)
            utility = min(utility, evaluation)
        return utility


def get_best_move(game_board: np.ndarray,
                  current_player: int, 
                  AI_index: int, 
                  max_depth: int = 4
            ) -> Tuple[int, int, int]:
    if not np.any(game_board): # empty, AI starts first
        best_first_moves = [
            (1, 1, None),
            (1, 4, None),
            (4, 1, None),
            (4, 4, None)
        ]
        return random.choice(best_first_moves)
    
    next_player = current_player%2 + 1
    
    best_utility = -math.inf
    possible_moves = generate_all_moves(game_board) 
    random.shuffle(possible_moves)
    
    for i in tqdm(possible_moves, desc='simulating next move for AI...'):
        rowi = i[0]
        coli = i[1]
        roti = i[2]
        
        new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti)
        
        if check_utility(new_board, current_player, AI_index) >= +20: # AI has won
            return (rowi, coli, roti) # no need to minimax anything 
        
        elif roti is None: # not a valid move, since AI hasn't won, but no rotation
            continue       
                
        evaluation = minimax(new_board, max_depth - 1, current_player, AI_index)
        if evaluation >= best_utility:
            best_utility = evaluation   
            best_move = (rowi, coli, roti)
        
#     print(f'Best Utility: {best_utility}')
    return best_move

def alpha_beta_minimax(game_board : np.ndarray,
            depth : int,
            current_player : int,
            AI_index : int,
            alpha : int,
            beta : int,
            ) -> float:  
    next_player = current_player%2 + 1

    if np.all(game_board): # tie
        return 0
    
    else: # not tie, check for victory 
        terminal_utility = check_utility(game_board, current_player, AI_index)
        terminal_utility_other_player = check_utility(game_board, next_player, AI_index)
        if abs(terminal_utility) >= 20: # someone has won
            if abs(terminal_utility_other_player) >= 20: # both players win
                if current_player == AI_index:
                    return -20 # AI loses, as his move led to both players winning together
                else:
                    return +20 # human loses, as his move led to both players winning together 
            else: # only one player wins 
                if current_player == AI_index:
                    return +20
                else: # human
                    return -20

        elif depth == 0: # max depth  
            return terminal_utility 
    
    if next_player == AI_index: # maximise AI 
        maxEval = -math.inf 
        possible_moves = generate_all_moves(game_board)  # generates possible moves for AI to make
        random.shuffle(possible_moves)
        
        for i in possible_moves:
            rowi = i[0]
            coli = i[1]
            roti = i[2]
            new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) # simulates move made by other player
            
            evaluation = alpha_beta_minimax(new_board, depth - 1, next_player, AI_index, alpha, beta)
            alpha = max(alpha, evaluation)
            maxEval = max(maxEval, evaluation)
            if beta <= alpha:
                break
        return maxEval
    
    else: # human, minimising player
        minEval = +math.inf
        possible_moves = generate_all_moves(game_board)  # generates moves for human to make
        random.shuffle(possible_moves)
        
        for i in possible_moves:
            rowi = i[0]
            coli = i[1]
            roti = i[2]
            new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) # simulates move made by human
            
            evaluation = alpha_beta_minimax(new_board, depth - 1, next_player, AI_index, alpha, beta)
            beta = min(beta, evaluation)
            minEval = min(minEval, evaluation)
            if beta <= alpha:
                break
        return minEval

def alpha_beta_get_best_move(game_board: np.ndarray,
            current_player: int, 
            AI_index : int, 
             max_depth: int
            ) -> Tuple[int, int, int]: 
    if not np.any(game_board): # empty, AI starts first
        best_first_moves = [
            (1, 1, 8),
            (1, 4, 8),
            (4, 1, 8),
            (4, 4, 1)
        ]
        return random.choice(best_first_moves)
    
    alpha = -math.inf
    beta = +math.inf
    
    best_utility = -math.inf
    possible_moves = generate_all_moves(game_board) 
    random.shuffle(possible_moves) # increase chances of pruning earlier, on average
    
    # use two for loops here, first to just check if any move wins, 2nd to actually do the minimax 
    # the idea is if the next immediate move can lead to a victory, then no point minimaxing any of the other moves 
    for i in tqdm(possible_moves, desc='checking if AI can win immediately :) ...'):
        rowi = i[0]
        coli = i[1]
        roti = i[2]
        
        new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti)
        if check_utility(new_board, current_player, AI_index) >= +20: # AI has won
            return (rowi, coli, roti) # no need to minimax anything 
        
    for i in tqdm(possible_moves, desc='simulating next move for AI (minimax)...'):
        rowi = i[0]
        coli = i[1]
        roti = i[2]
        
        if roti is None: # moves without rotation are definitely invalid since we already checked if AI could win immediately
            continue 
        
        new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti)

        evaluation = alpha_beta_minimax(new_board, max_depth - 1, current_player, AI_index, alpha, beta)
        alpha = max(alpha, evaluation) # update alpha 
        if evaluation >= best_utility: # maximise AI 
            best_utility = evaluation   
            best_move = (rowi, coli, roti)
         
    return best_move

def minimax_memoize(game_board : np.ndarray,
            depth : int,
            current_player : int,
            AI_index : int,
            transposition_table : dict,
            ) -> float:  
    next_player = current_player%2 + 1

    if np.all(game_board): # tie 
        return 0, transposition_table 
    
    else: # not tie, check for victory 
        terminal_utility = check_utility(game_board, current_player, AI_index)
        terminal_utility_other_player = check_utility(game_board, next_player, AI_index)
        if terminal_utility >= 20: # AI has won, check if other play wins also...
            if terminal_utility_other_player <= 20: # human also won
                if current_player == AI_index: # AI made the move, so AI loses
                    return -20, transposition_table
                else: # human made the move, so AI wins 
                    return +20, transposition_table
            else: # human didn't win, only AI won
                return +20, transposition_table
        
        elif terminal_utility <= -20: # human won (and AI cannot win, since we already checked that)
            return -20, transposition_table                    

        elif depth == 0: # max depth   
            return terminal_utility, transposition_table  
    
    if next_player == AI_index: # maximise AI 
        utility = -math.inf 
        possible_moves = generate_all_moves(game_board)  # generates possible moves for AI to make
        random.shuffle(possible_moves)
        
        for i in possible_moves:
            rowi = i[0]
            coli = i[1]
            roti = i[2]
            new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) # simulates move made by other player
            this_state = str(new_board.tostring())+str(next_player)+str(AI_index)+str(depth - 1)
            
            if this_state in transposition_table: 
                evaluation = transposition_table[this_state]
            else:
                evaluation, transposition_table = minimax_memoize(new_board, depth - 1, next_player, 
                                                                 AI_index, transposition_table)            
                transposition_table[this_state] = evaluation
            utility = max(utility, evaluation)
        return utility, transposition_table 
    
    else: # human, minimising player
        utility = +math.inf
        possible_moves = generate_all_moves(game_board)  # generates moves for human to make
        random.shuffle(possible_moves)
        
        for i in possible_moves:
            rowi = i[0]
            coli = i[1]
            roti = i[2]
            new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) # simulates move made by human 
            this_state = str(new_board.tostring())+str(next_player)+str(AI_index)+str(depth - 1)
            
            if this_state in transposition_table: 
                evaluation = transposition_table[this_state]
            else:
                evaluation, transposition_table = minimax_memoize(new_board, depth - 1, next_player, AI_index, 
                                                                transposition_table)            
                transposition_table[this_state] = evaluation
            utility = min(utility, evaluation)
        return utility, transposition_table 
    
def get_best_move_memoize(game_board: np.ndarray,
            current_player: int, 
            AI_index : int, 
             max_depth: int
            ) -> Tuple[int, int, int]: 
    if not np.any(game_board): # empty, AI starts first
        best_first_moves = [
            (1, 1, 8),
            (1, 4, 8),
            (4, 1, 8),
            (4, 4, 1)
        ]
        return random.choice(best_first_moves)
    
    transposition_table = {}  
    
    best_utility = -math.inf
    possible_moves = generate_all_moves(game_board) 
    random.shuffle(possible_moves) # increase chances of pruning earlier, on average
    
    # use two for loops here, first to just check if any move wins, 2nd to actually do the minimax 
    # the idea is if the next immediate move can lead to a victory, then no point minimaxing any of the other moves 
    for i in tqdm(possible_moves, desc='checking if AI can win immediately :) ...'):
        rowi = i[0]
        coli = i[1]
        roti = i[2]
        
        new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti)
        if check_utility(new_board, current_player, AI_index) >= +20: # AI has won
            return (rowi, coli, roti) # no need to minimax anything 
        
    for i in tqdm(possible_moves, desc='simulating next move for AI (minimax)...'):
        rowi = i[0]
        coli = i[1]
        roti = i[2]
        
        if roti is None: # moves without rotation are definitely invalid since we already checked if AI could win immediately
            continue 
        
        new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti) 
        this_state = str(new_board.tostring())+str(current_player)+str(AI_index)+str(max_depth - 1) 
        
        if this_state in transposition_table: 
            evaluation = transposition_table[this_state]
        else:
            evaluation, transposition_table = minimax_memoize(new_board, max_depth - 1, current_player, 
                                                             AI_index, transposition_table)
            transposition_table[this_state] = evaluation
         
        if evaluation >= best_utility: # maximise AI 
            best_utility = evaluation   
            best_move = (rowi, coli, roti)
            if best_utility >= 20: # no need to search further! 
                return best_move
    
    return best_move
 
 
# alpha beta + transposition table doesn't work for now - it is quite complicated to set up 
# def alpha_beta_minimax_memoize(game_board : np.ndarray,
#             depth : int,
#             current_player : int,
#             AI_index : int,
#             alpha : int,
#             beta : int,
#             transposition_table : dict,
#             ) -> float:  
#     next_player = current_player%2 + 1

#     if np.all(game_board): # tie
# #         this_state = str(game_board.tostring())+str(current_player)+str(AI_index)+str(depth)
# #         transposition_table[this_state] = 0
#         return 0, transposition_table 
    
#     else: # not tie, check for victory 
#         terminal_utility = check_utility(game_board, current_player, AI_index)
#         if abs(terminal_utility) >= 20: # someone has won 
#             # technically should check if other play wins also...
#             if current_player == AI_index:
# #                 this_state = str(game_board.tostring())+str(current_player)+str(AI_index)+str(depth)
# #                 transposition_table[this_state] = +20
#                 return +20, transposition_table
#             else: # human
# #                 this_state = str(game_board.tostring())+str(current_player)+str(AI_index)+str(depth)
# #                 transposition_table[this_state] = -20
#                 return -20, transposition_table

#         elif depth == 0: # max depth  
# #             this_state = str(game_board.tostring())+str(current_player)+str(AI_index)+str(depth)
# #             transposition_table[this_state] = terminal_utility
#             return terminal_utility, transposition_table  
    
#     to_break = False
#     if next_player == AI_index: # maximise AI 
#         maxEval = -math.inf 
#         possible_moves = generate_all_moves(game_board)  # generates possible moves for AI to make
#         random.shuffle(possible_moves)
        
#         for i in possible_moves:
#             rowi = i[0]
#             coli = i[1]
#             roti = i[2]
#             new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) # simulates move made by other player
# #             new_board_string = ''.join([str(element) for element in new_board.flatten().tolist()])
#             this_state = str(new_board.tostring())+str(next_player)+str(AI_index)+str(depth - 1)
            
#             if this_state in transposition_table:
# #                 print('Retrieving from transposition table!')
#                 evaluation = transposition_table[this_state]
#                 alpha = max(alpha, evaluation)
#                 maxEval = max(maxEval, evaluation)
#                 if beta <= alpha:
#                     to_break = True
#             else:
#                 evaluation, transposition_table = alpha_beta_minimax_memoize(new_board, depth - 1, next_player, AI_index, alpha, beta,
#                                                        transposition_table)            
#                 alpha = max(alpha, evaluation)
#                 maxEval = max(maxEval, evaluation)
#                 if beta <= alpha:
#                     to_break = True
#                 else:
#                     transposition_table[this_state] = evaluation
            
#             if to_break:
#                 break
#         return maxEval, transposition_table 
    
#     else: # human, minimising player
#         minEval = +math.inf
#         possible_moves = generate_all_moves(game_board)  # generates moves for human to make
#         random.shuffle(possible_moves)
        
#         for i in possible_moves:
#             rowi = i[0]
#             coli = i[1]
#             roti = i[2]
#             new_board = apply_move(game_board.copy(), next_player, rowi, coli, roti) # simulates move made by human
# #             new_board_string = ''.join([str(element) for element in new_board.flatten().tolist()])
#             this_state = str(new_board.tostring())+str(next_player)+str(AI_index)+str(depth - 1)
            
#             if this_state in transposition_table:
# #                 print('Retrieving from transposition table!')
#                 evaluation = transposition_table[this_state]
#                 beta = min(beta, evaluation)
#                 minEval = min(minEval, evaluation)
#                 if beta <= alpha:
#                     to_break = True
#             else:
#                 evaluation, transposition_table = alpha_beta_minimax_memoize(new_board, depth - 1, next_player, AI_index, 
#                                                                              alpha, beta, 
#                                                                        transposition_table)            
#                 beta = min(beta, evaluation)
#                 minEval = min(minEval, evaluation)
#                 if beta <= alpha:
#                     to_break = True
#                 else:
#                     transposition_table[this_state] = evaluation
                    
#             if to_break:
#                 break
#         return minEval, transposition_table 
    
# def alpha_beta_get_best_move_memoize(game_board: np.ndarray,
#             current_player: int, 
#             AI_index : int, 
#              max_depth: int
#             ) -> Tuple[int, int, int]: 
#     if not np.any(game_board): # empty, AI starts first
#         best_first_moves = [
#             (1, 1, 8),
#             (1, 4, 8),
#             (4, 1, 8),
#             (4, 4, 1)
#         ]
#         return random.choice(best_first_moves)
    
#     transposition_table = {} 
#     alpha = -math.inf
#     beta = +math.inf
    
#     best_utility = -math.inf
#     possible_moves = generate_all_moves(game_board) 
#     random.shuffle(possible_moves) # increase chances of pruning earlier, on average
    
#     # use two for loops here, first to just check if any move wins, 2nd to actually do the minimax 
#     # the idea is if the next immediate move can lead to a victory, then no point minimaxing any of the other moves 
#     for i in tqdm(possible_moves, desc='checking if AI can win immediately :) ...'):
#         rowi = i[0]
#         coli = i[1]
#         roti = i[2]
        
#         new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti)
#         if check_utility(new_board, current_player, AI_index) >= +20: # AI has won
#             return (rowi, coli, roti) # no need to minimax anything 
        
#     for i in tqdm(possible_moves, desc='simulating next move for AI (minimax)...'):
#         rowi = i[0]
#         coli = i[1]
#         roti = i[2]
        
#         if roti is None: # moves without rotation are definitely invalid since we already checked if AI could win immediately
#             continue 
        
#         new_board = apply_move(game_board.copy(), current_player, rowi, coli, roti)
# #         new_board_string = ''.join([str(element) for element in new_board.flatten().tolist()])
#         this_state = str(new_board.tostring())+str(current_player)+str(AI_index)+str(max_depth - 1) # 
        
#         if this_state in transposition_table:
# #             print('Retrieving from transposition table!')
#             evaluation = transposition_table[this_state]
#         else:
#             evaluation, transposition_table = alpha_beta_minimax_memoize(new_board, max_depth - 1, current_player, AI_index, alpha, beta,
#                                                transposition_table)
#             transposition_table[this_state] = evaluation
        
#         alpha = max(alpha, evaluation) # update alpha 
#         if evaluation >= best_utility: # maximise AI 
#             best_utility = evaluation   
#             best_move = (rowi, coli, roti)
#             if best_utility >= 20: # no need to search further! 
#                 return best_move
    
#     return best_move