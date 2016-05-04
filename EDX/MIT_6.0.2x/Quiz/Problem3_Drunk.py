import pylab, random, math

class Location(object):
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y

    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)

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
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)

    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,1.0), (0.0,-1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,0.9), (0.0,-1.03), (1.03, 0.0), (-1.03, 0.0)]
        return random.choice(stepChoices)

class EDrunk(Drunk):
    def takeStep(self):
        ang = 2 * math.pi * random.random()
        length = 0.5 + 0.5 * random.random()
        return (length * math.sin(ang), length * math.cos(ang))

class PhotoDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.0, 0.5),(0.0, -0.5),
                     (1.5, 0.0),(-1.5, 0.0)]
        return random.choice(stepChoices)

class DDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.85, 0.85), (-0.85, -0.85),
                     (-0.56, 0.56), (0.56, -0.56)]
        return random.choice(stepChoices)


def walkVector(field, drunk, numSteps):
    start = field.getLoc(drunk)
    for s in range(numSteps):
        field.moveDrunk(drunk)
    return(field.getLoc(drunk).getX() - start.getX(),
           field.getLoc(drunk).getY() - start.getY())


drunks = ( UsualDrunk, ColdDrunk, EDrunk, PhotoDrunk, DDrunk)


def simulation(drunk, numTrials, numSteps, size):
    current_drunk = ''
    room = Location(size[0], size[1])
    field = Field()
    field.addDrunk(drunk, room)
    name = drunk.getName()
    print name
    for trial in range(numTrials):
        distance = walkVector(field, drunk, numSteps)
        Drunken[name].append(distance)
    print current_drunk, "=", Drunken[name]

loc = (0, 0)

def simulation1(numTrials, numSteps, loc):
    results = {'UsualDrunk': [], 'ColdDrunk': [], 'EDrunk': [], 'PhotoDrunk': [], 'DDrunk': []}
    drunken_types = {'UsualDrunk': UsualDrunk, 'ColdDrunk': ColdDrunk, 'EDrunk': EDrunk, 'PhotoDrunk': PhotoDrunk,
                     'DDrunk': DDrunk}
    for drunken in drunken_types.keys():
        #Create field
        initial_loc = Location(loc[0], loc[1])
        field = Field()
        print "Simu", drunken
        drunk = Drunk(drunken)
        drunk_man = drunken_types[drunken](drunk)
        field.addDrunk(drunk_man, initial_loc)
        #print drunk_man
        for trial in range(numTrials):
            distance = walkVector(field, drunk_man, numSteps)
            results[drunken].append((round(distance[0], 1), round(distance[1], 1)))
        print drunken, "=", results[drunken]
    for result in results.keys():
        # x, y = zip(*results[result])
        # print "x", x
        # print "y", y
        pylab.plot(*zip(*results[result]), marker='o', color='r', ls='')
        pylab.title(result)
        pylab.xlabel('X coordinateds')
        pylab.ylabel('Y coordinateds')
        pylab.xlim(-100, 100)
        pylab.ylim(-100, 100)
        pylab.figure()
    pylab.show


# drunk1 = UsualDrunk(Drunk('UsualDrunk'))
# drunk2 = ColdDrunk(Drunk('ColdDrunk'))
# drunk3 = EDrunk(Drunk('EDrunk'))
# drunk4 = PhotoDrunk(Drunk('PhotoDrunk'))
# drunk5 = DDrunk(Drunk('DDrunk'))


simulation1(500, 800, loc)
pylab.show()




