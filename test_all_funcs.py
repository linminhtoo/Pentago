from functions import *
from inputs import *
from minimax import *

def test_check_utility():
    #### TEST CASE ####
    board1 = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    board2 = np.array( 
        [
            [1, 0, 0, 0, 2, 0],
            [0, 1, 2, 1, 0, 0],
            [2, 0, 0, 0, 0, 2],
            [0, 2, 1, 0, 1, 1],
            [0, 1, 2, 0, 1, 0],
            [1, 0, 0, 0, 2, 0]
        ]
    )
    board3 = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 2, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 2, 2, 2]
        ]
    )
    board4 = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 2, 1, 0, 2],
            [0, 0, 0, 0, 1, 2],
            [0, 0, 2, 0, 0, 2]
        ]
    )

    # if AI starts second, AI_index = 2, but it'll be 1 if AI starts first! 
    assert check_utility(board1, 1, 2) == -12.0 
    assert check_utility(board2, 1, 2) == -12.0
    assert check_utility(board2, 2, 2) == +4.0 
    assert check_utility(board3, 2, 2) == +12.0
    assert check_utility(board4, 2, 2) == -20.0

def test_check_input_row_and_col():
    ######################
    ##### TEST CASES #####
    ######################
    game_size = 6

    assert check_input_row_and_col(-1, 0, game_size) == (False, None, None)
    assert check_input_row_and_col(0, -1, game_size) == (False, None, None)
    assert check_input_row_and_col(7, 0, game_size) == (False, None, None)
    assert check_input_row_and_col(0, 7, game_size) == (False, None, None)
    assert check_input_row_and_col('one', 0, game_size) == (False, None, None)
    assert check_input_row_and_col(0, 'one', game_size) == (False, None, None)
    assert check_input_row_and_col(None, 0, game_size) == (False, None, None)
    assert check_input_row_and_col(5, 1, game_size) == (True, 4, 0)
    assert check_input_row_and_col(1, 5, game_size) == (True, 0, 4)
    assert check_input_row_and_col('5', 1, game_size) == (True, 4, 0)
    assert check_input_row_and_col(1, '5', game_size) == (True, 0, 4)
    print('\n')

def test_check_input_rot():
    assert check_input_rot('1L') == (True, '1L')
    assert check_input_rot('8L') == (False, None)

def test_generate_random_move():
    ######################
    ##### TEST CASES #####
    ######################
    my_board_one = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [1, 1, 0, 0, 2, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 2, 1, 0, 0]
        ]
    )

    my_board_two = np.array(
        [
            [1, 0, 1, 2, 1, 2],
            [1, 2, 1, 1, 2, 1],
            [2, 2, 2, 1, 1, 1],
            [1, 1, 1, 2, 2, 1],
            [2, 2, 2, 1, 1, 2],
            [1, 1, 1, 2, 2, 1],
        ]
    )

    no_valid_moves = np.array(
        [
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 1, 2, 1],
            [2, 2, 2, 1, 1, 1],
            [1, 1, 1, 2, 2, 1],
            [2, 2, 2, 1, 1, 2],
            [1, 1, 1, 2, 2, 1],
        ]
    )

    row, col, _ = generate_random_move(my_board_one)
    assert check_move(my_board_one, row, col) == True

    row, col, _ = generate_random_move(my_board_two)
    assert check_move(my_board_two, row, col) == True
    assert (row, col) == (0, 1)

    try: 
        generate_random_move(no_valid_moves)
        raise RuntimeError('Error! generate_random_move() produced a move on a full board without raising error.')
    except:
        print('Passed test case: did not generate any moves on a full board')

