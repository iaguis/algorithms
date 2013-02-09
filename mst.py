#!/usr/bin/env python
# -*- coding: utf8 -*-

import heap
import sys
import math

from collections import namedtuple
from itertools import permutations

Element = namedtuple ('Element', 'vertex priority')

class undirected_edges(dict):
    def __getitem__(self, key, second=None):
        return super(undirected_edges, self).__getitem__(tuple(sorted(key)))

    def __setitem__(self, key, value):
        super(undirected_edges, self).__setitem__(tuple(sorted(key)),value)

    def has_key(self, key):
        return super(undirected_edges, self).has_key(tuple(sorted(key)))

def initQueue (vertices, edges, start, queue):
    startVertex = start[0]
    neighbors = start[1]
    for v in vertices:
        if v in neighbors:
            minCost = min (edges[(startVertex, v)])
            queue.insert (Element (v, minCost))
        else:
            queue.insert (Element (v, sys.maxint))

def minEdge (edges, vertices, vertex, minCost):
    neighbors = vertices[vertex]
    for n in neighbors:
        if min (edges[(vertex, n)]) == minCost:
            return n, vertex

def prim_mst (vertices, edges):
    queue = heap.Heap()
    V = vertices.copy()
    start = V.popitem()
    X = set( )
    X.add(start[0])
    initQueue (V, edges, start, queue)
    T = set ()
    while X != set(vertices.keys()):
        element = queue.delMin()
        v = element.vertex
        cost = element.priority
        u, v = minEdge (edges, vertices, v, cost)
        T.add((u, v))
        X.add(v)

        for w in vertices:
            if w != v and queue.has_key(w):
                if edges.has_key((v, w)):
                    element = queue.delete(w)
                    key = min (element.priority, min (edges[(v, w)]))
                    queue.insert (Element (w, key))

    return T

def naive_prim_mst (vertices, edges):
    V = vertices.copy()
    start = V.popitem()
    X = set ()
    X.add(start[0])
    T = set ()
    while X != set (vertices.keys()):
        minCost = sys.maxint
        minU, minV = '', ''

        for perm in map (permutations, edges):
            for (u, v) in perm:
                if (u in X) and (not v in X):
                    if min(edges[(u, v)]) < minCost:
                        minCost = min(edges[(u, v)])
                        minU = u
                        minV = v

        T.add((minU, minV))
        X.add(minV)

    return T

def readFileEuler (filename):
    vertices = {}
    edges = undirected_edges()
    f = open (filename)
    i = 1
    j = 1
    weight = 0
    for line in f:
        neighbors = []
        j = 1
        line = line.rstrip()
        for val in line.split(','):
            if val.isdigit():
                cost = int(val)
                if j < i:
                    weight += cost
                neighbors.append(str(j))
                edges[(str(i), str(j))] = [cost]
            j += 1
        vertices[str(i)] = tuple(neighbors)
        i += 1
    return vertices, edges, weight

def readFileCoursera (filename):
    vertices = {}
    edges = undirected_edges()
    f = open (filename)

    f.readline()

    for line in f:
        line = line.rstrip()
        edge = line.split(' ')
        u = edge[0]
        v = edge[1]
        cost = int(edge[2])
        edges[(u, v)] = [cost]
        if vertices.has_key(u):
            vertices[u].append(v)
        else:
            vertices[u] = [v]
        if vertices.has_key(v):
            vertices[v].append(u)
        else:
            vertices[v] = [u]

    for key in vertices.keys():
        vertices[key] = tuple (vertices[key])

    return vertices, edges

def runMST (filename, coursera = False):
    if coursera:
        vertices, edges = readFileCoursera (filename)
    else:
        vertices, edges, weight = readFileEuler (filename)
    print "Computing minimum spanning tree of the graph in", "\"" + filename + "\" " \
          "with Prim's algorithm...\n"
    min_spanning_tree = prim_mst (vertices, edges)

    minweight = 0
    for edge in min_spanning_tree:
        minweight += min (edges[edge])

    if not coursera:
        print "Saving: ", weight - minweight
    else:
        print "Cost: ", minweight
    return min_spanning_tree

def main(filename):
    #runMST (filename)
    runMST (filename, True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: mst graph"
        sys.exit(0)

    main(sys.argv[1])
