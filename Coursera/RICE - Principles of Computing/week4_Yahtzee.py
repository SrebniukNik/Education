"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor

codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    score_board = {}
    for hand_outcome in hand:
        if hand_outcome not in score_board:
            score_board[hand_outcome] = hand_outcome
        else:
            score_board[hand_outcome] += hand_outcome
    return max(score_board.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_combi_of_free_dices = gen_all_sequences(set(list(range(1, num_die_sides - 1))), num_free_dice)

    # Calculating total value of all combinations
    total = 0
    for held in all_combi_of_free_dices:
        total += score(held + held_dice)

    # Calculating expected value
    return float(total) / (num_die_sides ** num_free_dice)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    for hand_item in hand:
        temp_set = set()
        iter_set = answer_set.copy()
        # print "1. iter_set", iter_set
        for partial_sequence in iter_set:
            # print "2. partial_sequence tuple", partial_sequence
            new_sequence = list(partial_sequence)
            # print "3. new_sequence list", new_sequence
            new_sequence.append(hand_item)
            # print "4. new_sequence updated", new_sequence
            temp_set.add(tuple(new_sequence))
            # print "5. temp_set", temp_set
            answer_set.update(temp_set)
            # print "6. answer_set updated", answer_set
            # print "*"*20
    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    expected_values = {}
    for held_dice in gen_all_holds(hand):
        expected_values[held_dice] = expected_value(held_dice, num_die_sides, len(hand) - len(held_dice))

    dice_to_hold = keywithmaxval(expected_values)
    expected_score = expected_values[dice_to_hold]
    return (expected_score, dice_to_hold)


def keywithmaxval(expected):
    """
    a) create a list of the dict's keys and values;
    b) return the key with the max value
    """
    expected_values = list(expected.values())
    expected_keys = list(expected.keys())
    return expected_keys[expected_values.index(max(expected_values))]


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

# run_example()


# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