def test_check_move():    
    ######################
    ##### TEST CASES #####
    ######################
    my_board_one = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [1, 1, 0, 0, 2, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 2, 1, 0, 0]
        ]
    )

    my_board_two = np.array(
        [
            [1, 0, 1, 2, 1, 2],
            [1, 2, 1, 1, 2, 1],
            [2, 2, 2, 1, 1, 1],
            [1, 1, 1, 2, 2, 1],
            [2, 2, 2, 1, 1, 2],
            [1, 1, 1, 2, 2, 1],
        ]
    )

    no_valid_moves = np.array(
        [
            [1, 2, 1, 2, 1, 2],
            [1, 2, 1, 1, 2, 1],
            [2, 2, 2, 1, 1, 1],
            [1, 1, 1, 2, 2, 1],
            [2, 2, 2, 1, 1, 2],
            [1, 1, 1, 2, 2, 1],
        ]
    )

    empty_board = np.zeros((6, 6))

    assert check_move(my_board_one, 5, 5) == True
    assert check_move(my_board_two, 0, 1) == True
    for row, col in zip(range(5), range(5)):
        assert check_move(empty_board, row, col) == True
    for row, col in zip(range(5), range(5)):
        assert check_move(no_valid_moves, row, col) == False



def test_rotate_quadrant():
    ######################
    ##### TEST CASES #####
    ######################
    my_board_rot2 = np.array( 
        [
            [0, 0, 0, 0, 0, 1],
            [2, 1, 0, 1, 1, 0],
            [1, 0, 1, 1, 2, 0],
            [1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [1, 0, 2, 0, 0, 0]
        ]
    )

    my_board_rot3 = np.array( 
        [
            [1, 2, 0, 1, 1, 0],
            [0, 1, 0, 2, 1, 0],
            [1, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [1, 0, 2, 0, 0, 0]
        ]
    )

    my_board_rot4 = np.array( 
        [
            [1, 2, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 2],
            [1, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [1, 0, 2, 0, 0, 0]
        ]
    )

    my_board_rot5 = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [1, 0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0]
        ]
    )

    my_board_rot6 = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [0, 0, 2, 1, 0, 0],
            [1, 1, 0, 0, 0, 2],
            [1, 0, 1, 0, 0, 0]
        ]
    )

    my_board_rot7 = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [1, 1, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 2, 0, 2, 0]
        ]
    )

    my_board_rot8 = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [1, 1, 0, 0, 2, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 2, 1, 0, 0]
        ]
    )

    my_board_initial = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 2, 0],
            [1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [1, 0, 2, 0, 0, 0]
        ]
    )

    my_board_rot1 = np.array( 
        [
            [1, 0, 1, 0, 0, 1],
            [0, 1, 2, 1, 1, 0],
            [0, 0, 0, 1, 2, 0],
            [1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [1, 0, 2, 0, 0, 0]
        ]
    )

    assert np.array_equal(rotate_quadrant(my_board_initial, 1), my_board_rot1)

    assert np.array_equal(rotate_quadrant(my_board_initial, 2), my_board_rot2)
    assert np.array_equal(rotate_quadrant(my_board_initial, 3), my_board_rot3)
    assert np.array_equal(rotate_quadrant(my_board_initial, 4), my_board_rot4)
    assert np.array_equal(rotate_quadrant(my_board_initial, 5), my_board_rot5)
    assert np.array_equal(rotate_quadrant(my_board_initial, 6), my_board_rot6)
    assert np.array_equal(rotate_quadrant(my_board_initial, 7), my_board_rot7)
    assert np.array_equal(rotate_quadrant(my_board_initial, 8), my_board_rot8) 


def test_check_neutral_quadrants():
    ######################
    ##### TEST CASES #####
    ######################
    top_left_neutral = np.array( 
        [
            [0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 2],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0]
        ]
    )

    sample_neutral_1 = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
    )

    no_neutral_1 = np.array( 
        [
            [1, 0, 1, 0, 0, 1],
            [0, 1, 2, 1, 1, 0],
            [0, 0, 0, 1, 2, 0],
            [1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2],
            [1, 0, 2, 0, 0, 0]
        ]
    )

    TL, TR, BL, BR = split_into_quadrants(top_left_neutral)
    assert TL.nonzero() == (1,1) 
    assert check_neutral_quadrants(top_left_neutral) == True

    assert check_neutral_quadrants(sample_neutral_1) == True
    assert check_neutral_quadrants(no_neutral_1) == False


