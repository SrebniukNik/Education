"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = zombie_list
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = human_list
        else:
            self._human_list = []

    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        ans += "Humans: " + str(self._human_list) + "\n"
        ans += "Zombies: " + str(self._zombie_list) + "\n"
        return ans

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._human_list = []
        self._zombie_list = []
        poc_grid.Grid.clear(self)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        return (human for human in self._human_list)

    def obstacle(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        return (obstacle for obstacle in self._obstacle_list)

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # Phase Two. Step 1
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        # Populating visited with obstacles
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])
            # Phase Two. Step 2
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]
        # Phase Two. Step 3
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            current_list = self._human_list[:]
        elif entity_type == ZOMBIE:
            current_list = self._zombie_list[:]

        for cell in current_list:
            boundary.enqueue(cell)
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        # Phase Two. Step 4
        while boundary:
            current_cell = boundary.dequeue()
            all_neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in all_neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[current_cell[0]][current_cell[1]] + 1,
                                                                   distance_field[neighbor[0]][neighbor[1]])
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_temp_list = []
        for human in self.humans():
            distance = []
            location = []
            all_human_neighbours = self.eight_neighbors(human[0], human[1])
            distance.append(zombie_distance_field[human[0]][human[1]])
            location.append(human)

            for neighbor in all_human_neighbours:
                if self.is_empty(neighbor[0], neighbor[1]):
                    # Form list with all distances for neighbors
                    distance.append(zombie_distance_field[neighbor[0]][neighbor[1]])
                    location.append(neighbor)
            # Find the best safe place(location)
            best_location = location[distance.index(max(distance))]
            self.set_empty(human[0], human[1])
            human_temp_list.append(best_location)

        self._human_list = human_temp_list

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_temp_list = []
        for zombie in self.zombies():
            distance = []
            location = []
            all_zombie_neighbours = self.four_neighbors(zombie[0], zombie[1])
            distance.append(human_distance_field[zombie[0]][zombie[1]])
            location.append(zombie)

            for neighbor in all_zombie_neighbours:
                if self.is_empty(neighbor[0], neighbor[1]):
                    # Form list with all distances for neighbors
                    distance.append(human_distance_field[neighbor[0]][neighbor[1]])
                    location.append(neighbor)
            # Find the best safe place(location)
            best_chase = location[distance.index(min(distance))]
            self.set_empty(zombie[0], zombie[1])
            zombie_temp_list.append(best_chase)

        self._zombie_list = zombie_temp_list

        # Start up gui for simulation - You will need to write some code above
        # before this will work without errors

        # poc_zombie_gui.run_gui(Apocalypse(3, 3))