"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100  # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player


# Add your functions here.

def mc_trial(board, player):
    """This function takes a current board and the next
    player to move. The function should play a game starting
    with the given player by making random moves, alternating
    between players. The function should return when the game
    is over. The modified board will contain the state of the
    game, so the function does not return anything."""
    # print "board ", board
    winner = board.check_win()
    # print "winner ",winner
    while winner == None:
        empty_cells = board.get_empty_squares()
        next_move = random.choice(empty_cells)
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
        winner = board.check_win()
        # print "-" * 20


def mc_update_scores(scores, board, player):
    """This function takes a grid of scores (a list of lists)
    with the same dimensions as the Tic-Tac-Toe board, a
    board from a completed game, and which player the machine
    player is. The function should score the completed board
    and update the scores grid. As the function updates the
    scores grid directly, it does not return anything"""
    winner = board.check_win()

    if winner in (None, provided.DRAW):
        return

    if winner == player:
        player_score = SCORE_CURRENT
        comp_score = -1 * SCORE_OTHER
    else:
        player_score = -1 * SCORE_CURRENT
        comp_score = SCORE_OTHER

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            cell_value = board.square(row, col)
            if cell_value == provided.EMPTY:
                pass
            elif cell_value == player:
                scores[row][col] += player_score
            else:
                scores[row][col] += comp_score


def get_best_move(board, scores):
    """This function takes a current board and a grid of
    scores. The function should find all of the empty squares
    with the maximum score and randomly return one of them as
    a (row, column) tuple. The case where the board is full
    will not be tested."""
    empty_cells = board.get_empty_squares()
    if len(empty_cells) == 0:
        return
    values = []
    # print "scores", scores
    for cell in empty_cells:
        values.append(scores[cell[0]][cell[1]])
    max_val = max(values)

    move_candidates = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col] == max_val and (row, col) in empty_cells:
                move_candidates.append((row, col))

    best_move = random.choice(move_candidates)
    return best_move


def mc_move(board, player, trials):
    """This function takes a current board,which player the
    machine player is,and the number of trials to run. The
    function should use the Monte Carlo simulation described
    above to return a move for the machine player in the
    form of a (row, column) tuple. Be sure to use the other
    functions you have written!"""
    scores = [[0 for dummy_y in range(board.get_dim())] for dummy_x in range(board.get_dim())]
    trial = 0
    while trial < trials:
        temp_board = board.clone()
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
        trial += 1
    # Choosing best move for Comp Player
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