def test_check_victory():
    ######################
    ##### TEST CASES #####
    ######################
    my_board_no_victory = np.array( 
        [
            [1, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 1]
        ]
    )

    my_board_row_no_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    my_board_col_no_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )
    my_board_col_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
    )

    my_board_col_victory_one_b = np.array( 
        [
            [0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )


    my_board_row_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    my_board_row_victory_one_b = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    my_board_pos_diag_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    my_board_pos_diag_victory_one_b = np.array( 
        [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1]
        ]
    )

    my_board_neg_diag_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    my_board_neg_diag_victory_one_b = np.array( 
        [
            [1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
    )

    my_board_neg_diag_victory_two_a = np.array( 
        [
            [1, 0, 2, 0, 2, 1],
            [2, 1, 2, 1, 2, 0],
            [1, 0, 0, 2, 0, 0],
            [1, 1, 2, 0, 0, 1],
            [0, 2, 0, 2, 1, 2],
            [2, 0, 1, 0, 1, 1]
        ]
    )

    my_board_neg_diag_victory_two_b = np.array( 
        [
            [1, 0, 2, 0, 2, 2],
            [2, 1, 2, 1, 2, 0],
            [1, 0, 0, 2, 0, 0],
            [1, 1, 2, 0, 0, 1],
            [0, 2, 0, 2, 1, 2],
            [1, 0, 1, 0, 1, 1]
        ]
    )

    my_board_neg_diag_victory_two_c = np.array( 
        [
            [1, 0, 2, 0, 2, 2],
            [2, 1, 2, 1, 2, 2],
            [1, 0, 0, 2, 2, 0],
            [1, 1, 2, 2, 0, 1],
            [0, 1, 2, 2, 1, 2],
            [1, 2, 1, 0, 1, 1]
        ]
    )

    my_board_tie = np.array(
        [
            [1, 1, 1, 2, 1, 2],
            [1, 2, 1, 1, 2, 1],
            [2, 2, 2, 1, 1, 1],
            [1, 1, 1, 2, 2, 1],
            [2, 2, 2, 1, 1, 2],
            [1, 1, 1, 2, 2, 1],
        ]
    )
    negdiag2 = np.array( 
        [
            [1, 0, 2, 0, 2, 2],
            [2, 1, 2, 1, 2, 2],
            [1, 0, 0, 2, 2, 0],
            [1, 1, 2, 2, 0, 1],
            [0, 1, 2, 2, 1, 2],
            [1, 2, 1, 0, 1, 1]
        ]
    )

    assert check_victory(my_board_no_victory, 1) == 0
    assert check_victory(my_board_row_no_victory_one_a, 1) == 0
    assert check_victory(my_board_col_no_victory_one_a, 1) == 0
    assert check_victory(my_board_row_victory_one_a, 1) == 1
    assert check_victory(my_board_row_victory_one_b, 1) == 1
    assert check_victory(my_board_col_victory_one_a, 1) == 1
    assert check_victory(my_board_col_victory_one_b, 1) == 1
    assert check_victory(my_board_pos_diag_victory_one_a, 1) == 1
    assert check_victory(my_board_pos_diag_victory_one_b, 1) == 1
    assert check_victory(my_board_neg_diag_victory_one_a, 1) == 1
    assert check_victory(my_board_neg_diag_victory_one_b, 1) == 1
    assert check_victory(my_board_neg_diag_victory_two_a, 1) == 2
    assert check_victory(my_board_neg_diag_victory_two_b, 1) == 2
    assert check_victory(my_board_neg_diag_victory_two_c, 1) == 2
    assert check_victory(my_board_tie, 1) == 3

def test_find_longest():
    ######################
    ##### TEST CASES ##### for find_longest
    ######################
    my_board_no_victory = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 2],
            [1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 2, 0, 1, 1]
        ]
    )

    my_board_col_victory_one_a = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
    )

    my_board_col_victory_one_b = np.array( 
        [
            [0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 0],
            [1, 0, 2, 0, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 2, 0, 2, 0],
            [1, 0, 0, 0, 2, 0]
        ]
    )

    my_board_diag_test_one_c = np.array( 
        [
            [0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 0],
            [1, 0, 2, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 2, 1, 2, 0],
            [1, 0, 1, 0, 2, 0]
        ]
    )

    my_board_no_victory = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 2],
            [1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 2, 0, 1, 1]
        ]
    )

    my_board_win = np.array( 
        [
            [1, 2, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 2],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 2, 0, 1, 1]
        ]
    )
    
    assert find_longest(my_board_no_victory,1, 3, None, None, None) == 4
    assert find_longest(my_board_no_victory, 1, None,3, None, None) == 1
    assert find_longest(my_board_col_victory_one_a, 1, None,0, None, None) == 5
    assert find_longest(my_board_no_victory, 1, None,None, 2, None) == 2
    assert find_longest(my_board_col_victory_one_a, 1, None,None, 3, None) == 2
    assert find_longest(my_board_col_victory_one_a, 1, None,None, None, 1) == 1
    assert find_longest(my_board_col_victory_one_b, 1, None,None, None, 2) == 2
    assert find_longest(my_board_col_victory_one_b, 2, None,None, None, 3) == 0
    assert find_longest(my_board_col_victory_one_b, 2, None,4, None, None) == 2
    assert find_longest(my_board_diag_test_one_c, 1, None, None, None, 7) == 4
    assert find_longest(my_board_win, 1, 3, None, None, None) == 6


