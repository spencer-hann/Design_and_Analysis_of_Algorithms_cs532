import csv
from collections import deque  # built in queue object
from pathlib import Path
from typing import List, Dict, Tuple, Any
from timeit import default_timer as timer
import pickle

__version__ = "2"


### Question 2
cdef class Vertex:
    cdef public int identifier
    cdef public object d
    cdef public object pi
    cdef public object color
    def __init__(self, identifier: Any):
        self.identifier = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"

cdef class Queue:
    """FIFO Queue Object
    """
    cdef public list _queue

    def __init__(self):
        # we use the underscore to indicate that we do not want to access
        # the attribute directly (it's python's way of saying that it should
        # be treated as private)
        self._queue: List[Vertex] = []

    def __bool__(self) -> bool: return bool(self._queue)
    def popleft(self) -> Vertex: return self._queue.pop(0)
    def append(self, element) -> None: self._queue.append(element)
    def appendleft(self,element) -> None: self._queue.insert(0,element)

def parse_universe(
    fpath=Path("sde-universe_2018-07-16.csv")
) -> Tuple[List[List[int]], Dict[int, str]]:
    """Method will parse the CSV file and build up a graph representation of the eve universe
    Keyword Arguments:
        fpath {[type]} -- path to the csv object ot import (default: {Path("sde-universe_2018-07-16.csv")})
    Returns:
        Tuple[List[List[int]], Dict[int, str] -- First item returned is an adjacency list reprenting
        the graph in the Eve Universe, the second item returned is a dictionary with keys of indexes
        in the adjacency list, and values as the system names.
    """

    # dictionary where key is a system_id and value is a list of adjacent system_ids
    system_mapping: Dict[int, List[int]] = {}

    # dictionary where the key is the name of the system, and the value is the associated system_id
    name_to_id: Dict[str, int] = {}

    # dictionary where key is the system_id, and the value is the index number in the
    # adjacency lists representation
    id_to_index: Dict[int, int] = {}

    cdef int i = 0
    with open(fpath) as f:
        reader = csv.reader(f)
        next(reader) # take first line
        for row in reader:
            if row[9]:
                row[9] = row[9][1:-1] # remove square brackets
                row[9] = row[9].split(',')
                row[9] = list(map(lambda x: int(x),row[9]))
            else: row[9] = []
            system_mapping[int(row[10])] = row[9]
            name_to_id[row[7]] = int(row[10])
            id_to_index[int(row[10])] = i
            i += 1

    # empty list of the right size to put your adjacency lists into
    graph: List[List[int]] = [None] * len(system_mapping)
    i = 0
    for system, adjacents in system_mapping.items():
        # here is where you populate the adjacency lists representation
        graph[i] = list(map(lambda a: id_to_index[a], adjacents))
        i += 1

    # not only can you do list comprehensions
    # you can do dictionary comprehensions in python as well!!
    name_to_index = {
        name: id_to_index[system_id] for name, system_id in name_to_id.items()
    }
    return graph, name_to_index

def backtrace(node: Vertex) -> List[int]:
    """Method creates a list of elements that correspond to the order of progression

    Arguments:
        node {Vertex} -- Vertex to backtrace from

    Returns:
        List[int] -- reconstructing the back-pointers
    """
    path = [node.identifier]
    while node.pi is not None:
        path.insert(0, node.pi.identifier)
        node = node.pi
    return path

def breadth_first_search(
    graph: List[List[int]], source: int, destination: int, use_python_deque=False
) -> List[int]:
    """Perform BFS on the graph,
    Arguments:
        graph {List[List[int]]} -- The adjacensy list representation of the graph
        source {int} -- The system index of the starting system
        destination {int} -- The system index of the destination system
    Keyword Arguments:
        use_python_deque {bool} -- option to use the native deque python object or your own implementation (default: {False})
    Returns:
        List[int] -- The list of system indexes representing the shortest path from the source to target destination
    """

    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].color = "gray"
    vertices[source].d = 0

    if use_python_deque:
        queue = deque()
    else:
        queue = Queue()

    # Here is where you implement the breadth first search
    queue.append(vertices[source])
    cdef Vertex u
    while queue:
        u = queue.popleft()
        for v in graph[u.identifier]:
            if vertices[v].color == "white":
                vertices[v].color = "gray"
                vertices[v].d = u.d + 1
                vertices[v].pi = u
                queue.append(vertices[v])
            if v == destination: queue = 0 # break outer
            u.color = "black"

    return backtrace(vertices[destination])

