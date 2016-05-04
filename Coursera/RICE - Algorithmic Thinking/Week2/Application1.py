"""Project 1"""

import urllib2


# EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
# EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
# EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

###################################
# Code for loading citation graph
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

#citation_graph = load_graph(CITATION_URL)

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

    #print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

#citation_graph = load_graph(CITATION_URL)

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary corresponding
    to a complete directed graph with the specified number of nodes
    Parameters:
        num_nodes: number of nodes

    Assumes:
        Provide positive number of num_nodes

    Returns:
        A complete graph contains all possible edges subject to the restriction
        that self-loops are not allowed. The nodes of the graph should be
        numbered 0 to num_nodes - 1 when num_nodes is positive. Otherwise,
        the function returns a dictionary corresponding to the empty graph.
    """
    graph = {}
    if num_nodes <= 0:
        return graph
    else:
        nodes = range(num_nodes)
        for node in nodes:
            tmp = nodes[:]
            tmp.remove(node)
            graph[node] = set(tmp)
    return graph


def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph.
    Parameters:
        digraph: dictionary corresponding to a complete directed
                graph
    Assumes:
        Provide complete directed graph with the specified number
        of nodes
    Returns:
        a dictionary with the same set of keys (nodes) as digraph
        whose corresponding values are the number of edges whose
        head matches a particular node.
    """
    edges = []
    edges_summary = {}
    #print "all values", digraph.values()
    for value in digraph.values():
        #print "value", value
        edges.extend(list(value))
    for node in digraph.keys():
        edges_summary[node] = edges.count(node)
    return edges_summary


def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) and
    computes the unnormalized distribution of the in-degrees of the graph.

    Parameters:
        digraph: dictionary corresponding to a complete directed
                graph
    Assumes:
        Provide complete directed graph with the specified number
        of nodes
    Returns:
        A dictionary whose keys correspond to in-degrees of nodes in the graph.
        The value associated with each particular in-degree is the number of
        nodes with that in-degree. In-degrees with no corresponding nodes in
        the graph are not included in the dictionary.
    """
    unnormalized = {}
    edges = compute_in_degrees(digraph)
    values = edges.values()
    #print "values", values
    for value in values:
        unnormalized[value] = values.count(value)
    return unnormalized

#You can provide URL of citation file or
CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
#graph = load_graph(input_file)
#You can provide filename of citation file or use function for downloading of URL
input_file = "citation_file.txt"
#Loading and format graph
graph = load_graph_file(input_file)
#print graph
indegree_count = compute_in_degrees(graph)

print indegree_count

unnorm_distribution = in_degree_distribution(indegree_count)

#print unnorm_distribution




#digraph = make_complete_graph(6)

#print compute_in_degrees(GRAPH9)

#print in_degree_distribution(GRAPH9)