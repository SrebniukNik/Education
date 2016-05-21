"""Project 1"""

import random

import Project1
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


def plotting(graph, name, file_to_save=None):
    '''
    Function for plotting log-log normalized in-degree distribution for graph
    :param graph: :dict. Graph
    :param name: :str. plot name
    :param file_to_save: :str. file name for saving plotting
    :return: None
    '''
    plot.plot(graph.keys(), graph.values(), 'ro')
    plot.loglog()
    plot.title('Normalized in-degree distribution of a %s graph (log-log)' % name)
    plot.xlabel('In-degree')
    plot.ylabel('Normalized distribution')
    plot.xlim(0, 2000)
    plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)


def Question1(filename=None, file_to_save=None):
    '''
    Function for simulation of answer for Question 1
    :param filename: :string. File name for importing graph initial data
    :param file_to_save: :string. File name for saving plotting
    :return: None
    '''
    graph = load_graph_file(filename)
    normalized = normalization(Project1.in_degree_distribution(graph))
    plotting(normalized, 'citation', file_to_save)


#Question 2.
def re_algorithm(length, probability):
    '''
    Function for simulation of answer for Question w
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

#Answers on Question 2
#Q1.
# Is the expected value of the in-degree the same for every node in an ER graph?
# Please answer yes or no and include a short explanation for your answer.
#Answer:
#Yes

#Q2.What does the in-degree distribution for an ER graph look like?
#Provide a short written description of the shape of the distribution.
#Answer:
#It looks like binomial distribution where the number of node is number of trial and number of node edges is result for this trial

#Q3. Does the shape of the in-degree distribution plot for ER look similar to the shape of the in-degree distribution
#for the citation graph? Provide a short explanation of the similarities or differences.
#Focus on comparing the shape of the two plots as discussed in the class page on "Creating, formatting, and comparing plots".
#The plot for ED in-degree distribution looks lile as binomial distribution plot, where in-degree distribution look like
#logarithmic shape plot


def mean_out_degree(graph):
    '''
    Function generating mean of out degree
    :param graph: :dict. Graph
    :return: Float
    '''
    length = float(len(graph))
    return sum(len(x) for x in graph.itervalues()) / length


def Question3(file_to_save=None):
    '''
    Function for simulation answer for Question 3
    :param file_to_save: :string. File name for saving plotting
    :return: None
    '''
    random_graph = re_algorithm(2000, 0.25)
    normalized = normalization(Project1.in_degree_distribution(random_graph))
    plotting(normalized, 'randomly generated', file_to_save)


def dpa_algorithm(lenght, probability):
    '''
    Function for generating graph with some : param probability edges for every node
    :param lenght: (int) lenght of nodes in graph (int)
    :param probability: :float. Probability
    :return:
    '''
    graph = Project1.make_complete_graph(probability)
    dpa_alg = alg_dpa_trial.DPATrial(probability)
    for dummy_i in xrange(probability, lenght):
        graph[dummy_i] = dpa_alg.run_trial(probability)
    return graph


def Question4(filename, file_to_save=None):
    '''
    Function for simulation answer for Question 4
    :param filename: :string. File name for importing graph initial data
    :param file_to_save: :string. File name for saving plotting
    :return: None
    '''
    graph = load_graph_file(filename)
    print 'Mean out degree ', mean_out_degree(graph)
    dpa_result = dpa_algorithm(27700, 13)
    normalized = normalization(Project1.in_degree_distribution(dpa_result))
    plotting(normalized, 'DPA-generated', file_to_save)


#Answers on Question 5
#Q1.
#Is the plot of the in-degree distribution for the DPA graph similar to that of the citation graph?
#Provide a short explanation of the similarities or differences. Focus on the various properties of the
#two plots as discussed in the class page on "Creating, formatting, and comparing plots".
#Answer:
# None

#Q2.What does the in-degree distribution for an ER graph look like?
#Which one of the three social phenomena listed above mimics the behavior of the DPA process?
#Provide a short explanation for your answer.
#Answer:
#None

#Q3. Could one of these phenomena explain the structure of the physics citation graph?
#Provide a short explanation for your answer.
#Answer:
#None

def main():
    '''
    Main function
    :return:
    '''
    filename = 'citation_file.txt'
    Question1(filename, 'Question1-citation.png')
    plot.clf()
    Question3('Question3-random.png')
    plot.clf()
    Question4(filename, 'Question4-dpa.png')
    plot.clf()



if __name__ == '__main__':
    main()