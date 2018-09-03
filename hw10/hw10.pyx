import numpy as np
cimport numpy as np
from queue import PriorityQueue
import csv
from pathlib import Path
from ast import literal_eval
from libc.math cimport sqrt
from heapq import heapify
import math

filename = "sde-universe_2018-07-16.csv"

cdef class System:
    cdef public str name
    cdef public int id
    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double security
    cdef public list adj

    def __init__(
            System self,
            str system_id,
            str adj,
            str x, str y, str z,
            str name="null",
            str security='0'
            ):
        self.name = name
        self.id = int(system_id)
        self.adj = list(literal_eval(adj))
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.security = max(0.,float(security))

    def __str__(self):
        return "System: " + self.name + \
            "\nLocation: (" + str(self.x) + \
            ", " + str(self.y) + ", " + \
            str(self.z) + ")"

    cdef double distance(System self, System other):
        return math.sqrt( # libc.math.sqrt
                (self.x - other.x)**2 +
                (self.y - other.y)**2 +
                (self.z - other.z)**2
                )

cdef class Vertex(System):
    cdef public double d
    cdef public Vertex pi

    def __init__(
            Vertex self,
            str system_id,
            str adj,
            str x, str y, str z,
            str name="null",
            str security='0'
            ):
        super().__init__(system_id,adj,x,y,z,name,security)
        self.d = float("inf")
        self.pi = None

    def __lt__(self, Vertex other): return self.d < other.d
    def __gt__(self, other): return self.d > other.d
    def __le__(self, other): return self.d <= other.d
    def __ge__(self, other): return self.d >= other.d
    def __eq__(self, other): return self.d == other.d
    def __ne__(self, other): return self.d != other.d

cdef class Vertex_list:
    cdef public dict names
    cdef public dict ids
    cdef public np.ndarray vertices

    def __init__(Vertex_list self, list lst):
        cdef int i = 0, size = len(lst)
        self.vertices = np.ndarray(size, Vertex)
        # get all vertices into a single list
        while i < size:
            self.vertices[i] = lst[i]
            i += 1
        # map names and ids to array indices
        self.ids = {s.id: i for s,i in zip(self.vertices,range(size))}
        self.names = {s.name: i for s,i in zip(self.vertices,range(size))}
        # path weights matrix

    def __len__(self): return len(self.vertices)

    def __getitem__(self, key):
        if type(key) is str:
            return self.vertices[self.names[key]]
        # if not str, should be int
        return self.vertices[self.ids[key]]
        # if type(key) is not int either, allow KeyError

    def __setitem__(self, tuple key, double val):
        self.w[self.ids[key[0].id], self.ids[key[1].id]] = val

    def __contains__(self, key):
        if type(key) is str: return key in self.names
        if type(key) is int: return key in self.ids
        return False

cdef Vertex_list load_file(fpath = Path(filename)):
    cdef list temp = []
    with open(fpath) as f:
        r = csv.DictReader(f)
        for row in r:
            if int(row["system_id"]) < 31_000_000:
                if not row["stargates"]: row["stargates"] = "[]"
                sys = Vertex(
                        row["system_id"],
                        row["stargates"],
                        row['x'], row['y'], row['z'],
                        row["solarsystem_name"],
                        row["security_status"]
                        )
                temp.append(sys)

    # creating my Vertex list from a list costs some
    # extra runtime, but it allows me to create a numpy
    # numpy array of the exact right size
    return Vertex_list(temp)

def w(Vertex u, Vertex v):
    if v.id not in u.adj: return float('inf')
    return u.distance(v)

################
#  Question 1  #
################

cdef void relax(Vertex u, Vertex v, Q):
    if v.d > u.d + w(u,v):
        v.d = u.d + w(u,v)
        v.pi = u
        heapify(Q.queue)

cdef void Dijkstras(Vertex_list G, Vertex s, dest):
    s.d = 0
    cdef int sys_id
    cdef Vertex u

    Q = PriorityQueue(maxsize=len(G))
    Q.queue = [u for u in G.vertices]
    heapify(Q.queue)

    while Q.queue:
        if len(Q.queue) % 1000 == 0: print(len(Q.queue))
        u = Q.get()
        for sys_id in u.adj:
            relax(u,G[sys_id],Q)

    print("Dodixie distance: " + str(G["Dodixie"].d))

cdef validate_path(list path, Vertex_list G):
    cdef double total =0
    for i in range(1,len(path)):
        if G[path[i]].id not in G[path[i-1]].adj:
            print(G[path[i-1]] +
                    " has no stargate to " +
                    G[path[i]].name
                )
            return None
        total += w(G[path[i]], G[path[i-1]])
    return total

