# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#
import random

class Node(object):
    def __init__(self, name):
        self.name = str(name)

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}

    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        if dest not in self.edges[src] and src != dest:
            self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.nodes:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

def generating_nodes(number_nodes):
    dgraph = Digraph()
    for number in range(number_nodes):
        node = Node(number)
        dgraph.addNode(node) # newNode takes one parameter, the number of the node
    return dgraph


def generating_graphs1(number_nodes):
    dgraph = generating_nodes(number_nodes)
    nodes = list(dgraph.nodes)
    for i in range(len(nodes)):
        x = random.choice(nodes)
        y = random.choice(nodes)
        edge = Edge(x, y)
        dgraph.addEdge(edge)
    print dgraph.edges
    print dgraph

def generating_graphs2(number_nodes):
    dgraph = generating_nodes(number_nodes)
    nodes = list(dgraph.nodes)
    for i in range(len(nodes)):
        x = random.choice(nodes)
        y = random.choice(nodes)
        edge = Edge(x, y)
        edge1 = Edge(y, x)
        dgraph.addEdge(edge)
        dgraph.addEdge(edge1)
    print dgraph.edges
    print dgraph

def generating_graphs3(number_nodes):
    dgraph = generating_nodes(number_nodes)
    nodes = list(dgraph.nodes)
    for i in range(len(nodes)):
        x = random.choice(nodes)
        y = random.choice(nodes)
        w = random.choice(nodes)
        z = random.choice(nodes)
        edge = Edge(x, y)
        edge1 = Edge(w, x)
        edge2 = Edge(z, w)
        edge3 = Edge(y, z)
        dgraph.addEdge(edge)
        dgraph.addEdge(edge1)
        dgraph.addEdge(edge2)
        dgraph.addEdge(edge3)
    print dgraph.edges
    print dgraph

def generating_graphs4(number_nodes):
    dgraph = generating_nodes(number_nodes)
    nodes = list(dgraph.nodes)
    for x in nodes:
        for y in nodes:
            edge = Edge(x, y)
            edge1 = Edge(y, x)
            dgraph.addEdge(edge)
            dgraph.addEdge(edge1)
    print dgraph.edges
    print dgraph

# print "generating_graphs1"
# generating_graphs1(10)
# print "generating_graphs2"
# generating_graphs2(6)
# print "generating_graphs3"
# generating_graphs3(6)
print "generating_graphs4"
generating_graphs4(4)