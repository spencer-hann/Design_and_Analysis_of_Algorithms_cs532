import numpy as np
cimport numpy as np
from queue import PriorityQueue as pqueue
import csv
from pathlib import Path
from ast import literal_eval


cdef class System:
    cdef public str name
    cdef public int id
    cdef public float x
    cdef public float y
    cdef public float z
    cdef public float security
    cdef public list adj

    def __init__(
            System self,
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

cdef class Vertex(System):
    cdef float d
    cdef Vertex pi

    def __init__(
            Vertex self,
            str system_id,
            str adj,
            str x, str y, str z,
            str name="null",
            str sec='0'
            ):
        super().__init__(system_id,adj,x,y,z,name,sec)
        self.reset()

    cpdef void reset(self):
        self.d = float("inf")
        self.pi = None

    # convenient for inserting into queue.PriorityQueue
    def __iter__(self):
        """convenient for inserting into queue.PriorityQueue
        returns tuple(self.d,self), where self.d is the 
        priority key, and self is the value being inserted"""
        return tuple(self.d, self)

cdef class Vertex_list:
    cdef public dict names
    cdef public dict ids
    cdef public np.ndarray vertices
    cdef public np.ndarray w

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
        self.w = np.full((size,size), np.inf)

    def __len__(self): return len(self.vertices)

    def __getitem__(self, key):
        if type(key) is tuple:
            return self.w[self.ids[key[0].id], self.ids[key[1].id]]
        if type(key) is str:
            return self.names[key]
        # if not str, should be int
        return self.ids[key]
        # if type(key) is not int either, allow KeyError

    def __contains__(self, key):
        if type(key) is str: return key in self.names
        if type(key) is int: return key in self.ids
        return False

    cpdef void reset(self):
        for v in self.vertices: v.reset()

cdef Vertex_list load_file(fpath = Path("sde-universe_2018-07-16.csv")):
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

cdef void update_priority(Vertex v, pqueue Q):
    raise NotImplementedError

cdef void relax(Vertex u, Vertex v, Vertex_list w):
    if v.d > u.d + w[v,u]:
        v.d = u.d + w[v,u]
        v.pi = u

cdef void Dijkstras(Vertex_list G, Vertex s):
    s.d = 0
    cdef Vertex u
    cdef set S = set()
    cdef pqueue Q = pqueue(maxsize=len(G))
    Q.put(s)
    while Q:
        u = Q.pop()
        S.add(u)
        for v in u.adj:
            relax(u,v,G)
            update_priority(v,Q)

def q1_shortest_path(str start, str destination):
    cdef Vertex_list G = load_file()
    if start not in G or destination not in G: return None

    Dijkstras(G, G[start])
    return []

def main():
    print("hw10.pyx:main()")
    print("tests")
    q1_shortest_path("test","test")