def print_route(route: List[int], reverse_mapping: Dict[int, str]) -> None:
    named_route = [reverse_mapping[system] for system in route]
    print(" -> ".join(named_route))

def question2(import_pickle=False):
    if import_pickle:
        with open("Q2_pickle", "rb") as f:
            graph = pickle.load(f)
            mapping = pickle.load(f)
    else:
        graph, mapping = parse_universe()
    # mapping gives us a dict of name -> index
    # BFS algorithm will give us a list of indexes, so we need a dict
    # of index -> name
    reverse_map = {index: name for name, index in mapping.items()}

    jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"])
    print_route(jita_dodixie_route, reverse_map)

def queue_test():
    graph, mapping = parse_universe()
    cdef int num_runs = 50000
    cdef int i = 0

    #from time import clock as timer
    start = timer()
    while i < num_runs:
        jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"], False)
        i += 1
    jd_queue = timer() - start

    i = 0; start = timer()
    while i < num_runs:
        jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"], True)
        i += 1
    jd_pydeque = timer() - start

    i = 0; start = timer()
    while i < num_runs:
        jita_dodixie_route = breadth_first_search(graph, mapping["313I-B"], mapping["ZDYA-G"], False)
        i += 1
    z_queue = timer() - start

    i = 0; start = timer()
    while i < num_runs:
        jita_dodixie_route = breadth_first_search(graph, mapping["313I-B"], mapping["ZDYA-G"], True)
        i += 1
    z_pydeque = timer() - start

    print("\t\tPython Deque\tCustom Queue")
    print("Jita->Dodixie\t%.6f\t%.6f" % (jd_pydeque, jd_queue))
    print("313I-B->ZDYA-G\t%.6f\t%.6f" % (z_pydeque, z_queue))
    print()

### Question 3

def parse_requirements(fpath=Path("dependencies.txt")) -> Dict[str, List[str]]:
    """Function read in dependencies, and create a graph representation

    Keyword Arguments:
        fpath {[type]} -- Path to the file to be imported (default: {Path("dependencies.txt")})

    Returns:
        Dict[str, List[str]] -- A dictionary representing the graph.  The key will be
    """
    graph: Dict[str, List[str]] = {}
    with open(fpath) as f:
        rdr = csv.reader(f)
        for row in rdr:
            row[0] = row[0].strip()
            if row[0][0] != '-':
                main = row[0]
                graph[main] = []
            else:
                graph[main].append(row[0][2:])
    return graph

class Node:
    def __init__(self, identifier: str, adj: List):
        self.id = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"
        self.adjacencies = adj

def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """Performs topological sort on the adjacency list generated earlier

    Arguments:
        graph {Dict[str, List[str]]} -- dictionary containing adjacency lists created by parse_requirements function

    Returns:
        List[str] -- Sorted dependencies
    """
    #vrt: List[Node] = [i for i in str_to_node)]

    # create node object for every item and map str to node
    mapping: Dict[str, Node] = {i: Node(i,None) for i in graph}
    # include nodes for items without dependencies
    for nodes in graph.values():
        for adj in nodes:
            if adj not in mapping:
                mapping[adj] = Node(adj,[])
    # iterate thru hash map, creating adjacency list for each node
    vrt: List[Node] = [mapping[i] for i in mapping]
    for n in vrt:
        if n.adjacencies is None:
            n.adjacencies = [mapping[i] for i in graph[n.id]]

    path: List[str] = []
    for u in vrt:
        if u.color == "white":
            dfs(u, path)
            #dfs_recursive(u, path)
    return path

def dfs_recursive(u: Node, path: List[str]) -> None:
    u.color = "done"
    for v in u.adjacencies:
        if v.color == "white":
            v.pi = u
            dfs(v, path)
    path.append(u.id)

def dfs(s: Node, path: List[str]) -> None:
    s.color = "done"

    stack = [s]
    stack2 = [s]
    while stack:
        u = stack.pop()
        for v in u.adjacencies:
            if v.color == "white":
                v.color = "done"
                stack.insert(0, v)
                stack2.append(v)

    while stack2: path.append(stack2.pop().id)

def question3(import_pickle=False) -> List[str]:
    """Function to give the solution to Question 3
    Returns:
        List[str] -- returns a list of strings with the order in which one should install TimeView's dependencies
    """

    if import_pickle:
        with open("Q3_pickle", "rb") as f:
            graph = pickle.load(f)
    else:
        graph = parse_requirements()
    install_order = topological_sort(graph)
    print(install_order)
    return install_order


def main():
    question2()
    #queue_test()
    question3()


if __name__ == "__main__":
    main()
