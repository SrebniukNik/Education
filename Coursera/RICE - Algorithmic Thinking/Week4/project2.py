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
