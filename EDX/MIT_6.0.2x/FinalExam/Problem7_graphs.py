import pylab, random

class newNode(object):
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

class siteGraph(object):
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
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}'.format(res, k, d)
        return res[:-1]

def initializeGraph(n): # n is an integer, the number of nodes in the graph
    G = siteGraph() # Initializes an empty graph, with G.graphNodes set to []
    for i in range(n):
        G.graphNodes.append(newNode(i)) # newNode takes one parameter, the number of the node
    for i in range(n):
    	x = G.graphNodes[i]
        y = G.graphNodes[ (i+1) % n ]
    	x.addOutEdge(y)
	y.addInEdge(x)
	G.allEdges.append((x, y))
    return G.graphNodes

def simulation(n):
    maxDegrees, meanDegrees, meanDegreeVariances, meanShortestPaths = [],[],[],[]
    graph = initializeGraph(n)
    for nEdges in range(n, n*n, n*n/10 ):
       graph.addEdges(nEdges)
       maxDegrees.append(graph.maxDegree())
       meanDegrees.append(graph.meanDegree())
       meanDegreeVariances.append(graph.meanDegreeVariances())
       meanShortestPaths.append(graph.meanShortestPath())
       pylab.plot(x_coordinates, y_coordinates, 'or',
                  label='{} Drunk'.format(move))


    pylab.title('{} drunk simulation'.format(move))
    pylab.xlabel('x coordinate')
    pylab.ylabel('y coordinate')
    pylab.legend()
    pylab.xlim(-60, 60)
    pylab.ylim(-60, 60)
    if file_name:
        new_file = file_name + "_" + move + ".png"
        pylab.savefig(new_file)
    pylab.close()