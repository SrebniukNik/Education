'''BFS sear algorithm'''

from collections import deque
#import alg_module2_graphs
import random

def bfs_visited(ugraph, start_node):
    '''
    Func for BFS search algorithm
    :param ugraph: undirection graph in Dict format
    :param start_node: initial node for starting
    :return: set of visited nodes
    '''
    queue = deque([start_node])
    visited = set([start_node])
    #print "BFS visited - ugraph", ugraph, "start node", start_node
    while queue:
        check = queue.popleft()
        #print "Check,", check, " ", ugraph[check]
        if ugraph.has_key(check):
            for neighbor in ugraph[check]:
                if neighbor not in visited:
                    visited.add(neighbor)
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
        random_node = random.choice(remaining_node)
        connected_set = bfs_visited(ugraph, random_node)
        all_sets.append(connected_set)
        for node in connected_set:
            if node in remaining_node:
                remaining_node.remove(node)
    return all_sets

def largest_cc_size(ugraph):
    '''
    Func for producing the size (an integer) of the largest
    connected component in ugraph.
    :param ugraph: undirection graph in Dict format
    :return: integer
    '''
    cc_size_list = cc_visited(ugraph)
    component_lenghts = [len(cc_size) for cc_size in cc_size_list]
    if len(component_lenghts) > 0:
        return max(component_lenghts)
    else:
        return 0

#print cc_visited(EX_GRAPH)

#print largest_cc_size(EX_GRAPH)

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
    #print "largest component original", largest_original
    for target in attack_order:
        if attack_order.index(target) % 300 == 0:
            print "Target", target, ' index ', attack_order.index(target)
        #neighbors = ugraph[target]
        try:
            if target in ugraph:
                for neighbor in ugraph[target]:
                    if target in ugraph[neighbor]:
                        ugraph[neighbor].remove(target)
                    ugraph.pop(target, None)
        except KeyError:
            pass
        largest_atacked = largest_cc_size(ugraph)
        resilience.append(largest_atacked)
    resilience.insert(0, largest_original)
    return resilience

#print compute_resilience(alg_module2_graphs.GRAPH0, [1, 2])
