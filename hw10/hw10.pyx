import numpy as np
cimport numpy as np
#define NPY_NO_DEPRECATED_API
#define NPY_1_7_API_VERSION
from queue import PriorityQueue as pqueue
import csv
from pathlib import Path

fpath = Path("sde-universe_2018-07-16.csv")

cdef class System:
    cdef str name
    cdef int id
    cdef int x
    cdef int y
    cdef int z
    cdef float security
    cdef list adj

    def __init__(
            System self,
            str system_id,
            str x, str y, str z,
            str name="null",
            str sec='0'
            ):
        self.name = name
        self.id = system_id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.security = max(0.,float(sec))
        self.adj = []

    def __str__(self):
        return "System: " + self.name + \
            "\nLocation: (" + str(self.x) + \
            ", " + str(self.y) + ", " + \
            str(self.z) + ")"

cdef class System_list:
    cdef dict name_to_id
    cdef np.ndarray systems

    def __init__(System_list self, int size):
        self.name_to_id = {}
        self.systems = np.ndarray(size, System)

    cdef add(System_list self, System to_add):
        pass

cdef class Vertex:
    cdef System system
    cdef float d
    cdef System pi
    def __init__(self, system):
        self.system = system
        self.d = float("inf")
        self.pi = None

cdef list q1_shortest_path(str start, str destination):
    cdef System_list G
    with open(fpath) as f:
        r = csv.DictReader(f)
        G = System_list(len(r))
        for row in r:
            sys = System(
                    row["system_id"],
                    row['x'], row['y'], row['z'],
                    row["solarsystem_name"],
                    row["security_status"]
                    )
            G.add(sys)

    w = np.full((len(G),len(G)), np.inf)

def main():
    print("hw10.pyx:main()")
    print("tests")
