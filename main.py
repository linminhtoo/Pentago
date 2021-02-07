from functions import *
from inputs import *
from minimax import *

import numpy as np
import random
import math
from typing import Optional, Tuple, List
import time

from tqdm import tqdm

def menu():
    try:
        tqdm._instances.clear() # clear progressbar cache 
    except:
        print('')
    
    print('WELCOME TO') 
    print(' _____  ______ _   _ _______       _____  ____ ')
    print('|  __ \|  ____| \ | |__   __|/\   / ____|/ __ \ ')
    print('| |__) | |__  |  \| |  | |  /  \ | |  __| |  | | ')
    print('|  ___/|  __| | . ` |  | | / /\ \| | |_ | |  | | ')
    print('| |    | |____| |\  |  | |/ ____ \ |__| | |__| | ')
    print('|_|    |______|_| \_|  |_/_/    \_\_____|\____/ ')
    print('\n')
    
    while True:
        player_one = input("What's your name? ")
        check = input(f'You entered {player_one}. Are you sure? Type Y if yes, N to enter again: ')
        if check.upper() == 'Y':
            break
        elif check.upper() == 'N':
            continue
        else:
            print('Please enter Y or N')
    print(f'Nice to meet you {player_one}!')
    
    print('\nWould you like to play against another human, or against the computer?')
    while True:
        num_humans = input('Type 1 for computer, 2 for human: ')
        try:
            num_humans = int(num_humans)
            if num_humans == 1:
                player_two = 'computer'
                print(f'Playing against {player_two}!')
                break
                
            elif num_humans == 2: 
                
                print('Playing against another human!')
                while True:
                    player_two = input("Please enter player 2's name: ")
                    check = input(f'You entered {player_two}. Are you sure? Type Y if yes, N to enter again: ')
                    if check.upper() == 'Y':
                        break
                    elif check.upper() == 'N':
                        continue
                    else:
                        print('Please enter Y or N')
                
                print(f'Playing against {player_two}!')
                break
                
            else:
                print('You entered an invalid input!')
                continue 
        except:
            print('You entered an invalid input!')
            continue
    
    level = None
    if num_humans == 1: # if num_humans == 2, level remains as None 
        print('\n Time to choose the difficulty of the computer player!')
        print('1 = Easy computer, that makes random moves')
        print('2 = Difficult computer, that makes smart moves. Good luck beating it :)')
        while True:
            level = input('Type 1 or 2: ')
            try:
                level = int(level)
                if level == 1:
                    print('Easy computer!')
                    break
                elif level == 2:
                    print('Difficult computer! Muahahahaha')
                    break
                else:
                    print('You entered an invalid input!')
            except:
                print('You entered an invalid input!')
                 
    if level == 2:
        print('\nPlease enter a single integer, for the max_depth of the level 2 computer.')
        while True: 
            computer_depth = input('Default = 3. Minimum = 1. We recommend 2 or 3.')
            try:
                computer_depth = int(computer_depth)
                if computer_depth >= 1:
                    print(f'Computer_depth entered: {computer_depth}')
                    break
                else:
                    print('Please enter a valid positive integer.')
                    continue
            except:
                print('Please enter a valid positive integer.')
                continue 
    
    print('\nPlease enter a single integer, for the size of the game board (N x N).')
    while True: 
        game_size = input('Default = 6. Minimum = 6. Maximum = 15 (for computational reasons): ')
        try:
            game_size = int(game_size)
            if 15 >= game_size >= 6:
                print(f'Board size entered: {game_size}')
                break
            else:
                print('Please enter a valid integer between 6 (inclusive) and 15 (inclusive).')
                continue
        except:
            print('Please enter a valid integer between 6 (inclusive) and 15 (inclusive).')
            continue 
    
    print('\nPlease enter a single integer, representing the number of consecutive same-color marbles needed for a player to win.')
    while True:
        num_consecutive = input(f'Default = 5. Minimum = 3. Maximum = 14. It also cannot exceed the board size, which is {game_size}: ')
        try: 
            num_consecutive = int(num_consecutive)
            if num_consecutive > game_size:
                print(f'Number entered {num_consecutive} exceeds board size {game_size}!!')
                continue
            if 14 >= num_consecutive >= 5: 
                print(f'Number entered {num_consecutive}')
                break
            else:
                print(f'Please enter a valid integer between 3 (inclusive) and {game_size} (inclusive)')
        except:
            print(f'Please enter a valid integer between 3 (inclusive) and {game_size} (inclusive)')
            continue
        
    print('\nPlayer 1, please pick your colour!')
    while True:
        colour_one = input('Enter white or black: ')
        colour_one = colour_one.lower()
        if colour_one == 'white':
            print('You picked white!')
            break
        elif colour_one == 'black':
            print('You picked black!')
            break
        else:
            print('You entered an invalid input!')
    
    colour_two = 'white' if colour_one == 'black' else 'black'
    if num_humans == 1:
        print(f'Computer has colour {colour_two}')
    else:
        print(f'Player 2 has colour {colour_two}')
        
    print('\nTime to decide who goes first!')
    print("It's simple... the other player has hidden a white marble in one hand and a black marble in the other.")
    print('Your job is to choose one of his hands, and the colour of the marble in it will go first!')
    colour_left = random.choice(['black', 'white'])
    colour_right = 'black' if colour_left == 'white' else 'white'
    col_to_player = {
        colour_one : player_one , 
        colour_two : player_two
    }
    while True:
        picked_hand = input('Enter left or right: ')
        if picked_hand == 'left':
            print(f'The colour you chose is {colour_left}')
            first_player = col_to_player[colour_left]
            sec_player = col_to_player[colour_right]
            break 
        elif picked_hand == 'right':
            print(f'The colour you chose is {colour_right}')
            first_player = col_to_player[colour_right]
            sec_player = col_to_player[colour_left]
            break 
        else:
            print('You entered an invalid input!')
            
    ############################ GAME ###################################  
    game_board = np.zeros((game_size, game_size), int)
    print(game_board) # display board

    current_player = 1 # alternates between 1 and 2, indicates which player is making the moves
    playernum_to_name = {
                1 : first_player,
                2 : sec_player 
            }
    if num_humans == 1:
        if first_player == 'computer':
            AI_index = 1
        else:
            AI_index = 2

    human_rot_to_comp_rot = {
        '1R': 1,
        '1L': 2,
        '2R': 3,
        '2L': 4,
        '3R': 5,
        '3L': 6,
        '4R': 7,
        '4L': 8,
    }
    comp_rot_to_human_rot = {}
    for key, value in human_rot_to_comp_rot.items():
        comp_rot_to_human_rot[value] = key

    game_over = False
    while not game_over:
        while True:
            print(f"It's {playernum_to_name[current_player]}'s turn")
            time.sleep(1)

            if playernum_to_name[current_player].lower() == 'computer': 
                if level == 2:
                    row, col, rot = get_best_move_memoize(game_board, current_player, AI_index, computer_depth)
                elif level == 1:
                    row, col, rot = generate_random_move(game_board)
                
                game_board = apply_move(game_board, current_player, row=row, col=col, rot=None)
                print(f'computer placed a piece at row {row + 1}, col {col + 1}')
                print('\n', game_board, '\n') # display_board(game_board)

                new_state = check_victory(game_board, current_player)
                if new_state == 1:
                    print(f'{first_player} has won!')
                    game_over = True 
                elif new_state == 2:
                    print(f'{sec_player} has won!')
                    game_over = True 
                elif new_state == 3:
                    print("It's a tie!")
                    game_over = True 
                    
                if game_over:
                    break

                game_board = apply_move(game_board, current_player, row=None, col=None, rot=rot)
                print(f'computer chose rot {comp_rot_to_human_rot[rot]}')
                print('\n', game_board, '\n')

                new_state = check_victory(game_board, current_player)
                if new_state == 1:
                    print(f'{first_player} has won!')
                    game_over = True 
                elif new_state == 2:
                    print(f'{sec_player} has won!')
                    game_over = True 
                elif new_state == 3:
                    print("It's a tie!")
                    game_over = True 

                if game_over:
                    break  

            else:
                # human player's turn
                while True:
                    print("If at any point of the game, you wish to quit, please type 'quit' as an input\n")
                    #check format of input row and col 
                    row = input(f"{playernum_to_name[current_player]} Please select row (1 - {game_size}): ")
                    if row.lower() == 'quit':
                        game_over = True
                        break
                    col = input(f"{playernum_to_name[current_player]} Please select column (1 - {game_size}): ")
                    if col.lower() == 'quit':
                        game_over = True
                        break

                    is_valid, row, col = check_input_row_and_col(row, col, game_size)
                    if is_valid:
                        if check_move(game_board, row, col):
                            game_board = apply_move(game_board, current_player, row=row, col=col, rot=None)
                            print('\n', game_board, '\n')
                            break              
                        else: #invalid move  
                            print(f"\nrow {row + 1}, col {col + 1} is already filled. Please pick another position.")
                            continue
                    else: #invalid input format
                        print(f'You entered row {row}, col {col}, which is invalid.')
                        continue  

                if game_over:
                    break

                new_state = check_victory(game_board, current_player)
                if new_state == 1:
                    print(f'{first_player} has won!')
                    game_over = True 
                elif new_state == 2:
                    print(f'{sec_player} has won!')
                    game_over = True
                elif new_state == 3:
                    print("It's a tie!")
                    game_over = True

                if game_over:
                    break

                optional_rot = check_neutral_quadrants(game_board)
                if optional_rot:
                    while optional_rot: # give player choice whether to rotate 
                        user_rot_choice = input('Do you wish to make a rotation? Type Y for yes, N for no: ')
                        if user_rot_choice.lower() == 'quit':
                            game_over = True
                            break

                        if user_rot_choice.upper() == 'Y':
                            do_rot = True
                            break
                        elif user_rot_choice.upper() == 'N':
                            do_rot = False
                            break
                        else:
                            print(f'You entered {user_rot_choice}, which is invalid.')
                            continue   
                else: # not optional, player must rotate 
                    do_rot = True 

                if game_over:
                    break  

                while do_rot:   #player chose to rotate / has no choice, must rotate  
                    rot = input(f"{playernum_to_name[current_player]} Please select rot (1 = top left, 2 = top right, 3 = bottom left, 4 = bottom right, \nL = anti-clockwise, R = clockwise), e.g. '1L' = top left, anti-clockwise: ") 
                    if rot.lower() == 'quit': 
                        game_over = True
                        break

                    is_valid, rot = check_input_rot(rot)
                    if is_valid:
                        rot = human_rot_to_comp_rot[rot]
                        game_board = apply_move(game_board, current_player, row=None, col=None, rot=rot)
                        print('\n', game_board, '\n')
                        break
                    else: # ask for user input again
                        continue 

                if game_over:
                    break    

                new_state = check_victory(game_board, current_player)
                if new_state == 1:
                    print(f'{first_player} has won!')
                    game_over = True 
                elif new_state == 2:
                    print(f'{sec_player} has won!')
                    game_over = True 
                elif new_state == 3:
                    print("It's a tie!")
                    game_over = True 

                if game_over:
                    break  

            # switch current_player from 1 to 2 or vice-versa
            current_player %= 2 
            current_player += 1

    print('Thank you for playing Pentago! Hope to see you again. This program was made by Cynthia, Min Htoo & Wesley.')

if __name__ == '__main__':
    menu() 