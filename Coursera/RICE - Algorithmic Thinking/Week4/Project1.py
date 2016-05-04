"""Project 1"""

EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}



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


#digraph = make_complete_graph(6)

#print compute_in_degrees(GRAPH9)

#print in_degree_distribution(GRAPH9)

