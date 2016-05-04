import random, pylab

# You are given this function


# You are given this class
class Die(object):
    def __init__(self, valList):
        """ valList is not empty """
        self.possibleVals = valList[:]
    def roll(self):
        return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
    """
      - values, a sequence of numbers
      - numBins, a positive int
      - xLabel, yLabel, title, are strings
      - Produces a histogram of values with numBins bins and the indicated labels
        for the x and y axis
      - If title is provided by caller, puts that title on the figure and otherwise
        does not title the figure
    """
    pylab.hist(values, bins=numBins)
    if title:
        pylab.title(title)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    pylab.show()

#makeHistogram([1,2], 4, "Aaa", "Bbb", 'mumu')

# Implement this -- Coding Part 2 of 2
# def getAverage(die, numRolls, numTrials):
#     """
#       - die, a Die
#       - numRolls, numTrials, are positive ints
#       - Calculates the expected mean value of the longest run of a number
#         over numTrials runs of numRolls rolls
#       - Calls makeHistogram to produce a histogram of the longest runs for all
#         the trials. There should be 10 bins in the histogram
#       - Choose appropriate labels for the x and y axes.
#       - Returns the mean calculated
#     """
#     total = []
#     dieTemplate = Die(range(1,7))
#     roll_len = len(die.possibleVals)
#     print roll_len
#     for trial in range(numTrials):
#         count = 0
#         for roll in range(numRolls):
#             new_roll = [0] * roll_len
#             for res in range(roll_len):
#                 new_roll[res] = dieTemplate.roll()
#             print new_roll
#             if new_roll == die.possibleVals:
#                 count += 1
#         total.append(count)
#         print "trial", trial, " count", count
#     mean, std = getMeanAndStd(total)
#     return mean


# One test case
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# Implement this -- Coding Part 2 of 2
def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number of dice roll
        over numTrials runs of numRolls rolls
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """
    total = []
    for trial in range(numTrials):
        roll = []
        for dice in range(numRolls):
            roll.append(die.roll())
        #print "Non-Sorted roll", roll
        longest = []
        same = 1
        for num in range(len(roll)-1):
            if roll[num] == roll[num+1]:
                same += 1
            else:
                longest.append(same)
                same = 1
        longest.append(same)
        #print "Max run", max(longest)
        total.append(max(longest)),
        #print "trial", trial, " Longest run", total[-1]
    mean, std = getMeanAndStd(total)
    makeHistogram(total, 10, "Trials", "Max run")
    return mean


#print getAverage(Die([1,2,3,4,5,6,6,6,7]), 10, 10)
print getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000)