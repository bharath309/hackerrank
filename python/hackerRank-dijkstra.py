import collections
import heapq
import queue
import unittest

# Cost comes first because that's how we want to compare edges
Edge = collections.namedtuple('Edge', ['cost', 'destination'])

class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = collections.defaultdict(list)


    def add_node(self, node):
        self.nodes.add(node)


    def add_edge(self, vertex1, vertex2, cost):
        self.nodes.add(vertex1)
        self.nodes.add(vertex2)
        self.edges[vertex1].append(Edge(cost=cost, destination=vertex2))
        self.edges[vertex2].append(Edge(cost=cost, destination=vertex1))


    @staticmethod
    def from_edges(edges):
        "Create graph from a list of (start, end, cost) tuples."
        graph = Graph()
        for start, end, cost in edges:
            graph.add_edge(start, end, cost)
        return graph

# The priority of the next Vertex.  Dijkstra's is greedy and only works if we
# pick the closest vertex next.
VertexPriority = collections.namedtuple("VertexPriority", ["cost", "vertex"])

def find_shortest_path(graph, start):
    # Initial distance travel distance is +inf so we can use min
    travel_costs = {node: float("+inf") for node in graph.nodes}
    travel_costs[start] = 0

    nodes_visited = set()
    frontier = queue.PriorityQueue()
    frontier.put(VertexPriority(cost=0, vertex=start))

    while not frontier.empty():
        _cost, node_current = frontier.get()
        node_cost = travel_costs[node_current]

        if node_current in nodes_visited:
            continue
        else:
            nodes_visited.add(node_current)

        for edge in graph.edges[node_current]:
            destination_cost = min(node_cost + edge.cost,
                                   travel_costs[edge.destination])
            frontier.put(VertexPriority(cost=destination_cost,
                                        vertex=edge.destination))
            travel_costs[edge.destination] = destination_cost

    # Mark disconnected nodes
    for node,cost in travel_costs.items():
        if cost == float("+inf"):
            travel_costs[node] = -1

    return travel_costs


class TestDijkstra(unittest.TestCase):

    def test_2_node_graph(self):
        graph = Graph.from_edges([(1, 2, 7)])
        expected = {1: 0, 2: 7}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_2_node_graph_edges_reveresed(self):
        graph = Graph.from_edges([(2, 1, 7)])
        expected = {1: 0, 2: 7}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_2_node_graph_disconnected(self):
        graph = Graph()
        graph.add_node(1)
        graph.add_node(2)
        expected = {1: 0, 2: -1}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_2_node_graph_1_repeated_edges(self):
        graph = Graph.from_edges([(1, 2, 7), (1, 2, 3)])
        expected = {1: 0, 2: 3}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_2_node_graph_1_repeated_edges_different_start(self):
        graph = Graph.from_edges([(1, 2, 7), (1, 2, 3)])
        expected = {1: 3, 2: 0}
        self.assertEqual(find_shortest_path(graph, start=2), expected)


    def test_2_node_graph_2_repeated_edges(self):
        graph = Graph.from_edges([(1, 2, 7), (1, 2, 5), (1, 2, 9)])
        expected = {1: 0, 2: 5}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_3_node_graph(self):
        graph = Graph.from_edges([(1, 2, 7), (2, 3, 5)])
        expected = {1: 0, 2: 7, 3: 12}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_3_node_graph_2_repeated_edges(self):
        graph = Graph.from_edges([(1, 2, 7), (1, 2, 8), (2, 3, 5), (2, 3, 3)])
        expected = {1: 0, 2: 7, 3: 10}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


    def test_3_node_graph_2_paths_to_last_node(self):
        graph = Graph.from_edges([(1, 2, 7), (1, 2, 8), (2, 3, 5), (2, 3, 3), (1, 3, 2)])
        expected = {1: 0, 2: 5, 3: 2}
        self.assertEqual(find_shortest_path(graph, start=1), expected)


def main():
    num_cases = int(input())
    for _ in range(num_cases):
        graph = Graph()
        _num_nodes, num_edges = [int(x) for x in input().split()]
        for _ in range(num_edges):
            vertex1, vertex2, cost = [int(x) for x in  input().split()]
            graph.add_edge(vertex1, vertex2, cost)
        start_vertex = int(input())
        answer = find_shortest_path(graph, start_vertex)
        answer_without_start = [(node, str(cost)) for node,cost in answer.items()
                                if node != start_vertex]
        print(" ".join([cost for _,cost in sorted(answer_without_start)]))

if __name__ == '__main__':
    unittest.main()
