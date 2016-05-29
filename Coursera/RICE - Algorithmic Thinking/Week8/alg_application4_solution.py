"""
Code and solution for Application 4
"""
import difflib
from alg_application4_provided import *
from alg_project4_solution import *
import matplotlib.pyplot as plt
import math
import string

def question1(filename_type, global_flag=False):
    '''
    Func for computing local alignment
    :param filename_type: string ('file' or 'URL')
    :return: None
    '''
    if filename_type == 'file':
        human_protein = read_protein_file(HUMAN_EYELESS_FILE)
        fruitfly_protein = read_protein_file(FRUITFLY_EYELESS_FILE)
        score_matrix = read_scoring_matrix_file(PAM50_FILE)
    elif filename_type == 'URL':
        human_protein = read_protein_file(HUMAN_EYELESS_URL)
        fruitfly_protein = read_protein_file(FRUITFLY_EYELESS_URL)
        score_matrix = read_scoring_matrix_file(PAM50_URL)
    # print human_protein
    # print fruitfly_protein
    # print score_matrix
    align_matrix = compute_alignment_matrix(human_protein, fruitfly_protein, score_matrix, global_flag)
    local_alignment = compute_local_alignment(human_protein, fruitfly_protein, score_matrix, align_matrix)
    file = open('question1_result.txt', 'wb')
    # for line in local_alignment[:-1]:
    #     file.write(str(line)+"\n")
    # for line in local_alignment[-1]:
    #     file.write(str(line))
    print "Local alignment"
    print "Score:", local_alignment[0]
    print "Human genomm local alignments:", local_alignment[1]
    print "FruitEyeless local_alignments:", local_alignment[2]
    print "-" * 80 * 2
    return local_alignment

def question2(filename_type, input_seq):
    '''
    Func for resolving Question 2.
    :param result:
    :return:
    '''
    if filename_type == 'file':
        consensus_pax = read_protein_file(CONSENSUS_PAX_FILE)
        score_matrix = read_scoring_matrix_file(PAM50_FILE)
    elif filename_type == 'URL':
        consensus_pax = read_protein_file(CONSENSUS_PAX_URL)
        score_matrix = read_scoring_matrix_file(PAM50_URL)
    seq = input_seq.replace('-', '')
    print "Seq without -: ", seq, "len", len(seq)
    print "PAX domain   : ", consensus_pax, "len", len(consensus_pax)
    align_matrix = compute_alignment_matrix(seq, consensus_pax, score_matrix, global_flag=True)
    score, global_alignment, global_align_pax = compute_global_alignment(seq, consensus_pax, score_matrix, align_matrix)
    print "Global score    :", score
    print "global_alignment:", global_alignment, "len", len(global_alignment)
    print "global_align_pax:", global_align_pax, "len", len(global_align_pax)
    count = 0
    for num in range(len(global_alignment)):
        if global_alignment[num] == global_align_pax[num]:
            count += 1
    #percentage = difflib.SequenceMatcher(None, global_alignment, global_align_pax)
    #return percentage.ratio()
    return float(count) / len(global_alignment)

def generate_null_distribution(seq_x, seq_y, score_matrix, num_trials):
    '''

    :param seq_x:
    :param seq_y:
    :param scoring_matrix:
    :param num_trials:
    :return:
    '''
    result = {}
    seq_copy = seq_y
    for trial in range(num_trials):

        seq_copy = list(seq_copy)
        random.shuffle(seq_copy)
        shuffled_seq_copy = ''
        shuffled_seq_copy = shuffled_seq_copy.join(seq_copy)
        print "Trial started #", trial #, "shuffle", shuffled_seq_copy
        align_matrix = compute_alignment_matrix(seq_x, shuffled_seq_copy, score_matrix, False)
        local_score, local_human_alignment, local_fruitfly_alignment = compute_local_alignment(seq_x, shuffled_seq_copy,
                                                                                               score_matrix, align_matrix)
        if result.has_key(local_score):
            result[local_score] += 1
        else:
            result[local_score] = 1

    return result



def question4(filename_type, num_trials, global_flag, file_to_save):
    '''
    Func for computing local alignment
    :param filename_type: string ('file' or 'URL')
    :return: None
    '''
    if filename_type == 'file':
        human_protein = read_protein_file(HUMAN_EYELESS_FILE)
        fruitfly_protein = read_protein_file(FRUITFLY_EYELESS_FILE)
        score_matrix = read_scoring_matrix_file(PAM50_FILE)
    elif filename_type == 'URL':
        human_protein = read_protein_file(HUMAN_EYELESS_URL)
        fruitfly_protein = read_protein_file(FRUITFLY_EYELESS_URL)
        score_matrix = read_scoring_matrix_file(PAM50_URL)
    result = generate_null_distribution(human_protein, fruitfly_protein, score_matrix, num_trials)
    print result
    trials = []
    scores = []
    for key, value in result.iteritems():
        print float(value)/num_trials, round(float(value)/num_trials, 3)
        trials.append(float(value)/num_trials)
        scores.append(key)
    #width = 1 / 1.5
    plt.bar(scores, trials, color="blue", label="Score distribution")
    plt.title('Null distribution for hypothesis testing using 1000 trials')
    plt.xlabel('Scores')
    plt.ylabel('Fraction of trials')
    plt.legend(loc='upper right')
    plt.tight_layout()
    if file_to_save:
        plt.savefig(file_to_save)
    plt.clf()
    return result

