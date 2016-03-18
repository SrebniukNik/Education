# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using 
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.room = [[0 for c in range(self.height)] for r in range(self.width)]

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.room[int(pos.getX())][int(pos.getY())] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return True if self.room[m][n] == 1 else False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.height * self.width

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum(item for row in self.room for item in row)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = round(random.uniform(0.0, float(self.width)),2)
        y = round(random.uniform(0.0, float(self.height)),2)
        return Position(x,y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        #print "if position in room", pos
        if 0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height:
            return True
        else:
            return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.robot_position = room.getRandomPosition()
        self.room = room
        self.speed = abs(float(speed))
        self.room.cleanTileAtPosition(self.robot_position)
        self.direction = random.randrange(0, 360)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        #print "Retrieve robot position", self.robot_position
        return self.robot_position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        #print "Retrieve robot position", self.robot_position
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.robot_position = position
        #print "Current robot position", self.robot_position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.robot_position = self.robot_position.getNewPosition(self.direction, self.speed)
        self.room.cleanTileAtPosition(self.robot_position)




# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        t = 1
        while t:
            temp_position = self.robot_position.getNewPosition(self.direction, self.speed)
            if ( 0 <= temp_position.getY() <= self.room.height) and ( 0 <= temp_position.getX() <= self.room.width):
                self.robot_position = temp_position
                self.room.cleanTileAtPosition(self.robot_position)
                t = 0
            else:
                self.direction = (self.direction + 100) % 360


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    room_size = width * height

    total_trials = []
    robots = [0]*num_robots

    for trial in range(num_trials):
        trial = 0
        room = RectangularRoom(width, height)
        # Initialize robots
        for robot in range(num_robots):
            robots[robot] = robot_type(room, speed)
        #Cleaning room
        #anim = ps2_visualize.RobotVisualization(num_robots, width, height)
        while min_coverage > room.getNumCleanedTiles() / float(room_size):
            for robot in robots:
                robot.updatePositionAndClean()
            #anim.update(room, robots)

            trial +=1
        #anim.done()
        total_trials.append(trial)

    mean = sum(total_trials)/float(len(total_trials))

    #return "Total trials", total_trials, "Mean is ", mean
    return mean

# Uncomment this line to see how much your simulation takes on average


# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        while True:
            pos_pool = []
            cur_pos = self.robot_position
            cur_x = int(cur_pos.getX())
            cur_y = int(cur_pos.getY())
            for x in range(cur_x-1, cur_x+2):
                for y in (cur_y-1, cur_y+2):
                    if 0 <= x < self.room.width and 0 <= y < self.room.height:
                        pos_pool.append((x,y))
            #print "\ninitial robot position", self.robot_position
            #print "all available moves", pos_pool
            if (cur_x,cur_y) in pos_pool:
                pos_pool.remove((cur_x, cur_y))
            moveToPos = random.choice(pos_pool)
            #print "selected move ", moveToPos
            #Description of movement
            next_x, next_y = moveToPos
            #Looking for direction angle
            temp_direction = math.degrees(math.atan2(next_y - cur_y,next_x - cur_x))
            #print "Initial direction ", temp_direction
            if temp_direction < 0:
                temp_direction += 360
            #Cleaning next position
            #Next position
            nextPos = Position(moveToPos[0],moveToPos[1])
            self.room.cleanTileAtPosition(nextPos)
            self.robot_position = nextPos
            #Move to next position
            self.direction = temp_direction
            #print "Final direction", self.direction, "\n"
            break


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.4, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.4, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.4, 20, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.4, 20, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#showPlot1("Time It Takes 1 - 10 Robots To Clean 80% Of A Room", "Number of robots", "Time-steps ")
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
showPlot2("Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms ", "Apect ratio", "Time")
#       (... your call here ...)
#


#print runSimulation(5, 1.0, 10, 10, 0.99, 30, RandomWalkRobot)

#anim = ps2_visualize.RobotVisualization(num_robots, width, height)

# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)

# #Create Position object
# point = Position(6.00,2.90)
# #Create room
# room = RectangularRoom(6, 3)
# #room.cleanTileAtPosition([3,2])
# #room.cleanTileAtPosition(point)
# print room.isPositionInRoom(point)
# print room.room
# print room.getNumCleanedTiles()

# robot = Robot(RectangularRoom(5,8), 1.0)
# print robot.getRobotPosition()
#
# if robot.room.isPositionInRoom(Position(1.00,0.00)):
#     robot.setRobotPosition(Position(1.00,0.00))
#
#     print robot.getRobotPosition()

#sd_robot = StandardRobot(RectangularRoom(5,8), 1.0)