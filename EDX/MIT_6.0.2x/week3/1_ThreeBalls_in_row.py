def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3
    balls of the same color were drawn.
    '''
    count = 0
    for trial in range(numTrials):
        same_balls = 0
        bucket = [1,1,1,0,0,0]
        for ball in range(3):
            ball_number = random.choice(range(len(bucket)))
            same_balls += bucket.pop(ball_number)

        if same_balls == 3 or same_balls == 0:
            count +=1

    return count/float(numTrials)