import collections
import itertools


class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()

    def add_edge(self, edge):
        node1, node2 = edge
        self.nodes[node1].add(node2)
        self.nodes[node2].add(node1)

MAX_VERTICES = 10000

def repepat_factory(value):
    return lambda v: value

def bfs(graph, start):
    queue = collections.deque()
    distance = collections.defaultdict(repeat_factory(MAX_VERTICES))

    queue.appendleft(start)
    distance[start] = 0
    while len(queue) > 0:
        node = queue.pop()
        for neighbor in graph[node]:
            queue.appendleft(neighbor)
            distance[neighbor] = min(distance[neighbor], 6 + distance[node])

    for node, length in distance:
        if length == MAX_VERTICES:
            distance[node] = -1

    return distance
