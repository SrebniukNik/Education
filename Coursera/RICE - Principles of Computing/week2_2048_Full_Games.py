"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # Step1. Putting 0 to the end of the list.
    result = []
    for cell in line:
        if cell != 0:
            result.append(cell)
    for cell in range(line.count(0)):
        result.append(0)
    # Step1. Replaced with a tile of twice the value and a zero tile
    for cell in range(len(result) - 1):
        if result[cell] == result[cell + 1] and len(result) != 1:
            result[cell] += result[cell]
            result[cell + 1] = 0
    # Step1. Repeat step1
    final_result = []
    for cell in result:
        if cell != 0:
            final_result.append(cell)
    for cell in range(result.count(0)):
        final_result.append(0)
    return final_result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    P10 = 0
    TOTAL = 1

    # Step2. Defyning class variable
    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width

        self._slices = {}
        self._slices[UP] = [[0, cell] for cell in range(self._grid_width)]
        self._slices[DOWN] = [[self._grid_height - 1, cell] for cell in range(self._grid_width)]
        self._slices[LEFT] = [[cell, 0] for cell in range(self._grid_height)]
        self._slices[RIGHT] = [[cell, self._grid_width - 1] for cell in range(self._grid_height)]

        self._sizes = {}
        self._sizes[UP] = grid_height
        self._sizes[DOWN] = grid_height
        self._sizes[LEFT] = grid_width
        self._sizes[RIGHT] = grid_width

        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._value = [[0 * (dummy_col + dummy_row) for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]

        for dummy_i in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        debug_str = ""
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                debug_str += (str(self._value[row][col]) + " ")
            debug_str += '\n'
        return debug_str

    # Step3. Create board
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    # Step3. Create board
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        temp_list = []
        moved = False
        for dummy_i in self._slices[direction]:
            for dummy_j in range(self._sizes[direction]):
                temp_list.append(self._value[dummy_i[0] + OFFSETS[direction][0] * dummy_j] \
                                     [dummy_i[1] + OFFSETS[direction][1] * dummy_j])
            merging_list = merge(temp_list)

            if merging_list != temp_list:
                for dummy_k in range(self._sizes[direction]):
                    self._value[dummy_i[0] + OFFSETS[direction][0] * dummy_k] \
                        [dummy_i[1] + OFFSETS[direction][1] * dummy_k] = merging_list[dummy_k]
                moved = True
            temp_list = []
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile = 0
        aval_pos = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._value[row][col] == 0:
                    aval_pos.append([row, col])
                    #        print "Avalaible position", aval_pos
        percent = float(TwentyFortyEight.P10) / float(TwentyFortyEight.TOTAL) * 100.0
        #        print "Percent: ", percent
        if aval_pos:
            random_cell = random.choice(aval_pos)
            #            print "Random cell", random_cell
            if random.choice([2, 4]) == 4 and percent <= 10.0:
                #                print "Tile value: 4"
                TwentyFortyEight.P10 += 1
                TwentyFortyEight.TOTAL += 1
                tile = 4
            else:
                #                print "Tile value: 2"
                TwentyFortyEight.TOTAL += 1
                tile = 2

        else:
            print "No positions. Game over"
        self.set_tile(random_cell[0], random_cell[1], tile)

    #        print "random_cell[0]", random_cell[0], "random_cell[1]",random_cell[1]
    #        print self.value

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # Step4. Create board
        self._value[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        #        print self._value
        #        print "row ", row , "Col", col
        return self._value[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
