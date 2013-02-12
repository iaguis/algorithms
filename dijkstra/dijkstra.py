import heap
import sys
import math
from collections import namedtuple

edges = { ("A", "B") : 3,
          ("B", "C") : 1,
          ("C", "D") : 7,
          ("D", "D") : 1,
          ("E", "A") : 4,
          ("E", "F") : 3,
          ("F", "G") : 2,
          ("G", "H") : 3,
          ("B", "E") : 2,
          ("B", "F") : 6,
          ("G", "F") : 1,
          ("C", "G") : 2,
          ("D", "C") : 1,
          ("C", "H") : 6,
          ("D", "H") : 4
        }

Element = namedtuple('Element', 'node priority')
Node = namedtuple('Node', 'name i j neighbors')

def get_distance (a, b):
    if (a.name, b.name) in edges:
        return edges[(a.name, b.name)]
    else:
        return sys.maxint

def dijkstra_to (nodes, source, target, width, height):
    distances = [sys.maxint for x in range(width*height)]
    previous = [None for x in range(width*height)]
    distances[source.i * width + source.j] = 0

    queue = heap.Heap()

    for n in nodes.values():
        if n == source:
            queue.insert(Element (n, 0))
        else:
            queue.insert(Element (n, sys.maxint))

    while not queue.isEmpty():
        u = queue.delMin()
        if u == target:
            return distances, previous

        if distances[u.i * width + u.j] == sys.maxint:
            return None, None

        for neighbor in u.neighbors:
            n = nodes[neighbor]
            if queue.has_key(n):
                new_distance = distances[u.i * width + u.j] + get_distance (u, n)
                queue.delete(n)
                if new_distance < distances[n.i * width + n.j]:
                    distances[n.i * width + n.j] = new_distance
                    previous[n.i * width + n.j] = u
                queue.insert(Element (n, new_distance))

    return distances, previous

nodes = { "A" : Node ("A", 0, 0, ("B")),
          "B" : Node ("B", 0, 1, ("C", "F", "E")),
          "C" : Node ("C", 0, 2, ("G", "D", "H")),
          "D" : Node ("D", 0, 3, ("C", "D", "H")),
          "E" : Node ("E", 1, 0, ("A", "F")),
          "F" : Node ("F", 1, 1, ("G")),
          "G" : Node ("G", 1, 2, ("F", "H")),
          "H" : Node ("H", 1, 3, ())
        }

source = Node ("A", 0, 0, ["B"])

width = 4
height = 2

distances, previous = dijkstra_to(nodes, source, None, width, height)
