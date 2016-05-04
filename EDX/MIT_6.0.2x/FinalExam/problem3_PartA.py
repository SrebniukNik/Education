import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 50
CURRENTFOXPOP = 300

def rabbitGrowth():
    """
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up,
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    rabbit_range = range(CURRENTRABBITPOP)
    for rabbit in rabbit_range:
        if 10 < CURRENTRABBITPOP < 1000:
            if random.random() < (1.0 - (CURRENTRABBITPOP / float(MAXRABBITPOP))):
                CURRENTRABBITPOP += 1
    #print "CURRENTRABBITPOP", CURRENTRABBITPOP


def foxGrowth():
    """
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    fox_range = range(CURRENTFOXPOP)

    for fox in fox_range:
        if CURRENTRABBITPOP > 10 and random.random() < (CURRENTRABBITPOP / float(MAXRABBITPOP)):
            CURRENTRABBITPOP -= 1
            if random.random() < 1/3.0:
                CURRENTFOXPOP += 1
        elif CURRENTFOXPOP > 10 and random.random() < 0.9:
            CURRENTFOXPOP -= 1

    #print "CURRENTFOXPOP", CURRENTFOXPOP

def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    rabbit_sim = []
    fox_sim = []
    for step in range(numSteps):
        rabbitGrowth()
        rabbit_sim.append(CURRENTRABBITPOP)
        foxGrowth()
        fox_sim.append(CURRENTFOXPOP)
    print "CURRENTRABBITPOP", CURRENTRABBITPOP, rabbit_sim
    print "CURRENTFOXPOP", CURRENTFOXPOP, fox_sim
    return rabbit_sim, fox_sim

def runSimulation1(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    rabbit_sim = []
    fox_sim = []
    for step in range(numSteps):
        rabbitGrowth()
        rabbit_sim.append(CURRENTRABBITPOP)
        foxGrowth()
        fox_sim.append(CURRENTFOXPOP)
    #print "CURRENTRABBITPOP", CURRENTRABBITPOP
    #print "CURRENTFOXPOP", CURRENTFOXPOP
    pylab.plot(range(numSteps), rabbit_sim, '-g', label='Rabbit population')
    pylab.plot(range(numSteps), fox_sim, '-o', label='Fox population')
    pylab.title('Fox and rabbit population in the wood')
    xlabel = "Plot for simulation of {} steps".format(numSteps)
    pylab.xlabel(xlabel)
    pylab.ylabel('Current fox and rabbit population')
    pylab.legend(loc='upper right')
    pylab.tight_layout()
    pylab.show()
    pylab.clf()


def runSimulation2(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    rabbitPopulationOverTime = []
    foxPopulationOverTime = []
    for step in range(numSteps):
        rabbitGrowth()
        rabbitPopulationOverTime.append(CURRENTRABBITPOP)
        foxGrowth()
        foxPopulationOverTime.append(CURRENTFOXPOP)
    print "CURRENTRABBITPOP", CURRENTRABBITPOP, rabbitPopulationOverTime
    print "CURRENTFOXPOP", CURRENTFOXPOP, foxPopulationOverTime
    pylab.plot(range(numSteps), rabbitPopulationOverTime, '-g', label='Rabbit population')
    pylab.plot(range(numSteps), foxPopulationOverTime, '-o', label='Fox population')
    rabbit_coeff = pylab.polyfit(range(len(rabbitPopulationOverTime)), rabbitPopulationOverTime, 2)
    pylab.plot(pylab.polyval(rabbit_coeff, range(len(rabbitPopulationOverTime))))
    fox_coeff = pylab.polyfit(range(len(foxPopulationOverTime)), foxPopulationOverTime, 2)
    pylab.plot(pylab.polyval(fox_coeff, range(len(rabbitPopulationOverTime))))
    pylab.title('Fox and rabbit population in the wood')
    xlabel = "Plot for simulation of {} steps".format(numSteps)
    pylab.xlabel(xlabel)
    pylab.ylabel('Current fox and rabbit population')
    pylab.legend(loc='upper right')
    pylab.tight_layout()
    pylab.show()
    pylab.clf()


runSimulation2(200)