import random
import pylab


class Location(object):
    
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y
        
    def move(self, new_X, new_Y):
        """deltaX and deltaY are floats"""
        return Location(new_X, new_Y)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5

    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'


class Field(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.drunks = {}
        
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc
            
    def moveDrunk(self, drunk, move):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        #use move method of Location to get new location
        current_X = currentLocation.getX()
        current_Y = currentLocation.getY()
        #SW move style
        width = self.width
        height = self.height
        params = [xDist, yDist, current_X, current_Y, width, height]
        move_function = {"SW": SW(params),
                         "BH": SW(params),
                         "SP": SP(params),
                         "WW": WW(params),
                         "WW1": WW(params)}
        new_loc_x, new_loc_y = move_function[move]
        self.drunks[drunk] = currentLocation.move(new_loc_x, new_loc_y)
        
    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]

#CORRECT
def SW(args):
    '''
    SW (Solid Walls): The drunk cannot go through the fence.
    If the drunk sees that his move will make him run into the
    fence, the drunk will hesitate and not move from the spot.
    :param args:
    :return:
    '''
    #print args
    xDist, yDist, current_X, current_Y, width, height = args
    next_X = current_X + xDist
    next_Y = current_Y + yDist
    if -width < next_X < width and -height < next_Y < height:
        current_X = next_X
        current_Y = next_Y
    return current_X, current_Y

def SP(args):
    '''
    BH (Back to Home): Whenever the drunk reaches any edge, the drunk
    is transported back to the center of the world.
    :param args:
    :return:
    '''
    xDist, yDist, current_X, current_Y, width, height = args
    next_X = current_X + xDist
    next_Y = current_Y + yDist
    if -width < next_X < width:
        current_X = next_X
    elif next_X >= width:
        current_X = next_X - width * 2
    # elif next_X < -width:
    #     current_X = width + next_X
    if -height < next_Y < height:
        current_Y = next_Y
    elif next_Y >= height:
        current_Y = next_Y - height * 2
    # elif next_Y < -height:
    #     current_Y = height + next_Y
    return current_X, current_Y

def WW(args):
    '''
    WW (Warped World): If the drunk moves past the right-most edge,
    he ends up on the top edge and vice versa. If the drunk moves past the left edge,
    he ends up on the bottom edge and vice versa.
    :param args:
    :return:
    '''
    xDist, yDist, current_X, current_Y, width, height = args
    next_X = current_X + xDist
    next_Y = current_Y + yDist
    if -width < next_X < width:
        current_X = next_X
    elif next_X >= width:
        current_Y = height
    # elif next_X < -width:
    #     current_Y = -height
    if -height <= next_Y <= height:
        current_Y = next_Y
    elif next_Y >= height:
        current_X = width
    # elif next_Y < -height:
    #     current_X = -width
    return current_X, current_Y

#CORRECT
def BH(args):
    '''
    BH (Back to Home): Whenever the drunk reaches any edge, the drunk
    is transported back to the center of the world.
    :param args:
    :return:
    '''
    xDist, yDist, current_X, current_Y, width, height = args
    next_X = current_X + xDist
    next_Y = current_Y + yDist
    if -width < next_X < width and -height < next_Y < height:
        current_X = next_X
        current_Y = next_Y
    else:
        current_X = 0
        current_Y = 0
    return current_X, current_Y

def WW1(args):
    '''
    WW (Warped World): If the drunk moves past the right-most edge,
    he ends up on the top edge and vice versa. If the drunk moves past the left edge,
    he ends up on the bottom edge and vice versa.
    :param args:
    :return:
    '''
    xDist, yDist, current_X, current_Y, width, height = args
    next_X = current_X + xDist
    next_Y = current_Y + yDist
    if next_X > width:
        current_X = current_Y
    if next_X < -width:
        current_X = current_Y
    if -width < next_X < width:
        current_X = next_X
    if next_Y > height:
        current_Y = current_X
    if next_Y < -height:
        current_Y = current_X
    if -height < next_Y < height:
        current_Y = next_Y
    return current_X, current_Y

class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name


class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoice = random.choice([(-1.0, -1.0), (-1.0, 0.0), (-1.0, 1.0), (0.0, 1.0),
                                     (0.0, -1.0), (1.0, -1.0), (1.0, 0.0), (1.0, 1.0)])
        return stepChoice


def simWalks(numSteps, width, height, file_name):

    moves = ['SW', 'SP', 'WW', 'BH', 'WW1']
    for move in moves:
        homer = UsualDrunk('Homer')
        origin = Location(0, 0)
        x_coordinates = [origin.getX()]
        y_coordinates = [origin.getY()]
        field = Field(width, height)
        field.addDrunk(homer, origin)
        for t in range(numSteps):
            field.moveDrunk(homer, move)
            new_location = field.getLoc(homer)
            x_coordinates.append(new_location.getX())
            y_coordinates.append(new_location.getY())
        pylab.plot(x_coordinates, y_coordinates, 'or',
                       label='{} Drunk'.format(move))
        pylab.title('{} drunk simulation'.format(move))
        pylab.xlabel('x coordinate')
        pylab.ylabel('y coordinate')
        pylab.legend()
        pylab.xlim(-60, 60)
        pylab.ylim(-60, 60)
        if file_name:
            new_file = file_name + "_" + move + ".png"
            pylab.savefig(new_file)
        pylab.close()


simWalks(5000, 40, 40, 'Problem4_Part2')