def test_generate_all_moves():
    #TEST CASE
    board1 = np.array( 
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0]
        ]
    )

    assert generate_all_moves(board1) == [(1, 0, 1),
    (1, 0, 2),
    (1, 0, 3),
    (1, 0, 4),
    (1, 0, 5),
    (1, 0, 6),
    (1, 0, 7),
    (1, 0, 8),
    (1, 0, None),
    (3, 0, 1),
    (3, 0, 2),
    (3, 0, 3),
    (3, 0, 4),
    (3, 0, 5),
    (3, 0, 6),
    (3, 0, 7),
    (3, 0, 8),
    (3, 0, None),
    (4, 0, 1),
    (4, 0, 2),
    (4, 0, 3),
    (4, 0, 4),
    (4, 0, 5),
    (4, 0, 6),
    (4, 0, 7),
    (4, 0, 8),
    (4, 0, None),
    (0, 1, 1),
    (0, 1, 2),
    (0, 1, 3),
    (0, 1, 4),
    (0, 1, 5),
    (0, 1, 6),
    (0, 1, 7),
    (0, 1, 8),
    (0, 1, None),
    (2, 1, 1),
    (2, 1, 2),
    (2, 1, 3),
    (2, 1, 4),
    (2, 1, 5),
    (2, 1, 6),
    (2, 1, 7),
    (2, 1, 8),
    (2, 1, None),
    (3, 1, 1),
    (3, 1, 2),
    (3, 1, 3),
    (3, 1, 4),
    (3, 1, 5),
    (3, 1, 6),
    (3, 1, 7),
    (3, 1, 8),
    (3, 1, None),
    (5, 1, 1),
    (5, 1, 2),
    (5, 1, 3),
    (5, 1, 4),
    (5, 1, 5),
    (5, 1, 6),
    (5, 1, 7),
    (5, 1, 8),
    (5, 1, None),
    (0, 2, 1),
    (0, 2, 2),
    (0, 2, 3),
    (0, 2, 4),
    (0, 2, 5),
    (0, 2, 6),
    (0, 2, 7),
    (0, 2, 8),
    (0, 2, None),
    (1, 2, 1),
    (1, 2, 2),
    (1, 2, 3),
    (1, 2, 4),
    (1, 2, 5),
    (1, 2, 6),
    (1, 2, 7),
    (1, 2, 8),
    (1, 2, None),
    (2, 2, 1),
    (2, 2, 2),
    (2, 2, 3),
    (2, 2, 4),
    (2, 2, 5),
    (2, 2, 6),
    (2, 2, 7),
    (2, 2, 8),
    (2, 2, None),
    (4, 2, 1),
    (4, 2, 2),
    (4, 2, 3),
    (4, 2, 4),
    (4, 2, 5),
    (4, 2, 6),
    (4, 2, 7),
    (4, 2, 8),
    (4, 2, None),
    (5, 2, 1),
    (5, 2, 2),
    (5, 2, 3),
    (5, 2, 4),
    (5, 2, 5),
    (5, 2, 6),
    (5, 2, 7),
    (5, 2, 8),
    (5, 2, None),
    (0, 3, 1),
    (0, 3, 2),
    (0, 3, 3),
    (0, 3, 4),
    (0, 3, 5),
    (0, 3, 6),
    (0, 3, 7),
    (0, 3, 8),
    (0, 3, None),
    (2, 3, 1),
    (2, 3, 2),
    (2, 3, 3),
    (2, 3, 4),
    (2, 3, 5),
    (2, 3, 6),
    (2, 3, 7),
    (2, 3, 8),
    (2, 3, None),
    (3, 3, 1),
    (3, 3, 2),
    (3, 3, 3),
    (3, 3, 4),
    (3, 3, 5),
    (3, 3, 6),
    (3, 3, 7),
    (3, 3, 8),
    (3, 3, None),
    (4, 3, 1),
    (4, 3, 2),
    (4, 3, 3),
    (4, 3, 4),
    (4, 3, 5),
    (4, 3, 6),
    (4, 3, 7),
    (4, 3, 8),
    (4, 3, None),
    (5, 3, 1),
    (5, 3, 2),
    (5, 3, 3),
    (5, 3, 4),
    (5, 3, 5),
    (5, 3, 6),
    (5, 3, 7),
    (5, 3, 8),
    (5, 3, None),
    (0, 4, 1),
    (0, 4, 2),
    (0, 4, 3),
    (0, 4, 4),
    (0, 4, 5),
    (0, 4, 6),
    (0, 4, 7),
    (0, 4, 8),
    (0, 4, None),
    (1, 4, 1),
    (1, 4, 2),
    (1, 4, 3),
    (1, 4, 4),
    (1, 4, 5),
    (1, 4, 6),
    (1, 4, 7),
    (1, 4, 8),
    (1, 4, None),
    (2, 4, 1),
    (2, 4, 2),
    (2, 4, 3),
    (2, 4, 4),
    (2, 4, 5),
    (2, 4, 6),
    (2, 4, 7),
    (2, 4, 8),
    (2, 4, None),
    (5, 4, 1),
    (5, 4, 2),
    (5, 4, 3),
    (5, 4, 4),
    (5, 4, 5),
    (5, 4, 6),
    (5, 4, 7),
    (5, 4, 8),
    (5, 4, None),
    (0, 5, 1),
    (0, 5, 2),
    (0, 5, 3),
    (0, 5, 4),
    (0, 5, 5),
    (0, 5, 6),
    (0, 5, 7),
    (0, 5, 8),
    (0, 5, None),
    (1, 5, 1),
    (1, 5, 2),
    (1, 5, 3),
    (1, 5, 4),
    (1, 5, 5),
    (1, 5, 6),
    (1, 5, 7),
    (1, 5, 8),
    (1, 5, None),
    (2, 5, 1),
    (2, 5, 2),
    (2, 5, 3),
    (2, 5, 4),
    (2, 5, 5),
    (2, 5, 6),
    (2, 5, 7),
    (2, 5, 8),
    (2, 5, None),
    (4, 5, 1),
    (4, 5, 2),
    (4, 5, 3),
    (4, 5, 4),
    (4, 5, 5),
    (4, 5, 6),
    (4, 5, 7),
    (4, 5, 8),
    (4, 5, None),
    (5, 5, 1),
    (5, 5, 2),
    (5, 5, 3),
    (5, 5, 4),
    (5, 5, 5),
    (5, 5, 6),
    (5, 5, 7),
    (5, 5, 8),
    (5, 5, None)]

if __name__ == "__main__":
    test_check_input_rot()
    test_check_input_row_and_col()
    test_check_neutral_quadrants()
    test_rotate_quadrant()
    test_check_move()
    test_check_utility()
    test_check_victory()
    test_find_longest()
    test_generate_all_moves()
    test_generate_random_move()
    print('#'*35)
    print('#####  PASSED ALL TESTCASES!  #####')
    print('#'*35)
    