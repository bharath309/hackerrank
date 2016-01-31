from fileinput import FileInput
from collections import namedtuple
import io

BLACK = 1
WHITE = 0

class Node(object):
    def __init__(self, identifier=-1, color=-1, children=[]):
        self.identifier = identifier
        self.color = color
        self.children = children


    def __repr__(self):
        return "Node<id={}, color={}, children={}".format(
            self.identifier, self.color, self.children)


    def __str__(self):
        return "Node<id={}, color={}, children={}".format(
            self.identifier, self.color, self.children)


def find_longest_path(nodes):

    NodeResult = namedtuple("NodeResult", ['best', 'best_continuous'])

    def long_path(node):
        if not node.children:
            if node.color == BLACK:
                return NodeResult(best=1, best_continuous=1)
            else:
                return NodeResult(best=0, best_continuous=0)

        results = [long_path(child) for child in node.children]
        best = max(results, key=lambda result: result.best).best
        best_continuous = max(results, key=lambda result: result.best_continuous).best_continuous

        return NodeResult(best, best_continuous)

    result = long_path(nodes[0])
    return max(result.best, result.best_continuous)


def parse_tree(string):
    with io.StringIO(string) as input_file:
        num_nodes = int(input_file.readline())

        nodes = [Node(color=int(color)) for color in input_file.readline().split()]

        for i, node in enumerate(nodes):
            node.identifier = i


        parents = [int(x) for x in input_file.readline().split()]

        for i, parent in enumerate(parents):
            # problem is 1-indexed, but our array is not
            child_index = i + 1
            parent_index = parent - 1
            nodes[parent_index].children.append(nodes[child_index])

        return nodes



def main():
    with FileInput("-") as input_file:
        num_nodes = int(input_file.readline())

        nodes = [Node(identifier=-1, color=int(color), children=[]) for color in input_file.readline().split()]

        for i, node in enumerate(nodes):
            node.identifier = i


        parents = [int(x) for x in input_file.readline().split()]

        for i, parent in enumerate(parents):
            # problem is 1-indexed, but our array is not
            child_index = i + 1
            parent_index = parent - 1
            nodes[parent_index].children.add(nodes[child_index])

        print(find_longest_path(nodes))


def test_parse():
    input = """3
    1 1 1
    1 1
    """
    actual = parse_tree(input)

    node_2 = Node(2, BLACK)
    node_1 = Node(1, BLACK)
    node_0 = Node(0, 1, [node_1, node_2])
    expected = [node_0, node_1, node_2]

    assert expected == []


if __name__ == '__main__':
    main()
