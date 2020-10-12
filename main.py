import random
from typing import List, Optional
from game import Game

def menu():
    print('WELCOME TO') 
    print(' _____  ______ _   _ _______       _____  ____ ')
    print('|  __ \|  ____| \ | |__   __|/\   / ____|/ __ \ ')
    print('| |__) | |__  |  \| |  | |  /  \ | |  __| |  | | ')
    print('|  ___/|  __| | . ` |  | | / /\ \| | |_ | |  | | ')
    print('| |    | |____| |\  |  | |/ ____ \ |__| | |__| | ')
    print('|_|    |______|_| \_|  |_/_/    \_\_____|\____/ ')
    
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
                player_two = 'Computer'
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
        win_length = input(f'Default = 5. Minimum = 3. Maximum = 14. It also cannot exceed the board size, which is {game_size}: ')
        try: 
            win_length = int(win_length)
            if win_length > game_size:
                print(f'Number entered {win_length} exceeds board size {game_size}!!')
                continue
            if 14 >= win_length >= 5: 
                print(f'Number entered {win_length}')
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
            first_colour = colour_left
            sec_player = col_to_player[colour_right]
            sec_colour = colour_right
            break 
        elif picked_hand == 'right':
            print(f'The colour you chose is {colour_right}')
            first_player = col_to_player[colour_right]
            first_colour = colour_right
            sec_player = col_to_player[colour_left]
            sec_colour = colour_left
            break 
        else:
            print('You entered an invalid input!')
        
    game = Game(num_humans, game_size, win_length, first_player, sec_player, level) # init game object
    while True:
        game.display_board()
        
        print('\nPentago is a work in progress! Check back later for updates ;)')
        break 
        
        # whenever player inputs 'quit', 
        # break this loop 
        # print ('Thank you for playing Pentago!!! This game was made by Cynthia, Min Htoo & Wesley.')
        
        
        if game.state in [1, 2, 3]:
            print(game.state_full)
            print('\nThank you for playing Pentago!!!!')
            print('This game was made by Cynthia, Min Htoo & Wesley!')
            break 
        else:
            game.increment_turn() # add 1 to turn 
                                                              