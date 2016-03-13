def f(x):
    import math
    return 200*math.e**(math.log(0.5)/14.1 * x)

def radiationExposure(start, stop, step):
  '''
  Computes and returns the amount of radiation exposed
  to between the start and stop times. Calls the
  function f (defined for you in the grading script)
  to obtain the value of the function at any point.

  start: integer, the time at which exposure begins
  stop: integer, the time at which exposure ends
  step: float, the width of each rectangle. You can assume that
    the step size will always partition the space evenly.

  returns: float, the amount of radiation exposed to
    between start and stop times.
  '''
  # measure = 0
  # while start != stop:
  #   measure += f(start) * step
  #   start += step
  # return measure
  measure = 0
  if start >= stop:
    print "start", start
    #measure += f(start)
    return measure
  else:
    print "start", start
    print "f(", start, ")=", f(start) * 0.1
    measure += f(start) * step + radiationExposure(start+step, stop, step)
    print "measure", measure
    return measure

print radiationExposure(0, 3, 0.1)

