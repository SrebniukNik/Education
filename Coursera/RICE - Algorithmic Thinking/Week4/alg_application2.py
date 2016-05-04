"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import project2

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


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
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order



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
    graph = {key: set() for key in xrange(length)}
    for i in xrange(length):
        for j in xrange(length):
            if i != j:
                if random.random() < probability:
                    graph[i].add(j)
                if random.random() < probability:
                    graph[j].add(i)
    return graph


def upa_algorithm(final_number, existing_number):
    '''
    Function for generating graph with some : param probability edges for every node
    :param lenght: (int) lenght of nodes in graph (int)
    :param probability: :float. Probability
    :return:
    '''
    graph = project1.make_complete_graph(existing_number)
    dpa_alg = alg_dpa_trial.DPATrial(existing_number)
    for dummy_i in xrange(existing_number, final_number):
        graph[dummy_i] = dpa_alg.run_trial(existing_number)
    return graph