import csv
from collections import deque  # built in queue object
from pathlib import Path
from typing import List, Dict, Tuple, Any
from timeit import default_timer as timer
import pickle

__version__ = "2"


### Question 2
class Vertex:
    def __init__(self, identifier: Any):
        self.identifier = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"


class Queue:
    """FIFO Queue Object
    """

    def __init__(self):
        # we use the underscore to indicate that we do not want to access
        # the attribute directly (it's python's way of saying that it should
        # be treated as private)
        self._queue: List[Vertex] = []

    def __bool__(self) -> bool: return bool(self._queue)
    def popleft(self) -> Vertex: return self._queue.pop(0)
    def append(self, element: Vertex) -> None: self._queue.append(element)
    dequeue = popleft; enqueue = append

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

    i: int = 0
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
            i+=1

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
    queue.enqueue(vertices[source])
    while queue:
        print(queue._queue)
        u: Vertex = queue.dequeue()
        for v in graph[u.identifier]:
            if v == destination:
                print("dest reached: ",end='')
                print(v, destination)
                break
            if vertices[v].color == "white":
                vertices[v].color = "gray"
                vertices[v].d = u.d + 1
                vertices[v].pi = u
                queue.enqueue(vertices[v])
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
    print('mapping["Jita"], mapping["Dodixie"]')
    print(mapping["Jita"], mapping["Dodixie"])

    jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"])
    print_route(jita_dodixie_route, reverse_map)

### Question 3

def parse_requirements(fpath=Path("dependencies.txt")) -> Dict[str, List[str]]:
    """Function read in dependencies, and create a graph representation

    Keyword Arguments:
        fpath {[type]} -- Path to the file to be imported (default: {Path("dependencies.txt")})

    Returns:
        Dict[str, List[str]] -- A dictionary representing the graph.  The key will be 
    """
    raise NotImplementedError


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """Performs topological sort on the adjacency list generated earlier

    Arguments:
        graph {Dict[str, List[str]]} -- dictionary containing adjacency lists created by parse_requirements function

    Returns:
        List[str] -- Sorted dependencies
    """
    raise NotImplementedError


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
    #question3()


if __name__ == "__main__":
    main()
