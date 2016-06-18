"""Project 1"""

import random

import alg_project1_solution
import matplotlib.pyplot as plot

import alg_dpa_trial


###########################################
# Code for loading citation graph from file

def load_graph_file(input_file):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = open(input_file, 'rb')
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def normalization(distribution):
    '''
    Function for normalizing edges distribution
    :param distribution: :dict. Unnormilized distribution
    :return: Dict
    '''
    new_dict = {}
    total = float(sum(value for value in distribution.values()))
    for degree, count in distribution.iteritems():
        new_dict[degree] = count / total
    return new_dict

def plotting(graph, title, xlabel, ylabel, xlim, file_to_save=None):
    '''
    Function for plotting log-log normalized in-degree distribution for graph
    :param graph: :dict. Graph
    :param name: :str. plot name
    :param file_to_save: :str. file name for saving plotting
    :return: None
    '''
    plot.plot(graph.keys(), graph.values(), 'ro')
    plot.loglog()
    plot.title(title)
    plot.xlabel(xlabel)
    plot.ylabel(ylabel)
    #plot.xlim(0, xlim)
    plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)
    plot.clf()

def mean_out_degree(graph):
    '''
    Function generating mean of out degree
    :param graph: :dict. Graph
    :return: Float
    '''
    length = float(len(graph))
    return sum(len(x) for x in graph.itervalues()) / length

def dpa_algorithm(lenght, probability):
    '''
    Function for generating graph with some : param probability edges for every node
    :param lenght: (int) lenght of nodes in graph (int)
    :param probability: :float. Probability
    :return:
    '''
    graph = alg_project1_solution.make_complete_graph(probability)
    dpa_alg = alg_dpa_trial.DPATrial(probability)
    for dummy_i in xrange(probability, lenght):
        graph[dummy_i] = dpa_alg.run_trial(probability)
    return graph

def re_algorithm(length, probability):
    '''
    Function for simulation of answer for question w
    :param length: (int) lenght of nodes in graph (int)
    :param probability: :float. Probability
    :return:
    '''
    graph = {key: set() for key in xrange(length)}
    for i in xrange(length):
        for j in xrange(length):
            if i != j:
                if random.random() < probability:
                    graph[i].add(j)
                if random.random() < probability:
                    graph[j].add(i)
    return graph


def question1(filename=None, file_to_save=None):
    '''
    Function for simulation of answer for question 1
    :param filename: :string. File name for importing graph initial data
    :param file_to_save: :string. File name for saving plotting
    :return: None
    '''
    graph = load_graph_file(filename)
    normalized = normalization(alg_project1_solution.in_degree_distribution(graph))
    title = 'Log/Log plot of in_degree distribution for the citation graph'
    xlabel = 'Number of citations'
    ylabel = 'Fraction of papers'
    xlim = 2500
    plotting(normalized, title, xlabel, ylabel, xlim, file_to_save)

def question2(length=None, probability=None, file_to_save=None):
    '''

    :return:
    '''
    graph = re_algorithm(length, probability)
    #normalized = normalization(alg_project1_solution.in_degree_distribution(graph))
    normalized = alg_project1_solution.in_degree_distribution(graph)
    title = 'Log/Log plot of in_degree distribution for the ER algorithm'
    xlabel = 'Number of citations'
    ylabel = 'Fraction of papers'
    xlim = 2500
    plotting(normalized, title, xlabel, ylabel, xlim, file_to_save)

def question3(filename=None, file_to_save=None):
    '''
    Function for simulation answer for question 3
    :param file_to_save: :string. File name for saving plotting
    :return: None
    '''
    graph = load_graph_file(filename)
    nodes = len(graph)
    edges = sum(len(x) for x in graph.itervalues())
    mean = edges / float(nodes)
    print "Number of nodes: {0}. Number of edges: {1}. Value of m (mean): {2}".format(nodes, edges, mean)


def question4(filename, file_to_save=None):
    '''
    Function for simulation answer for question 4
    :param filename: :string. File name for importing graph initial data
    :param file_to_save: :string. File name for saving plotting
    :return: None
    '''
    # graph = load_graph_file(filename)
    # print 'Mean out degree ', mean_out_degree(graph)
    dpa_result = dpa_algorithm(27770, 13)
    normalized = normalization(alg_project1_solution.in_degree_distribution(dpa_result))
    title = 'Log/Log plot of in_degree distribution for the DPA graph'
    xlabel = 'in_degree'
    ylabel = 'Fraction of nodes'
    xlim = 2500
    plotting(normalized, title, xlabel, ylabel, xlim, file_to_save)



def main():
    '''
    Main function
    :return:
    '''
    filename = 'citation_file.txt'
    # question1(filename, 'question1-citation.png')

    # question2(27770, 0.01, 'question2-ER_1.png')
    # question2(500, 0.3, 'question2-ER_2.png')
    '''
    Answers on question 2
    Item a. Answer:
    Yes. ER algorithm produce each node in the graph in same way as in-degree distribution. So expected value for each
    node must be a same.
    Item b. Answer:
    The in-degree distribution for an ER graph looks like Gaussian distribution (binomially distributed)
    Item c. Answer:
    No. The in-degree distribution for an ER graph looks like Gaussian distribution and citiation graphs
    has linear shape of in-degree distribution.
    '''
    #
    #question3(filename)
    '''
    Answer 3:
    Number of nodes: 27769. Number of edges: 352765. Value of m (mean): 12.7035543232
    '''
    question4(filename, 'question4-dpa.png')

    #question5
    '''
    Item a. Answer:
    The plot of the in-degree distribution for the DPA graph is completely similar with plot of in-degree distribution
    of citation graph.
    Item b. Answer:
    "The rich gets richer"is correct phenomenon. In DPA algorithm node with higher degree has greater probability to get a new
    edge. LIke if you have more money You have more chance to be close to more richest people and grasp new ideas to become
    more richest.
    Item c. Answer:
    On my opinion it is "Rich get richer" phenomenon. The same as is for DPA algorithm.
    '''

if __name__ == '__main__':
    main()