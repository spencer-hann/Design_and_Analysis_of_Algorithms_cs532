import numpy as np
from queue import PriorityQueue as pqueue
import csv
from pathlib import Path

cdef Path fpath = Path("sde-universe_2018-07-16.csv")

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
    cdef list systems

    def __init__(System_list self):
        self.name_to_id = {}
        self.systems = []

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
    cdef System_list G = []
    with open(fpath) as f:
        r = csv.DictReader(f)
        for row in r:
            sys = System(
                    row["system_id"],
                    row['x'],
                    row['y'],
                    row['z'],
                    row["solarsystem_name"],
                    row["security_status"]
                    )

    w = np.array((len(G),len(G)), np.inf)

def main():
    print("hw10.pyx:main()")
    print("tests")
    cdef System test = System()
    print(test)
    cdef Vertex tst = Vertex(test)
