import random, pylab

xVals = []
yVals = []
wVals = []
for i in range(1000):
    xVals.append(random.random())
    yVals.append(random.random())
    wVals.append(random.random())
xVals = pylab.array(xVals)
yVals = pylab.array(yVals)
wVals = pylab.array(wVals)

xVals = xVals + xVals
zVals = xVals + yVals
tVals = xVals + yVals + wVals


def plotting(vals, name):
    pylab.plot(vals)
    label = name
    pylab.title(label)
    pylab.xlabel('Amount of vals')
    pylab.ylabel('Vals count')


def plotting2(vals, name):
    pylab.figure()
    pylab.hist(vals, bins=10)
    pylab.title(name)
    pylab.xlabel('Amount of vals')
    pylab.ylabel('Vals count')

# plotting(xVals, "tVals distribution")
# plotting2(xVals, "tVals distribution")

pylab.plot(sorted(xVals), sorted(yVals))


pylab.show()
