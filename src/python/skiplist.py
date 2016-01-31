from itertools import permutations, chain
import math
import numpy as np
from numpy.random import geometric as np_geometric
import unittest
from ipdb import launch_ipdb_on_exception

# Profiling
# Baseline: 64.1s
# Without head and tail properties: 59.0s
# without next and dropwhile: 11.067s
# with self.level 17s
# only lists 8.8s
# inline ceiling 7.8s


class SkipList(object):

    def __init__(self):
        self.tail = [2**63 - 1]
        self.head = [-2**31, self.tail]


    def find_lower(self, search_data, update):
        height = len(self.head)
        node = self.head
        for level in range(height - 1, 0, -1):
            next_node = node[level]

            # 0 is index for data
            while next_node[0] < search_data:
                node = next_node
                next_node = node[level]

            # update doesn't have a 0 element data
            update[level - 1] = node

        return node


    def insert(self, data):
        """Inserts data into appropriate position."""

        # Subtract 1 because first elem of head is data
        height = len(self.head) - 1

        # update is an out-parameter from find_lower
        update = [None] * height
        node = self.find_lower(data, update)

        node_height = np_geometric(p=0.5)

        # Add new levels if node_height > head
        for _ in range(node_height - height):
            self.head.append(self.tail)
            update.append(self.head)

        new_node = [data]
        for i in range(node_height):
            # Add next levels from update
            new_node.append(update[i][i+1])

        for level in range(node_height):
            # Point update levels at new_node
            update[level][level + 1] = new_node

    def ceiling(self, search_data):
        """Returns the least element greater than or equal to `elem`, or 0 if no such
element exists.

        """
        height = len(self.head)
        node = self.head
        for level in range(height - 1, 0, -1):
            next_node = node[level]

            # 0 is index for data
            while next_node[0] < search_data:
                node = next_node
                next_node = node[level]

        candidate = node[1]
        if candidate is not self.tail:
            return candidate[0]
        else:
            return 0


    def _level(self, start=None, level=0):
        node = start or self.head[level+1]
        while node is not self.tail:
            yield node
            node = node[level+1]

    def pprint(self):
        max_height = len(self.head.nxt)
        active_heights = set(range(max_height))
        pic_height = max_height * 2 + 1
        skip_pic = [''] * pic_height

        all_nodes = chain([SkipNode('HEAD', self.head.nxt)],
                          list(self._level()),
                          [SkipNode("TAIL", self.head.nxt)]
                          )

        for node in all_nodes:
            node_pic = [''] * pic_height

            # Draw x-axis
            node_pic[pic_height - 1] = str(node.data).ljust(13)

            for r in range(len(node.nxt)):
                active_heights.add(r)

            for row in range(max_height):
                row_idx = pic_height - 1 - (2 * row + 2)
                spacer_idx = pic_height - 1 - (2 * row + 1)
                row_height = len(node.nxt)

                if row < row_height:
                    node_pic[row_idx] += 'o'
                    node_pic[spacer_idx] += '|'

                else:
                    node_pic[row_idx] += '-'
                    node_pic[spacer_idx] += ' '

                if node.data != 'TAIL':
                    node_pic[row_idx] += '-' * 12
                    node_pic[spacer_idx] += ' ' * 12


            skip_pic = [skip_pic[i] + s for i,s in enumerate(node_pic)]

        for row in skip_pic:
            print(row)




    def __str__(self):
        return 'skiplist({{{}}})'.format(
            ', '.join('{value}[{size}]'.format(value=node.data, size=len(node.nxt)) for node in self._level())
        )


class TestSkipList(unittest.TestCase):

    def test_single_elem(self):
        tree = SkipList()
        tree.insert(1)
        self.assertEqual(tree.ceiling(-2), 1)
        self.assertEqual(tree.ceiling(0), 1)
        self.assertEqual(tree.ceiling(3), 0)


    def test_two_elems(self):
        tree = SkipList()
        tree.insert(1)
        tree.insert(3)
        self.assertEqual(tree.ceiling(-2), 1)
        self.assertEqual(tree.ceiling(0), 1)
        self.assertEqual(tree.ceiling(2), 3)
        self.assertEqual(tree.ceiling(3), 3)
        self.assertEqual(tree.ceiling(4), 0)
        self.assertEqual(tree.ceiling(8), 0)



    def test_three_elems(self):
        tree = SkipList()
        tree.insert(7)
        tree.insert(12)
        tree.insert(2)
        self.assertEqual(tree.ceiling(-2), 2)
        self.assertEqual(tree.ceiling(0), 2)
        self.assertEqual(tree.ceiling(1), 2)
        self.assertEqual(tree.ceiling(2), 2)
        self.assertEqual(tree.ceiling(6), 7)
        self.assertEqual(tree.ceiling(7), 7)
        self.assertEqual(tree.ceiling(8), 12)
        self.assertEqual(tree.ceiling(11), 12)
        self.assertEqual(tree.ceiling(12), 12)
        self.assertEqual(tree.ceiling(13), 0)

    def test_three_elems_different_insert_order(self):
        tree = SkipList()
        elements = [7, 12, 2]

        for permutation in permutations(elements):
            tree = SkipList()
            for elem in permutation:
                tree.insert(elem)

            self.assertEqual(tree.ceiling(-2), 2)
            self.assertEqual(tree.ceiling(0), 2)
            self.assertEqual(tree.ceiling(1), 2)
            self.assertEqual(tree.ceiling(2), 2)
            self.assertEqual(tree.ceiling(6), 7)
            self.assertEqual(tree.ceiling(7), 7)
            self.assertEqual(tree.ceiling(8), 12)
            self.assertEqual(tree.ceiling(11), 12)
            self.assertEqual(tree.ceiling(12), 12)
            self.assertEqual(tree.ceiling(13), 0)


if __name__ == '__main__':
    l = SkipList()
    l.insert(4)
    l.insert(5)
    l.insert(5)
    l.insert(5)
    l.insert(5)
    l.insert(6)
    l.pprint()
