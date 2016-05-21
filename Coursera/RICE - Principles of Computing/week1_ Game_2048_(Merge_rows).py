"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    #Step1. Putting 0 to the end of the list.
    result = []
    for cell in line:
        if cell != 0:
            result.append(cell)
    for cell in range(line.count(0)):
        result.append(0)
    #Step2. Replaced with a tile of twice the value and a zero tile
    for cell in range(len(result)-1):
        if result[cell] == result[cell+1] and len(result) != 1:
            result[cell] += result[cell]
            result[cell+1] = 0
    #Step3. Repeat step1
    final_result = []
    for cell in result:
        if cell != 0:
            final_result.append(cell)
    for cell in range(result.count(0)):
        final_result.append(0)
    return final_result

print merge([2, 0, 2, 4]) # [4, 4, 0, 0]
print merge([0, 0, 2, 2]) # [4, 0, 0, 0]
print merge([2, 2, 0, 0]) # [4, 0, 0, 0]
print merge([2, 2, 2, 2, 2]) # [4, 4, 2, 0, 0]
print merge([8, 16, 16, 8]) # [8, 32, 8, 0]
print merge([4]) # [8, 32, 8, 0]
