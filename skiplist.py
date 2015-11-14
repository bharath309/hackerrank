from itertools import chain, takewhile, dropwhile, permutations
import numpy as np
from numpy.random import geometric as np_geometric
import unittest

# Profiling
# Baseline: 64.1s
# Without head and tail properties: 59.0s


class SkipNode(object):
    __slots__ = ('data', 'nxt', 'prev')

    def __init__(self, data, nxt, prev):
        self.data = data
        self.nxt = nxt
        self.prev = prev

        for level in range(len(prev)):
            prev[level].nxt[level] = self.nxt[level].prev[level] = self

class SkipList(object):

    def __init__(self):

        self.tail = SkipNode(2**32 - 1, [], [])
        self.head = SkipNode(-2**31, [self.tail], [])
        self.tail.prev.extend([self.head])


    def _level(self, start=None, level=0):
        node = start or self.head.nxt[level]
        while node is not self.tail:
            yield node
            node = node.nxt[level]

    def _scan(self, search_data, update):
        height = len(self.head.nxt)
        update = [self.head] * height
        # start = self.head.nxt[-1]
        node = self.head
        # print("SCANNING")
        # print("  Scanning {}".format(self))
        for level in range(height - 1, -1, -1):
            # print("  Level {}".format(level))
            node_data = node.data
            while node_data < search_data:
                # print("  at Node {}".format(node.data))
                node = node.nxt[level]
                node_data = node.data
            update[level] = node

        return node

    def ceiling(self, data):
        """Returns the least element greater than or equal to `elem`, or 0 if no such
element exists."""
        _update = [None] * len(self.head.nxt)
        node = self._scan(data, _update)

        if node:
            return data

        result = update[0].nxt[0]
        if result is self.tail:
            return 0
        else:
            return result.data

    def pprint(self):
        max_height = len(self.head.nxt)
        active_heights = set(range(max_height))
        pic_height = max_height * 2 + 1
        skip_pic = [''] * pic_height

        all_nodes = chain([SkipNode('HEAD', self.head.nxt, [])],
                          list(self._level()),
                          [SkipNode("TAIL", self.tail.prev, [])]
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


    def insert(self, data):
        """Inserts data into appropriate position."""

        node_height = np_geometric(p=0.5)
        # Maybe optimize, by only adding one new level.
        update = [self.head for _ in range(max(node_height, len(self.head.nxt)))]
        node = self._scan(data, update)
        # print("INSERTING")
        # print("  inserting after {}".format(node.data))

        # if node's height is greater than number of levels
        # then add new levels, if not do nothing
        height = len(self.head.nxt)

        update.extend([self.head for _ in range(height, node_height)])

        self.head.nxt.extend([self.tail for _ in range(height, node_height)])

        self.tail.prev.extend([self.head for _ in range(height, node_height)])

        new_node = SkipNode(data,
                            nxt=[update[l].nxt[l] for l in range(node_height)],
                            prev=[update[l] for l in range(node_height)])

        for level in range(node_height):
            update[level].nxt[level] = new_node


    def __str__(self):
        return 'skiplist({{{}}})'.format(
            ', '.join('{value}[{size}]'.format(value=node.data, size=len(node.nxt)) for node in self._level())
        )


class TestSkipList(unittest.TestCase):

    def test_single_elem(self):
        tree = SkipList()
        tree.insert(1)
        self.assertEqual(tree.ceiling(-2), 1)
        # self.assertEqual(tree.ceiling(0), 1)
        # self.assertEqual(tree.ceiling(3), 0)


    # def test_two_elems(self):
    #     tree = SkipList()
    #     tree.insert(1)
    #     tree.insert(3)
    #     self.assertEqual(tree.ceiling(-2), 1)
    #     self.assertEqual(tree.ceiling(0), 1)
    #     self.assertEqual(tree.ceiling(2), 3)
    #     self.assertEqual(tree.ceiling(3), 3)
    #     self.assertEqual(tree.ceiling(4), 0)
    #     self.assertEqual(tree.ceiling(8), 0)



    # def test_three_elems(self):
    #     tree = SkipList()
    #     tree.insert(7)
    #     tree.insert(12)
    #     tree.insert(2)
    #     self.assertEqual(tree.ceiling(-2), 2)
    #     self.assertEqual(tree.ceiling(0), 2)
    #     self.assertEqual(tree.ceiling(1), 2)
    #     self.assertEqual(tree.ceiling(2), 2)
    #     self.assertEqual(tree.ceiling(6), 7)
    #     self.assertEqual(tree.ceiling(7), 7)
    #     self.assertEqual(tree.ceiling(8), 12)
    #     self.assertEqual(tree.ceiling(11), 12)
    #     self.assertEqual(tree.ceiling(12), 12)
    #     self.assertEqual(tree.ceiling(13), 0)

    # def test_three_elems_different_insert_order(self):
    #     tree = SkipList()
    #     elements = [7, 12, 2]

    #     for permutation in permutations(elements):
    #         tree = SkipList()
    #         for elem in permutation:
    #             tree.insert(elem)

    #         self.assertEqual(tree.ceiling(-2), 2)
    #         self.assertEqual(tree.ceiling(0), 2)
    #         self.assertEqual(tree.ceiling(1), 2)
    #         self.assertEqual(tree.ceiling(2), 2)
    #         self.assertEqual(tree.ceiling(6), 7)
    #         self.assertEqual(tree.ceiling(7), 7)
    #         self.assertEqual(tree.ceiling(8), 12)
    #         self.assertEqual(tree.ceiling(11), 12)
    #         self.assertEqual(tree.ceiling(12), 12)
    #         self.assertEqual(tree.ceiling(13), 0)


if __name__ == '__main__':
    l = SkipList()
    l.insert(4)
    l.insert(5)
    l.insert(5)
    l.insert(5)
    l.insert(5)
    l.insert(6)
    l.pprint()