def question5(result, ntrials, score_of_local_alignment):
    '''

    :param filename_type:
    :param num_trials:
    :param global_flag:
    :param file_to_save:
    :return:
    '''
    values = []
    for key, value in result.iteritems():
        values.extend([key]*value)
    print len(values), values

    mean = sum(values) / float(len(values))
    sigma = math.sqrt(sum(math.pow((value - mean), 2) for value in values) / float(ntrials))
    z_score = (score_of_local_alignment - mean) / sigma
    print "Standart mean  is {0} and deviation is {1}".format(mean, sigma)
    print "Likelihood of the score s being a product of chance {0}".format(z_score)


def question7(ntrials, human_seq, fruit_fly):
    '''

    :return:
    '''

    for diag_score in range(ntrials):
        for off_diag_score in range(ntrials):
            for dash_score in range(ntrials):

                score_matrix = build_scoring_matrix(string.ascii_lowercase, diag_score, off_diag_score, dash_score)
                align_matrix = compute_alignment_matrix(human_seq, fruit_fly, score_matrix, global_flag=False)
                score, global_alignment, global_align_pax = compute_global_alignment(human_seq, fruit_fly, score_matrix,
                                                                                     align_matrix)
                dist = len(human_seq) + len(fruit_fly) - score
                if diag_score > off_diag_score > dash_score:
                    print "\ndiag_score, off_diag_score, dash_score = (", diag_score, off_diag_score, dash_score, ")"
                    print "Edit distance VS score", score, "<>", dist
                    return diag_score, off_diag_score, dash_score

def check_spelling(checked_word, dist, word_list, scores):
    '''

    :param checked_word:
    :param dist:
    :param word_list:
    :return:
    '''
    diag_score, off_diag_score, dash_score = scores
    score_matrix = build_scoring_matrix(string.ascii_lowercase, diag_score, off_diag_score, dash_score)
    result = []
    len1 = len(checked_word)
    for word in word_list:
        align_matrix = compute_alignment_matrix(checked_word, word, score_matrix, global_flag=False)
        score, global_alignment, global_align_pax = compute_global_alignment(checked_word, word, score_matrix,
                                                                             align_matrix)
        computed_distance = len1 + len(word) - score
        if computed_distance in (dist, 0):
            result.append(word)
    sorted(result)
    print "set of words within an edit distance for word ", checked_word,
    print result
    return result

def question8(filename_type, checked_word, dist, scores):
    '''

    :param filename_type:
    :param num_trials:
    :param global_flag:
    :param file_to_save:
    :return:
    '''
    if filename_type == 'file':
        word_list = read_words_file(WORD_LIST_FILE)
    elif filename_type == 'URL':
        word_list = read_words_url(WORD_LIST_URL)
    return check_spelling(checked_word, dist, word_list, scores)




