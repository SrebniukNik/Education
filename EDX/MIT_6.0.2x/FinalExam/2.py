n = ([0,1,2,3,4,5,6,7,8], [5,10,10,10,15], [0,1,2,4,6,8], [6,7,11,12,13,15], [9,0,0,3,3,3,6,6])

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5, mean

def possible_mean(L):
    return sum(L)/len(L)

def possible_variance(L):
    mu = possible_mean(L)
    temp = 0
    for e in L:
        temp += (e-mu)**2
    return temp / len(L)

for m in n:
    print possible_variance(m), "list", m

