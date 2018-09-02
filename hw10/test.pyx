import numpy as np
cimport numpy as np
from queue import PriorityQueue as pqueue
import csv
from pathlib import Path
from ast import literal_eval
from libc.math cimport sqrt
from heapq import heapify


class tystem:
    def __init__(
            self,
            str system_id,
            str adj,
            str x, str y, str z,
            str name="null",
            str sec='0'
            ):
        self.name = name
        self.id = int(system_id)
        self.adj = list(literal_eval(adj))
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.security = max(0.,float(sec))

    def __str__(self):
        return "System: " + self.name + \
            "\nLocation: (" + str(self.x) + \
            ", " + str(self.y) + ", " + \
            str(self.z) + ")"

    def distance(self, other):
        return sqrt( # libc.math.sqrt
                (self.x**2 + other.x**2) +
                (self.y**2 + other.y**2) +
                (self.z**2 + other.z**2)
                )

class Vertex(System):
    def __init__(
            self,
            str system_id,
            str adj,
            str x, str y, str z,
            str name="null",
            str sec='0'
            ):
        super().__init__(system_id,adj,x,y,z,name,sec)
        self.d = float("inf")
        self.pi = None

    def __lt__(self, other): return self.d < other.d
    def __gt__(self, other): return self.d > other.d
    def __le__(self, other): return self.d <= other.d
    def __ge__(self, other): return self.d >= other.d
    def __eq__(self, other): return self.d == other.d
    def __ne__(self, other): return self.d != other.d

class Vertex_list:
    def __init__(self, list lst):
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
        self.w = np.full((size,size), np.inf)
        for u in self.vertices:
            for i in u.adj:
                v = self.vertices[self.ids[i]]
                self[u,v] = u.distance(v)

    def __len__(self): return len(self.vertices)

    def __getitem__(self, key):
        if type(key) is tuple:
            return self.w[self.ids[key[0].id], self.ids[key[1].id]]
        if type(key) is str:
            return self.vertices[self.names[key]]
        # if not str, should be int
        return self.vertices[self.ids[key]]
        # if type(key) is not int either, allow KeyError

    def __setitem__(self, tuple key, float val):
        self.w[self.ids[key[0].id], self.ids[key[1].id]] = val

    def __contains__(self, key):
        if type(key) is str: return key in self.names
        if type(key) is int: return key in self.ids
        return False

def load_file(fpath = Path("sde-universe_2018-07-16.csv")):
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

    return Vertex_list(temp)

cdef void update_priority(v, Q): raise NotImplementedError

cdef void relax(u, v, s, w):
    if v.d > u.d + w[u,v]:
        v.d = u.d + w[u,v]
        v.pi = u
        w[s,v] = v.d

cdef void Dijkstras(G, s):
    s.d = 0
    cdef int sys_id
    cdef set S = set()
    Q = pqueue(maxsize=len(G))
    #for u in G.vertices: Q.put((u.d,u))
    while Q:
        _,u = Q.get()
        S.add(u)
        for sys_id in u.adj:
            relax(u,G[sys_id],s,G)
            heapify(Q)

def q1_shortest_path(str start, str destination):
    G = load_file()
    if start not in G or destination not in G: return None

    Dijkstras(G, G[start])
    return []

def main():
    print("hw10.pyx:main()")
    print("tests")
    print(q1_shortest_path("test","test"))
    print(q1_shortest_path("6VDT-H","Dodixie"))


