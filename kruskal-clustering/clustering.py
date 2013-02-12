#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import math

class undirected_edges(dict):
    def __getitem__(self, key, second=None):
        return super(undirected_edges, self).__getitem__(tuple(sorted(key)))

    def __setitem__(self, key, value):
        super(undirected_edges, self).__setitem__(tuple(sorted(key)),value)

    def has_key(self, key):
        return super(undirected_edges, self).has_key(tuple(sorted(key)))

class union_find():
    def __init__ (self, vertices):
        self.groups = {}
        self.leaders = {}
        self.k = 0
        for v in vertices:
            leader = v
            group_vertices = [v]
            size = 1
            self.groups[v] = (leader, group_vertices, size)
            self.leaders[v] = v
            self.k += 1

    def find (self, vertex):
        return self.leaders[vertex]

    def union (self, group1, group2):
        leader1, vertices1, size1 = self.groups[group1]
        leader2, vertices2, size2 = self.groups[group2]

        if size1 > size2:
            new_leader = leader1
            smaller_vertices = vertices2
            bigger_vertices = vertices1
            smaller_group = group2
            bigger_group = group1
        else:
            new_leader = leader2
            smaller_vertices = vertices1
            bigger_vertices = vertices2
            smaller_group = group1
            bigger_group = group2

        for vertex in smaller_vertices:
            # Add vertices of smaller group to bigger group
            bigger_vertices.append(vertex)
            # Update leader of moved vertices
            self.leaders[vertex] = new_leader
        # Discard smaller group
        self.groups.pop(smaller_group)
        # Update bigger group
        self.groups[bigger_group] = (new_leader, bigger_vertices, size1 + size2)
        # Lower cluster count
        self.k -= 1

def k_clustering (vertices, edges, k):
    sorted_edges = sorted (edges, key=lambda edge: edges[edge])
    T = set()
    uf = union_find(vertices)
    for (u, v) in sorted_edges:
        group_u = uf.find(u)
        group_v = uf.find(v)
        if group_u != group_v:
            # We reached K so we output the next edge that we would use to
            # join the next two groups
            if uf.k == k:
                return min(edges[(u, v)])

            T.add((u, v))
            uf.union(group_u, group_v)

    return "ERROR"

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

def runClustering (filename, k):
    vertices, edges = readFileCoursera (filename)
    print "Computing clustering with k =", k, "of the graph in", "\"" + filename + "\" " \
          "with Kruskal's algorithm...\n"
    max_spacing = k_clustering (vertices, edges, k)

    return max_spacing

def main(filename, k):
    max_spacing = runClustering (filename, k)
    print "Maximum spacing of a", str(k) + "-clustering =", max_spacing

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: clustering graph_file.txt k"
        sys.exit(0)

    main(sys.argv[1], int(sys.argv[2]))
