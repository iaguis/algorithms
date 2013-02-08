#!/usr/bin/env python
# -*- coding: utf8 -*-

import heap
import sys
import math

from collections import namedtuple

Element = namedtuple ('Element', 'vertex priority')

def costs (edges, edge):
    u, v = edge
    if not edges.has_key ((u, v)):
        u, v = v, u
    return edges[(u, v)]

def initQueue (vertices, edges, start, queue):
    startVertex = start[0]
    neighbors = start[1]
    for v in vertices:
        if v in neighbors:
            minCost = min (costs (edges, (startVertex, v)))
            queue.insert (Element (v, minCost))
        else:
            queue.insert (Element (v, sys.maxint))

def minEdge (edges, vertices, vertex, minCost):
    neighbors = vertices[vertex]
    for n in neighbors:
        if min (costs(edges, (vertex, n))) == minCost:
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
        for (w, x) in edges:
            if x == v and queue.has_key (w):
                element = queue.delete(w)
                key = min (element.priority, min (costs (edges, (v, w))))
                queue.insert (Element (w, key))
            elif w == v and queue.has_key (x):
                element = queue.delete (x)
                key = min (element.priority, min (costs (edges, (v, x))))
                queue.insert (Element (x, key))

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

        for (u, v) in edges:
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
    edges = {}
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
    edges = {}
    f = open (filename)

    f.readline()

    for line in f:
        line = line.rstrip()
        edge = line.split(' ')
        u = edge[0]
        v = edge[1]
        cost = int(edge[2])
        # Yeah, this is hacky, so what?
        edges[(u, v)] = [cost]
        edges[(v, u)] = [cost]
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
        minweight += min (costs(edges, edge))

    if not coursera:
        print "Saving: ", weight - minweight
    else:
        print "Cost: ", minweight

def main(filename):
    #runMST (filename)
    runMST (filename, True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: mst graph"
        sys.exit(0)

    main(sys.argv[1])
