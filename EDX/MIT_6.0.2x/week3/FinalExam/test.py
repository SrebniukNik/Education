import numpy
import random
import matplotlib.pyplot as plt
from ps3b import *

def totPopFinal(numSteps):

    conditions={"condA":300, "condB":150, "condC":75, "condD":0} #num Steps Delay
    resistances={'guttagonol': False}

    virus=ResistantVirus(0.1, 0.05, resistances, 0.005)
    virusLi=[virus for virus_id  in range(100) ]
    treatedJohn=TreatedPatient(virusLi, 1000)
    counter=1

    while counter <= numSteps:
        treatedJohn.update()
        counter+=1

    treatedJohn.addPrescription("guttagonol")
    counter2=1
    while counter2 <= 150:  #NumStepsAfter
        treatedJohn.update()
        counter2+=1
    return treatedJohn.getTotalPop()

def makePlot(values, title, style, xLabel="Final Virus Pop", yLabel="Num Trials/Bin", binNum=10,  ):
    plt.figure()
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.hist(values, bins=binNum, color=style)


def simulationDelayedTreatment(numTrials):
    ''' Run simulations and make histograms for problem 1'''

    #numStepsAfter=150
    conditions={"condA":300, "condB":150, "condC":75, "condD":0} #num Steps Delay
    resistances={'guttagonol': False}

    virus=ResistantVirus(0.1, 0.05, resistances, 0.005)
    virusLi=[virus for virus_id  in range(100) ]




    TotpopCondA=[totPopFinal(300) for i in range (numTrials)]
    TotpopCondB=[totPopFinal(150) for i in range (numTrials)]
    TotpopCondC=[totPopFinal(75) for i in range (numTrials)]
    TotpopCondD=[totPopFinal(0) for i in range (numTrials)]

    #     for i in conditions:
    #         for trial in range(numTrials):
    #             totPopDic={i: totPopFinal(conditions[i]) for trial in range(numTrials)}

    #return totPopDic


    makePlot(TotpopCondA, "Final Population-300 steps Witout", "b")
    makePlot(TotpopCondB, "Final Population-150 steps Witout","r")
    makePlot(TotpopCondC, "Final Population-75 steps Witout", "y" )
    makePlot(TotpopCondD, "Final Population-0 steps Witout", "g")


simulationDelayedTreatment(10)

plt.show()