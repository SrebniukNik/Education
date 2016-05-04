# 6.00.2x Problem Set 4

import numpy
import random
import pylab
#from ps3b import *
from ps3b_precompiled_27 import *
#
# PROBLEM 1
#

def simulationOneDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, testedSteps):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    flue = [virus] * numViruses
    total_steps = 150 + testedSteps
    patient = TreatedPatient(flue, maxPop)
    for step in range(total_steps):
        patient.update()
        if step == testedSteps:
            patient.addPrescription('guttagonol')
    #print "Population", patient.getTotalPop()
    return patient.getTotalPop()

#Created plotted figures
def plothistOneDrug(topViruses, steps):
    pylab.figure()
    pylab.hist(topViruses, bins=10)
    label = 'ResistantVirus simulation ' + str(steps) + ' steps'
    pylab.title(label)
    pylab.xlabel('histogram bins')
    pylab.ylabel('number of trials')



def simulationDelayedTreatment(numTrials):

    steps = [300, 150, 75, 0]

    x = [0] * len(steps)

    for step in range(len(steps)):
        x[step] = [0] * numTrials
        for trial in range(numTrials):
            result = simulationOneDrug(100, 1000, 0.1, 0.05, {'guttagonol': True}, 0.005, steps[step])
            x[step][trial] = result
            print "Step =", step, "trial =", trial, ". Result =", result

    for simu in range(len(steps)):
        plothistOneDrug(x[simu], steps[simu])

# simulationDelayedTreatment(100)
# pylab.show()



#
# PROBLEM 2
#
def simulationTwoDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances,
               mutProb, testedSteps):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    flue = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for virus in range(numViruses)]
    #print "total_viruses", len(flue), flue
    total_steps = 300 + testedSteps
    patient = TreatedPatient(flue, maxPop)
    for step in range(total_steps):
        patient.update()
        if step == 149:
            patient.addPrescription('guttagonol')
        if step == testedSteps + 149:
            patient.addPrescription('grimpex')
    print "Population", patient.getTotalPop()
    return patient.getTotalPop()


# Created plotted figures
def plothistTwoDrugs(topViruses, steps):
    pylab.figure()
    pylab.hist(topViruses, bins=10)
    label = 'ResistantVirus simulation of 2 drugs ' + str(steps) + ' steps'
    pylab.title(label)
    pylab.xlabel('histogram bins')
    pylab.ylabel('number of trials')


def simulationTwoDrugsDelayedTreatment(numTrials):
    #steps = [300, 150, 75, 0]
    steps = [0.005, 0.02, 0.08, 0.32]
    steps = [75, 75, 75, 75]
    #steps = [300, 150, 75, 0]

    x = [0] * len(steps)

    for step in range(len(steps)):
        x[step] = [0] * numTrials
        for trial in range(numTrials):
            #def simulationTwoDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances,mutProb, testedSteps):
            #result = simulationTwoDrugs(100, 1000, 0.1, 0.05, {'guttagonol':False, 'grimpex':False}, steps[step], 300)
            result = simulationTwoDrugs(100, 1000, 0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.005, steps[step])
            #result = simulationTwoDrugs(100, 1000, 0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.005, steps[step])
            x[step][trial] = result
            print "Step =", step, "trial =", trial, ". Result =", result

    for simu in range(len(steps)):
        plothistTwoDrugs(x[simu], steps[simu])

simulationTwoDrugsDelayedTreatment(100)
pylab.show()
