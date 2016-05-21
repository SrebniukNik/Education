"""
Student template code for Project 4
Student will implement four functions:

build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):


"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Func for gennerating scoring matrix
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

    :param seq_x:
    :param seq_y:
    :param scoring_matrix:
    :param global_flag:
    :return:
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

#scoring_matrix = build_scoring_matrix('ACTUG', 10, 5, -5)

#print compute_alignment_matrix('A', 'CTGAG', scoring_matrix, False)


# print compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#                                           'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
#                                           '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#                                           'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
#                                           'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}},
#                                 False)

# #expected [[0, -4], [-4, 6]] but received [[2]]
#
# print compute_alignment_matrix('ATG', 'ACG', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#                                               'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
#                                               '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#                                               'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
#                                               'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}},
#                                True)

#expected [[0, -4, -8, -12], [-4, 6, 2, -2], [-8, 2, 8, 4], [-12, -2, 4, 14]]
# but received [[0, -4, -4, -4], [-4, 6, 2, -2], [-4, 2, 8, 4], [-4, -2, 4, 14]]

#
# result = compute_alignment_matrix('ACTACT', 'AGCTA', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
#                                              'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
#                                              '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
#                                              'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
#                                              'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}},
#                          True)
# print "Result", result
# print "\nExpect [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]]"
#expected [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]]
#but received (Exception: IndexError) "list index out of range" at line 49, in compute_alignment_matrix


#print build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)

#expected {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}