def main():
    '''

    :return:
    '''
    ####Question1####
    #Please enter source for input data: 'file' or 'url, and global_flag type for alignment computation
    #question1('file', False)
    #Answer
    '''
    Score - 875
    Human aligned sequence: HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ
    FruitFly aligned sequence: HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ
    '''
    ####Question2####
    #result = question1('file', False)

    # result = ('','HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ',
    #              'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ')
    #print question2('file', result[1])
    #print question2('file', result[2])
    #Answer on Question2
    '''
    Ratio of global alignment for Human    vs. consensus PAX domain:  72,3308271%
    Ratio of global alignment for fruitfly vs. consensus PAX domain:  70,1492537313%
    '''
    ####Question3####
    # Answer on Question3
    '''
    The possibility of similarity Human or Fruitfly sequence with PAX domain sequence is 1 from 23 ^ 133 where
    23 is a 23 possible amino acids ("ACBEDGFIHKMLNQPSRTWVYXZ")
    133 - length of global aligned sequence
    Conclusion: similarity is not due to chance. Its due to mutation from parent genom.
    '''
    ###Question 4.
    #result_scores = question4(filename_type='file', num_trials=1000, global_flag=False, file_to_save='question4_4.png')
    #Output: result0 = {36: 8, 37: 10, 38: 12, 39: 22, 40: 26, 41: 41, 42: 51, 43: 53, 44: 65, 45: 61, 46: 66, 47: 75, 48: 65, 49: 70, 50: 48, 51: 42, 52: 38, 53: 35, 54: 31, 55: 33, 56: 25, 57: 19, 58: 13, 59: 8, 60: 13, 61: 13, 62: 11, 63: 3, 64: 8, 65: 11, 66: 3, 67: 2, 68: 6, 69: 3, 70: 1, 71: 3, 72: 1, 73: 1, 74: 1, 75: 2, 76: 1}
    #Output: results1 = {35: 1, 36: 3, 37: 6, 38: 6, 39: 27, 40: 28, 41: 45, 42: 56, 43: 69, 44: 63, 45: 72, 46: 69, 47: 49, 48: 65, 49: 52, 50: 54, 51: 46, 52: 49, 53: 43, 54: 33, 55: 28, 56: 17, 57: 20, 58: 13, 59: 11, 60: 16, 61: 8, 62: 9, 63: 7, 64: 7, 65: 8, 66: 3, 67: 5, 68: 4, 69: 1, 71: 1, 73: 1, 74: 1, 75: 1, 79: 1, 80: 1, 87: 1}
    ####Question5####
    # result_scores0 = {36: 8, 37: 10, 38: 12, 39: 22, 40: 26, 41: 41, 42: 51, 43: 53, 44: 65, 45: 61, 46: 66, 47: 75, 48: 65,
    #           49: 70, 50: 48, 51: 42, 52: 38, 53: 35, 54: 31, 55: 33, 56: 25, 57: 19, 58: 13, 59: 8, 60: 13, 61: 13,
    #           62: 11, 63: 3, 64: 8, 65: 11, 66: 3, 67: 2, 68: 6, 69: 3, 70: 1, 71: 3, 72: 1, 73: 1, 74: 1, 75: 2, 76: 1}
    # result_scores1 = {35: 1, 36: 3, 37: 6, 38: 6, 39: 27, 40: 28, 41: 45, 42: 56, 43: 69, 44: 63, 45: 72, 46: 69, 47: 49,
    #                  48: 65, 49: 52, 50: 54, 51: 46, 52: 49, 53: 43, 54: 33, 55: 28, 56: 17, 57: 20, 58: 13, 59: 11,
    #                  60: 16, 61: 8, 62: 9, 63: 7, 64: 7, 65: 8, 66: 3, 67: 5, 68: 4, 69: 1, 71: 1, 73: 1, 74: 1, 75: 1,
    #                  79: 1, 80: 1, 87: 1}
    # result_scores2 = {35: 1, 36: 1, 37: 9, 38: 13, 39: 21, 40: 36, 41: 38, 42: 57, 43: 61, 44: 74, 45: 65, 46: 74, 47: 74,
    #                   48: 78, 49: 67, 50: 54, 51: 40, 52: 41, 53: 37, 54: 22, 55: 16, 56: 20, 57: 17, 58: 14, 59: 11,
    #                   60: 13, 61: 10, 62: 6, 63: 9, 64: 2, 65: 2, 66: 4, 67: 2, 69: 1, 70: 1, 71: 2, 72: 2, 73: 2, 74: 1,
    #                   80: 1, 84: 1}
    # score_of_local_alignment = 875
    # question5(result_scores, 1000, score_of_local_alignment)
    #Answer
    '''
    Standart mean is 51.657 and deviation is 6.91891255907
    Likelihood of the scores being a; product; of; chance 118.998902352
    '''
    ####Question6####
    '''
    I've run calculations couple times and got looks like bell shaped similar normal distribution plots of scores for 1000 trials.
    We got a high z-score (118.99) which means a lower likelihood that the local alignment score was due to chance.
    '''

    ####Question7####
    # result = ('HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ',
    #           'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ')
    # result = ('humble', 'humble')
    # question7(15, result[0], result[1])
    '''
    diag_score = 2
    off_diag_score = 1
    dash_score = 0
    '''


    ####Question 8####
    question8('file', "humble", 1, (2, 1, 0))
    question8('file', "firefly", 2, (2, 1, 0))
    '''
    Set of words within an edit distance for word "humble" is ['bumble', 'fumble', 'humble', 'humbled', 'humbler', 'humbles', 'humbly', 'jumble', 'mumble', 'rumble', 'tumble']
    Set of words within an edit distance for word "firefly" is ['direly', 'finely', 'fireclay', 'firefly', 'firmly', 'firstly', 'fixedly', 'freely', 'liefly', 'refly', 'tiredly']
    '''


    ####Question 9####
    #Hierarchical clustering requires less human supervision to produce clustering with relatively low distortion.

    ####Question 10
    #URLs = [alg_project3_viz.DATA_111_URL, alg_project3_viz.DATA_290_URL, alg_project3_viz.DATA_896_URL]
    #URLs = [alg_project3_viz.DATA_290_URL, alg_project3_viz.DATA_896_URL]
    #URLs = [alg_project3_viz.DATA_111_URL]
    #question10(URLs, 6, 20, 5, "Question10.png")

    ####Question11####
    ####No one method produces lower distortion clustering.


if __name__ == '__main__':
    main()