cdef list get_path(Vertex start, Vertex dest):
    cdef list lst = []
    while dest is not start:
        lst.insert(0,dest.name)
        dest = dest.pi
    lst.insert(0,start.name)
    return lst

def q1_shortest_path(str start, str destination, return_graph=False):
    cdef Vertex_list G = load_file()
    if start not in G or destination not in G: return None
    Dijkstras(G, G[start], G[destination])
    path = get_path(G[start], G[destination])
    valid = validate_path(path, G)
    if valid == False:
        print("Error: invalid path")
    else:
        print("total distance: " + str(valid))
    print(validate_path(path, G))
    if return_graph:
        return path, G
    return path


################
#  Question 2  #
################
cdef void relax2(Vertex u, Vertex v, Q):
    if v.d > u.d:
        v.d = u.d if u.d > v.security else v.security
        #v.d = max(u.d,v.security)
        v.pi = u
        heapify(Q.queue)

cdef void Dijkstras2(Vertex_list G, Vertex s, dest):
    s.d = 0
    cdef int sys_id
    cdef Vertex u

    Q = PriorityQueue(maxsize=len(G))
    Q.queue = [u for u in G.vertices]
    heapify(Q.queue)

    while Q.queue:
        if len(Q.queue) % 1000 == 0: print(len(Q.queue))
        u = Q.get()
        for sys_id in u.adj:
            relax2(u,G[sys_id],Q)

def q2_best_path(str start, str destination):
    cdef Vertex_list G = load_file()
    if start not in G or destination not in G: return None

    Dijkstras2(G, G[start], G[destination])
    path = get_path(G[start], G[destination])
    return path


################
#  Question 3  #
################
cdef Vertex_list load_file_empty_adjacencies(fpath=Path(filename)):
    cdef list temp = []
    with open(fpath) as f:
        r = csv.DictReader(f)
        for row in r:
            if int(row["system_id"]) < 31_000_000:
                sys = Vertex(
                        row["system_id"],
                        "[]",
                        row['x'], row['y'], row['z'],
                        row["solarsystem_name"],
                        row["security_status"]
                        )
                temp.append(sys)

    # creating my Vertex list from a list costs some
    # extra runtime, but it allows me to create a numpy
    # numpy array of the exact right size
    return Vertex_list(temp)

cdef mst_prim(double limit): # no r, source node is arbitrary
    cdef Vertex_list G
    cdef np.ndarray w
    cdef Vertex u, v
    G, w = fill_adjacencies(limit)

    Q = PriorityQueue(maxsize=len(G))
    Q.queue = [u for u in G.vertices]
    Q.queue[0].d = 0

    while Q.queue:
        u = Q.get()
        for v in u.adj:
            if v in Q.queue and w[u,v] < v.d:
                v.pi = u
                v.key = w[u,v]
#this is Prims copied over quickly
# it may be better to calculate the distances in-time, rather than using the matrix
    return G, w # does w need to be returned?

cdef tuple fill_adjacencies(double limit):
    cdef Vertex_list G = load_file_empty_adjacencies()
    cdef Vertex u, v
    cdef int j, i=0, size = len(G.vertices)

    while i < size:
        u = G.vertices[i]
        j = i + 1
        while j < size:
            v = G.vertices[j]
            if u.distance(v) <= limit:
                u.adj.append(v)
                v.adj.append(u)
            j+=1
        i+=1
    return np.ndarray, G



def q3_fully_connected(limit): raise NotImplementedError


################
#  Question 4  #
################
cdef tuple load_distance_matrix(double limit):
    cdef Vertex_list G = load_file_empty_adjacencies()
    cdef int j, i=0, size = len(G.vertices)
    cdef double d
    cdef np.ndarray dist_matrx = np.zeros((size,size))

    while i < size:
        j = i + 1
        while j < size:
            d = G.vertices[i].distance(G.vertices[j])
            if d <= limit:
                G.vertices[i].adj.append(G.vertices[j])
                G.vertices[j].adj.append(G.vertices[i])
                dist_matrx[i,j] = d
                dist_matrx[j,i] = d
            j+=1
        i+=1
    return np.ndarray, G

def main():
    print("hw10.pyx:main()")
    print("tests")
    #print q1_shortest_path("6VDT-H","Dodixie")
    #path = q2_best_path("6VDT-H","N-RAEL")
    #print path
    #q3_fully_connected(1.0e22)
