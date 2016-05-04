import random

def drawing_without_replacement_sim(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns a float - the fraction of times 3
    balls of the same color were drawn in the first 3 draws.
    '''
    count = 0
    busket = ['r', 'g'] * 4
    print busket
    for trial in range(numTrials):
        busket_copy = busket[:]
        choices = []
        for n in range(3):
            choice = random.randrange(0, len(busket_copy))
            choices.append(busket_copy.pop(choice))
        if choices.count('r') == 3 or choices.count('g') == 3:
            count += 1
    return round(float(count)/numTrials, 2)

print drawing_without_replacement_sim(1000000)


