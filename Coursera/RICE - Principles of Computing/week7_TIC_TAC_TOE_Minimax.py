"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor

codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # Check if somebody have win at this moment
    status = board.check_win()
    if status:
        return SCORES[status], (-1, -1)

    # Initial values
    result = (-1, (-1, -1))

    # DFS for every empty_cell
    for empty_cell in board.get_empty_squares():
        board_copy = board.clone()
        board_copy.move(empty_cell[0], empty_cell[1], player)
        score = mm_move(board_copy, provided.switch_player(player))
        # print score
        if score[0] * SCORES[player] == 1:
            return score[0], empty_cell
        elif score[0] * SCORES[player] == 0:
            result = (score[0], empty_cell)

    return result[0] * SCORES[player], result[1]


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
