EX_GRAPH0 = {}

EX_GRAPH1 = {}

EX_GRAPH2 = {}


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
            graph[node] = tmp
    return graph

print make_complete_graph(6)