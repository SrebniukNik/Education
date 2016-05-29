"""
Student template code for Project 4
Student will implement four functions:

build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):


"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Func for generating scoring matrix
    :param alphabet: string in uppercase without '-'
    :param diag_score: integer
    :param off_diag_score: integer
    :param dash_score: integer
    :return: dictionary with dictionaries
    '''
    matrix = {}
    alphabet = list(alphabet) + ['-']
    for row in alphabet:
        cell = {}
        for col in alphabet:
            if '-' in (row, col):
                cell[col] = dash_score
            elif row == col:
                cell[col] = diag_score
            else:
                cell[col] = off_diag_score
        matrix[row] = cell
    #matrix['-']['-'] = 0
    return matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    Func for computing alignment matrix
    :param seq_x: string in uppercase
    :param seq_y: string in uppercase
    :param scoring_matrix: Dictionary in dictionary
    :param global_flag: boolean value
    :return: 2D array with integers (scored matrix)
    '''
    x_len = len(seq_x) + 1
    y_len = len(seq_y) + 1
    matrix = [[0 for col in range(y_len)] for row in range(x_len)]
    for row in range(1, x_len):
        value = matrix[row - 1][0] + scoring_matrix[seq_x[row - 1]]['-']
        if not global_flag and value < 0:
            value = 0
        matrix[row][0] = value
    for col in range(1, y_len):
        value = matrix[0][col - 1] + scoring_matrix['-'][seq_y[col - 1]]
        if not global_flag and value < 0:
            value = 0
        matrix[0][col] = value
    #print matrix
    for row in range(1, x_len):
        for col in range(1, y_len):
            #print "row", seq_x[row], 'col', seq_y[col]
            value = max((matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]),
                        (matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-']),
                        (matrix[row][col - 1] + scoring_matrix['-'][seq_y[col - 1]]))

            # print "row, col = ", row, col, "choices of max",
            # print (matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]),
            # print (matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-']),
            # print (matrix[row][col - 1] + scoring_matrix['-'][seq_y[col - 1]])
            if not global_flag and value < 0:
                value = 0
            matrix[row][col] = value
    if not matrix:
        return [[0]]
    return matrix

def compute_global_alignment(seq_x, seq_y, score_m, align_m):
    '''
    Func for producing global alignment
    :param seq_x: string in uppercase
    :param seq_y: string in uppercase
    :param scoring_matrix: Dictionary in dictionary
    :param alignment_matrix: 2D array with integers
    :return: tuple with score with aligned seq_x and seq_y
    '''
    row = len(seq_x)
    col = len(seq_y)
    new_x = ''
    new_y = ''

    while row != 0 and col != 0:
        if align_m[row][col] == align_m[row - 1][col - 1] + score_m[seq_x[row - 1]][seq_y[col - 1]]:
            new_x = seq_x[row - 1] + new_x
            new_y = seq_y[col - 1] + new_y
            row -= 1
            col -= 1
        else:
            if align_m[row][col] == align_m[row - 1][col] + score_m[seq_x[row - 1]]['-']:
                new_x = seq_x[row - 1] + new_x
                new_y = '-' + new_y
                row -= 1
            else:
                new_x = '-' + new_x
                new_y = seq_y[col - 1] + new_y
                col -= 1
    while row != 0:
        new_x = seq_x[row - 1] + new_x
        new_y = '-' + new_y
        row -= 1
    while col != 0:
        new_x = '-' + new_x
        new_y = seq_y[col - 1] + new_y
        col -= 1
    score = sum(score_m[new_x[pos]][new_y[pos]] for pos in range(len(new_x)))
    #print new_x, new_y
    return (score, new_x, new_y)

def compute_local_alignment(seq_x, seq_y, score_m, align_m):
    '''
    Func for producing local alignment
    :param seq_x: string in uppercase
    :param seq_y: string in uppercase
    :param scoring_matrix: Dictionary in dictionary
    :param alignment_matrix: 2D array with integers
    :return: tuple with score with aligned seq_x and seq_y
    '''
    len_row = len(seq_x)
    len_col = len(seq_y)
    new_x = ''
    new_y = ''
    max_value = 0
    indexes = []
    if len_row != 0 and len_col != 0:
        for row in range(len(align_m)):
            for col in range(len(align_m[0])):
                #print "row, col", row, col
                if align_m[row][col] > max_value:
                    max_value = align_m[row][col]
                    indexes.append((row, col))
    #print "indexes", indexes, max_value
    max_idx = (0, 0)
    if indexes:
        max_idx = max(indexes)
    row, col = max_idx
    #print "max_idx", max_idx
    while align_m[row][col] != 0 and row != 0 and col != 0:
        #print "Trace begin", row, col
        if align_m[row][col] == align_m[row - 1][col - 1] + score_m[seq_x[row - 1]][seq_y[col - 1]]:
            new_x = seq_x[row - 1] + new_x
            new_y = seq_y[col - 1] + new_y
            row -= 1
            col -= 1
        else:
            if align_m[row][col] == align_m[row - 1][col] + score_m[seq_x[row - 1]]['-']:
                new_x = seq_x[row - 1] + new_x
                new_y = '-' + new_y
                row -= 1
            else:
                new_x = '-' + new_x
                new_y = seq_y[col - 1] + new_y
                col -= 1
    # while align_m[row][col] != 0 and row != 0:
    #     new_x = seq_x[row - 1] + new_x
    #     new_y = '-' + new_y
    #     row -= 1
    # while align_m[row][col] != 0 and col != 0:
    #     new_x = '-' + new_x
    #     new_y = seq_y[col - 1] + new_y
    #     col -= 1
    score = sum(score_m[new_x[pos]][new_y[pos]] for pos in range(len(new_x)))

    return (score, new_x, new_y)


def compute_local_alignment1(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequences seq_x and seq_y whose element share a common
    alphabet with the scoring matrix scoring_matrix.
    This function computes a local alignment of seq_x and seq_y using the local
    matrix alignment_matrix
    Return a tuple of the form (score, align_x, align_y) where the score is the \
    score of the optimal local alignment align_x and align_y
    '''
    score_optimal = max([max(item) for item in alignment_matrix])
    for item in alignment_matrix:
        if score_optimal in item:
            idx_y = item.index(score_optimal)
            idx_x = alignment_matrix.index(item)

    align_x = ''
    align_y = ''
    # import pdb; pdb.set_trace()
    while idx_x and idx_y:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][
            seq_y[idx_y - 1]]:
            align_x += seq_x[idx_x - 1]
            align_y += seq_y[idx_y - 1]
            # import pdb; pdb.set_trace()
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]][
                '-']:
                align_x += seq_x[idx_x - 1]
                align_y += '-'
                idx_x -= 1
                # import pdb; pdb.set_trace()
            else:
                align_x += '-'
                align_y += seq_y[idx_y - 1]
                idx_y -= 1

    # there are '-' on the tail
    # while True:
    #     try:
    #         if align_x[-1] == '-' or align_y[-1] == '-':
    #             align_x = align_x[:-1]
    #             align_y = align_y[:-1]
    #         else:
    #             break
    #     except(IndexError):
    #         break

            # The score need to recalculate, cause the length is less.
    score_updated = sum([scoring_matrix[align_x[idx]][align_y[idx]] for idx in range(len(align_x))])

    return score_updated, align_x[::-1], align_y[::-1]

def compute_global_alignment1(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequence seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix.
    This function compute a global alignment of seq_x and seq_y using the global
    alignment matrix alignment_matrix.
    Return a tuple form (score, align_x, align_y) where score is the score of
    the global alignment align_x and align_y.
    Align_x and align_y have same length.(add "-")
    '''
    score_optimal = max([max(item) for item in alignment_matrix])
    for item in alignment_matrix:
        if score_optimal in item:
            idx_y = item.index(score_optimal)
            idx_x = alignment_matrix.index(item)

    # initial the align_x and align_y, reserve it
    align_x = seq_x[idx_x:]
    align_y = seq_y[idx_y:]
    align_x = align_x[::-1]
    align_y = align_y[::-1]
    while idx_x and idx_y:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][
            seq_y[idx_y - 1]]:
            align_x += seq_x[idx_x - 1]
            align_y += seq_y[idx_y - 1]
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]][
                '-']:
                align_x += seq_x[idx_x - 1]
                align_y += '-'
                idx_x -= 1
                # import pdb; pdb.set_trace()
            else:
                align_x += '-'
                align_y += seq_y[idx_y - 1]
                idx_y -= 1
    while idx_x:
        align_x += seq_x[idx_x - 1]
        align_y += '-'
        idx_x -= 1
    while idx_y:
        align_x += '-'
        align_y += seq_y[idx_y - 1]
        idx_y -= 1

    # reserve the string
    align_x = align_x[::-1]
    align_y = align_y[::-1]

    # align_x and align_y have same length
    length_x = len(align_x)
    length_y = len(align_y)
    if length_x < length_y:
        align_x += '-' * (length_y - length_x)
    else:
        align_y += '-' * (length_x - length_y)

    # The score need to recalculate, cause there may be '-' more
    score_updated = sum([scoring_matrix[align_x[idx]][align_y[idx]] for idx in range(len(align_x))])

    return score_updated, align_x, align_y

#Homework4 - Solving quiz
#Question 12 and 13
# scoring_matrix = build_scoring_matrix('ACTG', 10, 4, -6)
# print scoring_matrix
# align = compute_alignment_matrix('AA', 'TAAT', scoring_matrix, False)
#Question 14
#print align
#print align[0][2], align[2][0], align[2][2]
#Question 15
#print compute_local_alignment('AA', 'TAAT', scoring_matrix, align)

######MANUAL TESTING

#######Func1 build_scoring_matrix - Manual testing
#scoring_matrix = build_scoring_matrix('ACTUG', 10, 5, -5)
#print compute_alignment_matrix('A', 'CTGAG', scoring_matrix, False)

#######Func2 compute_alignment_matrix - Manual testing
# print compute_alignment_matrix('ATG', 'ACG', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#                                               'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
#                                               '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#                                               'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
#                                               'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}},
#                                True)
#expected [[0, -4, -8, -12], [-4, 6, 2, -2], [-8, 2, 8, 4], [-12, -2, 4, 14]]
# but received [[0, -4, -4, -4], [-4, 6, 2, -2], [-4, 2, 8, 4], [-4, -2, 4, 14]]


# result = compute_alignment_matrix('ACTACT', 'AGCTA', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
#                                              'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
#                                              '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
#                                              'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
#                                              'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}},
#                          True)
# print "Result", result
#print "\nExpect [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]]"
#expected [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]]
#but received (Exception: IndexError) "list index out of range" at line 49, in compute_alignment_matrix


#print build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
#expected {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}

# print compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#                                           'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
#                                           '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#                                           'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
#                                           'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}},
#                                 False)
#######Func3 compute_global_alignment - Manual testing
# print compute_global_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#                                       'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
#                                       '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#                                       'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
#                                       'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]])
#print compute_global_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]])
#returned incorrect score, expected 6 but received 0

#print compute_global_alignment('G', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, -4], [-4, 6]])
#returned incorrect score, expected 6 but received 0

#######Func4 compute_local_alignment - Manual testing
#print compute_local_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]])
#expected ({'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, 0, '', '', False)

# print compute_local_alignment('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#                                          'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
#                                          '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#                                          'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
#                                          'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, 0], [0, 6]])
#returned incorrect score, expected 6 but received 0

# print compute_local_alignment('ACTACT', 'AGCTA', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
#                                             'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
#                                             '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
#                                             'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
#                                             'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}},
#                         [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6],
#                          [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]])
#expected ({
# 'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
# 'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
# '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
# 'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
# 'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}, 8, 'ACTACT', 'AGCTA', False)
#but received (Exception: IndexError) "list index out of range" at line 193, in compute_local_alignment
