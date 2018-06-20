import random as r

G = {
'a': ['b'],
'b': ['a', 'c', 'd'],
'c': ['b', 'd'],
'd': ['b', 'c', 'e'],
'e': ['d', 'f'],
'f': ['e']
}

G = {
0: [1],
1: [0,2,3],
2: [1,3],
3: [1,2,4],
4: [3,5],
5: [4]
}

class graph():
    def __init__(self,num_of_vertices,edges):
        self.v = [x for x in range(num_of_vertices)]
        self.e = []
        x = 0
        while x < len(edges)-1:
            self.e.append(edges[x:x+2])
            x += 2
        self.d = {}
        for i in range(len(self.v)):
            self.d[i] = self.e

    def add(self, vertex, edges):
        self.d[vertex] = [edges]

def generate(num_nodes,run_time,p=False):
    G_set = []
    set_of_degrees = []
    edge_chance = (num_nodes**2 - num_nodes)
    for x in range(run_time):
        Gn = enum(num_nodes,edge_chance-r.randint(0,num_nodes)-((x*num_nodes**2)//run_time))
        if p: print((x*num_nodes)//run_time)
        test = neigh(Gn)
        if test[0] and test[1] not in set_of_degrees:
            if p: print(Gn)
            set_of_degrees.append(test[1])
            G_set.append(Gn)
    print(edge_chance-r.randint(0,num_nodes)-((x*num_nodes**2)//run_time))
    return G_set,set_of_degrees

def test_unique_degree(G_set):
    G_same_deg = []
    for G in G_set:
        degrees = []
        for node in G:
            degrees.append(len(G[node]))
        degrees.sort()
        x = 0
        unique = False
        if not(degrees[0] < degrees[1]):
            while x < len(degrees)-3:
                if degrees[x] < degrees[x+1] and degrees[x+1] < degrees[x+2]:
                    unique = True
                    break
                x += 1
        if not unique: G_same_deg.append(G)
    return G_same_deg
            

def max_deg(G):
    degrees = []
    for x in G:
        degrees.append(len(G[x]))
    return max(degrees) 

def enum(num_nodes,edge_chances):
    #for now, randomly enumerate connections between nodes
    Gn = {}
    for i in range(num_nodes):
        Gn[i] = []
    for x in range(edge_chances):
        a = r.randint(0,num_nodes-1)
        b = (a+r.randint(1,num_nodes-2))%(num_nodes-1)
        if b not in Gn[a]:
            Gn[a].append(b)
            Gn[b].append(a)
    return Gn
            

#This works well.
def match(G):
    """
    Turns a digraph into a simple graph
    O(n^2) or something watch out
    """
    for x in G:
        #Go through keys
        for y in G[x]:
            #Go through node data
            if x not in G[y]:
                G[y].append(x)

def reconstruct(set_of_degrees):
    G = {}
    for x in range(len(set_of_degrees)):
        G[x] = []
    num_edges = 0
    for degrees in set_of_degrees: num_edges += len(degrees)
    num_edges = num_edges//2

    G_edges = 0
    #an index num
    place  = find_only(set_of_degrees)
    while G_edges < num_edges:
        connecting_nodes = find_connecting_nodes(G,set_of_degrees,place)
        G[place].extend(connecting_nodes)
        for x in connecting_nodes:
            G[x].append(place)
        place = (place+1)%(len(G)-1)
        G_edges += len(connecting_nodes)
    return G

def find_connecting_nodes(G,set_of_degrees,place):
    connecting_nodes = []
    #for x in range(len(set_of_degrees[place])-len(G[place])):
    for y in set_of_degrees:
        if y != set_of_degrees[place]:
            if len(set_of_degrees[place]) in y and len(y) in set_of_degrees[place]: connecting_nodes.append(set_of_degrees.index(y))
    return connecting_nodes


def find_only(set_of_degrees):
    for degrees in set_of_degrees:
        same = True
        a = degrees[0]
        for x in degrees:
            if x != a: same = False
        if same: return set_of_degrees.index(degrees)
    
def neigh(G):
    prop = True
    set_of_degrees = []
    for node in G:
        degrees = []
        #Within node data
        for neighbor in G[node]:
            degrees.append(len(G[neighbor]))
        degrees.sort()
        if degrees in set_of_degrees: prop = False
        set_of_degrees.append(degrees)
    set_of_degrees.sort()
    return prop,set_of_degrees

def path(G,start=0):
    k = []
    loc = start
    for x in range(len(G)-1):
        k.append(loc)
        choice = 0 #choice to be moved to
        while G[loc][choice] in k:
            choice += 1
        loc = G[loc][choice]
    k.append(loc)
        
    return k

a = neigh(G)[1]
