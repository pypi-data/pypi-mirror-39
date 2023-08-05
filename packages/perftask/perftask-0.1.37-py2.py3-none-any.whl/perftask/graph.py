# -*- coding: utf-8 -*-

"""graph module."""

from __future__ import unicode_literals

import random

class Graph(object):

    START_MARK = random.getrandbits(64)
    STOP_MARK = random.getrandbits(64)

    def __init__(self):
        self._graph = {self.START_MARK: []}

    def __contains__(self, node):
        if node is None:
            return True
        else:
            return node in self._graph

    def __len__(self):
        return len(self._graph)

    def __iter__(self):
        for g in self._graph:
            if g in (self.START_MARK, self.STOP_MARK):
                continue
            yield g

    def add(self, node, prev_node):

        if prev_node is None:
            prev_node = self.START_MARK

        if node in self._graph:
            raise Exception("Node, '{}', already exists.".format(str(node)))

        if prev_node not in self._graph:
            raise Exception("Previous node, '{}', does not exist.".format(str(prev_node)))

        self._graph[prev_node].append(node)
        self._graph[node] = []

    def get_entrynodes(self):
        return self._graph[self.START_MARK]

    def get_nextnodes(self, node):
        return self._graph[node]

    def get_prevnodes(self, node):
        prevnodes = []
        for pnode, nnodes in self._graph.items():
            if node in nnodes:
                prevnodes.append(pnode)
        return prevnodes
