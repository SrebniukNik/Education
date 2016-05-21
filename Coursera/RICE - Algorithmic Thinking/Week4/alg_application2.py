"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import project2, project1
import alg_upa_trial

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plot


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        #print neighbors, max_degree_node
        try:
            for neighbor in neighbors:
                new_graph[neighbor].remove(max_degree_node)
        except KeyError:
            pass
        order.append(max_degree_node)
    #print "order", order
    return order

def fast_targeted_order(ugraph):
    """
    Fast compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    degree_sets = [set() for key in xrange(len(ugraph))]
    for node in ugraph:
        degree_sets[len(ugraph[node])].add(node)
    order_list = []
    count = 0
    for node in range(len(ugraph)-1, -1, -1):
        try:
            while degree_sets[node]:
                random_choice = random.choice(list(degree_sets[node]))
                degree_sets[node].remove(random_choice)
                for neighbor in ugraph[node]:
                    degree = len(ugraph[neighbor])
                    #DegreeSets[degree].remove(neighbor)
                    degree_sets[degree-1].add(neighbor)
                order_list.insert(count, random_choice)
                count += 1
                delete_node(ugraph, random_choice)
        except IndexError:
            pass
        except KeyError:
            pass
    #print "order list", order_list
    return order_list


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
INPUT_FILE = "alg_rf7.txt"


def load_graph_url(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
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


def re_algorithm(length, probability):
    '''
    Function for simulation of answer for Question w
    :param length: (int) lenght of nodes in graph (int)
    :param probability: :float. Probability
    :return:
    '''
    graph = {}
    for node in xrange(length):
        if node not in graph:
            graph[node] = set()
        for edge in xrange(node, length):
            if edge not in graph:
                graph[edge] = set()
            if node != edge:
                if random.random() < probability:
                    graph[node].add(edge)
                    graph[edge].add(node)
    return graph


def upa_algorithm(lenght, number_of_nodes):
    '''
    Function for generating graph with some : param probability edges for every node
    :param lenght: (int) lenght of nodes in graph (int)
    :param probability: :float. Probability
    :return:
    '''
    graph = project1.make_complete_graph(number_of_nodes)
    upa_alg = alg_upa_trial.UPATrial(number_of_nodes)
    #print upa_alg._node_numbers
    for node in xrange(number_of_nodes, lenght):
        nodes_to_connect = upa_alg.run_trial(number_of_nodes)
        graph[node] = nodes_to_connect
        for gen_node in nodes_to_connect:
            graph[gen_node].add(node)
    #print "upa graph", graph
    return graph

def random_order(graph):
    '''
    Function for radom order of graph nodes
    :param graph: dictionary of nodes and edges
    :return: list of shuffled nodes
    '''
    shuffled = graph.keys()
    random.shuffle(shuffled)
    return shuffled



# dgraph = re_algorithm(1239, 0.0039)
# cgraph = load_graph_file(INPUT_FILE)
# ugraph = upa_algorithm(1239, 3)
#
# print "RE edges", sum(len(edges) for edges in dgraph.values()), "nodes", len(dgraph.keys())
# print "Loaded from file edges", sum(len(edges) for edges in cgraph.values()), "nodes", len(cgraph.keys())#
# print "UPA from file edges", sum(len(edges) for edges in ugraph.values()), "nodes", len(ugraph.keys())#
#

#print random_order(cgraph)

def question1(file_to_save = None):
    '''

    :param INPUT_FILE:
    :return:
    '''
    nodes = 1238
    x_coordinate = range(nodes+1)
    cgraph = load_graph_file(INPUT_FILE)
    #cgraph = load_graph_url(NETWORK_URL)
    cattack = random_order(cgraph)
    print "cattack order", cattack
    cgraph_res = project2.compute_resilience(cgraph, cattack)
    print "cgraph_res", len(cgraph_res)
    dgraph = re_algorithm(nodes, 0.0039)
    dgraph_res = project2.compute_resilience(dgraph, random_order(dgraph))
    print "dgraph_res", len(dgraph_res)
    ugraph = upa_algorithm(nodes, 3)
    ugraph_res = project2.compute_resilience(ugraph, random_order(ugraph))
    print "ugraph_res", len(ugraph_res)

    plot.plot(x_coordinate, cgraph_res, '-r', label='Compute network')
    plot.plot(x_coordinate, dgraph_res, '-g', label='ER graph, p=0.0039')
    plot.plot(x_coordinate, ugraph_res, '-y', label='UPA graph, m=3')

    plot.title('Comparison of graph resilience for random attack order')
    plot.xlabel('Number of nodes removed')
    plot.ylabel('Size of largest connected component')
    plot.legend(loc='upper right')
    plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)

def question2(file_to_save = None):
    '''

    :param INPUT_FILE:
    :return:
    '''
    nodes = 1238
    # x_coordinate = range((nodes+1)/5)
    x_coordinate = range(248)
    cgraph = load_graph_file(INPUT_FILE)
    #cgraph = load_graph_url(NETWORK_URL)
    cattack = random_order(cgraph)
    print "cattack order", cattack
    cgraph_res = project2.compute_resilience(cgraph, random_order(cgraph)[:(nodes+1)/5])
    print "cgraph_res", len(cgraph_res), cgraph_res[-1]
    dgraph = re_algorithm(nodes, 0.0039)
    dgraph_res = project2.compute_resilience(dgraph, random_order(dgraph)[:(nodes+1)/5])
    print "dgraph_res", len(dgraph_res), dgraph_res[-1]
    print "x_coordinate", len(x_coordinate)
    ugraph = upa_algorithm(nodes, 3)
    ugraph_res = project2.compute_resilience(ugraph, random_order(ugraph)[:(nodes+1)/5])
    print "ugraph_res", len(ugraph_res), ugraph_res[-1]

    plot.plot(x_coordinate, cgraph_res, '-r', label='Compute network')
    plot.plot(x_coordinate, dgraph_res, '-g', label='ER graph, p=0.0039')
    plot.plot(x_coordinate, ugraph_res, '-y', label='UPA graph, m=3')

    plot.title('Comparison of graph resilience for random attack order')
    plot.xlabel('Number of nodes removed')
    plot.ylabel('Size of largest connected component')
    plot.legend(loc='upper right')
    plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)

def question3(file_to_save = None):
    '''
    Wrong func for this task
    :param INPUT_FILE:
    :return:
    '''
    time_target = []
    time_fast_target = []
    nodes = range(10, 1000, 10)
    print nodes
    for node_amount in nodes:

        ugraph = upa_algorithm(node_amount, 5)

        start_time = time.time()
        target_uattack = targeted_order(ugraph)
        stop_time = time.time()
        time_target.append(stop_time - start_time)

        start_time = time.time()
        fast_target_uattack = fast_targeted_order(ugraph)
        stop_time = time.time()
        time_fast_target.append(stop_time - start_time)

    plot.plot(nodes, time_target, '-r', label='Target attack: UPA graph')
    plot.plot(nodes, time_fast_target, '-g', label='Fast Target attack: UPA graph')

    plot.title('Regular vs fast computation of target order - PyCharm (IntelliJ)')
    plot.xlabel('Size of UPA graph, m = 5')
    plot.ylabel('Running time in seconds')
    plot.legend(loc='upper right')
    #plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)

def question4(file_to_save = None, type_target_order = None):
    '''

    :param INPUT_FILE:
    :return:
    '''
    nodes = 1238
    x_coordinate = range(nodes+1)
    cgraph = load_graph_file(INPUT_FILE)
    #cgraph = load_graph_url(NETWORK_URL)
    dgraph = re_algorithm(nodes, 0.0039)
    ugraph = upa_algorithm(nodes, 3)
    if not type_target_order:
        cattack = targeted_order(cgraph)
        dattack = targeted_order(dgraph)
        uattack = targeted_order(ugraph)
    elif type_target_order:
        cattack = fast_targeted_order(cgraph)
        dattack = fast_targeted_order(dgraph)
        uattack = fast_targeted_order(ugraph)
    print "cattack order", cattack
    cgraph_res = project2.compute_resilience(cgraph, cattack)
    print "cgraph_res", len(cgraph_res)
    dgraph_res = project2.compute_resilience(dgraph, dattack)
    print "dgraph_res", len(dgraph_res)
    ugraph_res = project2.compute_resilience(ugraph, uattack)
    print "ugraph_res", len(ugraph_res)

    plot.plot(range(len(cgraph_res)), cgraph_res, '-r', label='Compute network')
    plot.plot(range(len(dgraph_res)), dgraph_res, '-g', label='ER graph, p=0.0039')
    plot.plot(range(len(ugraph_res)), ugraph_res, '-y', label='UPA graph, m=3')

    plot.title('Comparison of graph resilience for random attack order')
    plot.xlabel('Number of nodes removed')
    plot.ylabel('Size of largest connected component')
    plot.legend(loc='upper right')
    plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)
    plot.clf()


def main():
    '''
    Launch execution of whole application
    :return:
    '''
    ##################################################################################
    #Answer for question 1:
    #Please check in current folder file: Question1_final.jpg
    question1("Question1_final.jpg")

    ###################################################################################
    #This func will help check 20% nodes removal during random attack
    #Answer for question 2:
    #All three graphs are resilient under random attack as the first 20% of their nodes
    #are removed.
    question2("Question2.jpg")
    ###################################################################################
    #This func will perform target random removal during random attack
    #Answer for question 3:
    #All three graphs are resilient under random attack as the first 20% of their nodes
    #are removed.
    ###################################################################################
    #Question 3.
    #1. The running time for targeted_order is O(n^2 + m)
    #   The running time for fast_targeted_order is O(n + m)
    #2. PyCharm (IntelliJ) desktop
    #3. In general its correct, but there are 2 strange spikes.
    question3("Question3_running_time_comparison.jpg")
    ###################################################################################
    # Question 4.
    # 1. The running time for targeted_order is O(n^2 + m)
    #   The running time for fast_targeted_order is O(n + m)
    # 2. PyCharm (IntelliJ) desktop
    # 3. In general its correct, but there are 2 strange spikes.
    question4("Question4_target_order_resilience.jpg", False)
    #question4("Question4_fastest_target_order_resilience.jpg", True)
    #Answer. All graphs are not resilient to target attack. Reason: almost all largest component are removed when
    #the first 20% of nodes are removed.

if __name__ == '__main__':
    main()

