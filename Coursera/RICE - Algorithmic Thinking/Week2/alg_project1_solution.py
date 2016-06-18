'''BFS sear algorithm'''

from collections import deque
#import alg_module2_graphs

def bfs_visited(ugraph, start_node):
    '''
    Func for BFS search algorithm
    :param ugraph: undirection graph in Dict format
    :param start_node: initial node for starting
    :return: set of visited nodes
    '''
    queue = deque([start_node])
    visited = [start_node]
    #print "BFS visited - ugraph", ugraph, "start node", start_node
    while queue:
        check = queue.popleft()
        #print "Check,", check, " ", ugraph[check]
        if ugraph.has_key(check):
            for neighbor in ugraph[check]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
    return set(visited)

def cc_visited(ugraph):
    '''
    Func for producing list of sets, where each set consists of all the nodes
    (and nothing else) in a connected component
    :param ugraph: undirection graph in Dict format
    :return: list of sets
    '''
    remaining_node = ugraph.keys()
    all_sets = []
    while remaining_node:
        connected_set = bfs_visited(ugraph, remaining_node.pop())
        if connected_set not in all_sets:
            all_sets.append(connected_set)
    return all_sets

def largest_cc_size(ugraph):
    '''
    Func for producing the size (an integer) of the largest
    connected component in ugraph.
    :param ugraph: undirection graph in Dict format
    :return: integer
    '''
    remaining_node = ugraph.keys()
    size = 0
    while remaining_node:
        connected_set = bfs_visited(ugraph, remaining_node.pop())
        current_set_size = len(connected_set)
        if current_set_size > size:
            size = current_set_size
    return size

#print cc_visited(EX_GRAPH)

#print largest_cc_size(EX_GRAPH)

# EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
#
# EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
#
# EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}


def compute_resilience(ugraph, attack_order):
    '''
    Func tion that takes an undirected graph and a list of nodes that will be attacked.
    You will remove these nodes (and their edges) from the graph one at a time and then
    measure the "resilience" of the graph at each removal by computing the size of its
    largest remaining connected component.
    :param ugraph: undirection graph in Dict format
    :param attack_order: list of nodes
    :return: list of lists
    '''
    resilience = []
    largest_original = largest_cc_size(ugraph)
    for target in attack_order:
        #print "resilience urgaph Before pop", ugraph
        #largest_original = largest_cc_size(ugraph)
        #print "resilience", target, ugraph[target]
        #temp_list = [target] + list(ugraph[target])
        #print "temp_list", temp_list
        #for edge in temp_list:
        for neighbors in ugraph[target]:
            ugraph[neighbors].remove(target)
        ugraph.pop(target)
        #print "urgaph after pop", ugraph
        largest_atacked = largest_cc_size(ugraph)
        resilience.append(largest_atacked)
    resilience.insert(0, largest_original)
    return resilience

#print compute_resilience(alg_module2_graphs.GRAPH0, [1, 2])

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
