def nfruits(fruits, eats):
    """
    Func for counting eated fruits by Python
    """
    for i in range(len(eats)):
        for key in fruits.iterkeys():
            if key == eats[i]:
                fruits[key] -= 1
            elif i != (len(eats) - 1):
                fruits[key] += 1

    return max(fruits.values())

def nfruits1(fruits, note):
    """
    fruits: dictionary of different types of fruits with quantities
    note: string of eated fruits

    returns: integer, maximum number of stayed fruits
    """
    for fruitIdx in range(len(note)):
        fruit = note[fruitIdx]
        fruits[fruit] -= 1
        # Nothing buy if reached campus
        if fruitIdx != len(note) - 1:
            for fruitKey in fruits:
                if fruitKey != fruit:
                    fruits[fruitKey] += 1
    return max(fruits.values())



print nfruits({'A': 1, 'B': 2, 'C': 3}, 'AC')

print nfruits1({'A': 1, 'B': 2, 'C': 3}, 'AC')