# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

#from ps3b_precompiled_27 import *
''' 
Begin helper code
'''

#set line width
pylab.rcParams['lines.linewidth'] = 7
#set font size for titles
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.major.size'] = 5
#set size of numbers on y-axis
pylab.rcParams['ytick.major.size'] = 5

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return True if random.random() < self.getClearProb() else False


    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if random.random() < self.getMaxBirthProb() * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            NoChildException()


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """
        virus_servived = []
        for virus in self.viruses:
            if not virus.doesClear():
                virus_servived.append(virus)

        self.viruses = virus_servived[:]
        density = len(virus_servived)/float(self.getMaxPop())
        try:
            for virus in virus_servived:
                if len(self.viruses) <= self.maxPop:
                    new_virus = virus.reproduce(density)
                    if new_virus:
                        self.viruses.append(new_virus)
        except NoChildException:
            pass

        return len(self.viruses)

# v1 = SimpleVirus(1.0, 0.0)
# #print v1.doesClear()
# #print v1.reproduce(0.05)
# patient = Patient([v1], 100)
#
# for n in range(100):
#     print
#     patient.update()
#
# print len(patient.viruses)

#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    virus = SimpleVirus(maxBirthProb, clearProb)
    flue = [virus] * numViruses
    virus_total = [0]*300
    for trial in range(numTrials):
        patient = Patient(flue, maxPop)
        for step in range(300):
            patient.update()
            virus_total[step] += float(patient.getTotalPop())

        # for step in range(300):
        #     virus_total[step] /= 300.0
        #print virus_total
        pylab.plot(virus_total, 'ro', label = 'SimpleVirus simulation')
        pylab.title('SimpleVirus simulation')
        pylab.xlabel('Time Steps')
        pylab.ylabel('Average Virus Population')
        pylab.legend()
        pylab.show()


#simulationWithoutDrug(100, 1000, 0.1, 0.05, 10)


# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self,maxBirthProb,clearProb)
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances.keys():
            return True if self.resistances[drug] else False
        else:
            NoChildException()


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # print "popDensity", popDensity
        # print "activedrugs", activeDrugs
        reproducible = 0
        repr_prob = 0
        for drug in activeDrugs:
            if drug in self.resistances.keys() and self.resistances[drug]:
                reproducible += 1
        #print "reproducible", reproducible

        if activeDrugs and reproducible == 0:
            NoChildException()
        elif reproducible == 1 and len(activeDrugs) > 1:
            NoChildException()
        else:
            repr_prob = self.maxBirthProb * (1 - popDensity)

        if random.random() < repr_prob:
            inherit_resist = self.resistances.copy()
            if not activeDrugs:
                activeDrugs = inherit_resist.keys()
            for drug in activeDrugs:
                #print "inital virus", self.isResistantTo(drug)
                if drug in inherit_resist.keys():
                    #print inherit_resist[drug]
                    if inherit_resist[drug] and random.random() < self.mutProb:
                        inherit_resist[drug] = False
                    elif not inherit_resist[drug] and random.random() < self.mutProb:
                        inherit_resist[drug] = True
                    #print "Final virus", self.isResistantTo(drug)

            return ResistantVirus(self.maxBirthProb, self.clearProb, inherit_resist, self.mutProb)
        else:
            NoChildException()



class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        virus_resust = 0

        for virus in self.viruses:
            drugs_resist = 0
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    drugs_resist += 1
            if drugs_resist == len(drugResist):
                virus_resust += 1
            # print "checking drug", drug, "|", virus.isResistantTo(drug)
        return virus_resust


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        virus_servived = []
        for virus in self.viruses:
            if not virus.doesClear():
                virus_servived.append(virus)

        self.viruses = virus_servived[:]
        density = len(virus_servived) / float(self.getMaxPop())
        try:
            for virus in virus_servived:
                if len(self.viruses) <= self.maxPop:
                    new_virus = virus.reproduce(density, self.drugs)
                    if new_virus:
                        self.viruses.append(new_virus)
        except NoChildException:
            pass

        return len(self.viruses)




def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, testesSteps):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """



    # pylab.plot(virus_treated, 'go', label='ResistantVirus simulation')
    # pylab.title('ResistantVirus simulation')
    # pylab.xlabel('time step')
    # pylab.ylabel('# viruses')
    # pylab.legend()
    # pylab.show()



#virus = ResistantVirus(1.0, 0.0, {"drug1":True, "drug2":False}, 0.0)
#virus = ResistantVirus(1.0, 0.0, {"drug1":True}, 0.0)
#virus = ResistantVirus(1.0, 0.0, {"drug2": True}, 1.0)
#virus = ResistantVirus(1.0, 0.0, {'drug1':True, 'drug2': True, 'drug3': True, 'drug4': True, 'drug5': True, 'drug6': True}, 0.5)
#child = virus.reproduce(0, ["drug2"])
#child1 = virus.reproduce(0, ["drug1"])
#print virus.maxBirthProb
# print "1", child
# print "2", child1
# viruses = []
# for n in range(100):
#     child = virus.reproduce(0, ["drug2"])
#     print "child", child.resistances["drug2"]
#     viruses.append(child)
#
# print viruses
# count = 0
# for vir in viruses:
#     print "Virus #", count, "Resistent to drug2", vir.resistances["drug2"]
#     count += 1
#print len(viruses)
############################################################################33
# viruses = []
# virus = ResistantVirus(1.0, 0.0, {'drug1':True, 'drug2': True, 'drug3': True, 'drug4': True, 'drug5': True, 'drug6': True}, 0.5)
# for n in range(10):
#     child = virus.reproduce(0, [])
#     #print "child", child.resistances["drug2"]
#     viruses.append(child)
#
# count = 0
# for vir in viruses:
#     for drug in vir.resistances.keys():
#         print "Virus #", count, "Resistent to ", drug, " - ", vir.resistances[drug]
#     count += 1
# print len(viruses)
#
# virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
# virus2 = ResistantVirus(1.0, 0.0, {"drug1": False, "drug2": True}, 0.0)
# virus3 = ResistantVirus(1.0, 0.0, {"drug1": True, "drug2": True}, 0.0)
# patient = TreatedPatient([virus1, virus2, virus3], 100)
# print patient.getResistPop(['drug1'])
# print patient.getResistPop(['drug2'])
# print patient.getResistPop(['drug1','drug2'])
# print patient.getResistPop(['drug3'])
# print patient.getResistPop(['drug1', 'drug3'])
# print patient.getResistPop(['drug1','drug2', 'drug3'])