from itertools import chain, takewhile, dropwhile, permutations
import numpy as np
import unittest

class NIL(object):
    """Sentinel object that always compares greater than another object"""
    __slots__ = ()

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __eq__(self, other):
        return False

    def __str__(self):
        return 'NIL'

    def __nonzero__(self):
        return False

class SkipNode(object):
    __slots__ = ('data', 'nxt', 'prev')

    def __init__(self, data, nxt, prev):
        self.data = data
        self.nxt = nxt
        self.prev = prev

        for level in range(len(prev)):
            prev[level].nxt[level] = self.nxt[level].prev[level] = self

class SkipList(object):

    def _height(self):
        return len(self.head.nxt)

    def _level(self, start=None, level=0):
        node = start or self.head.nxt[level]
        while node is not self.tail:
            yield node
            node = node.nxt[level]

    def _scan(self, data):
        return_value = None
        height = len(self.head.nxt)
        prevs = [self.head] * height
        start = self.head.nxt[-1]
        for level in reversed(range(height)):
            node = next(
                dropwhile(
                    lambda node_: node_.nxt[level].data <= data,
                    chain([self.head], self._level(start, level))
                )
            )
            if node.data == data:
                return_value = node
            else:
                prevs[level] = node
                # do not need to scan from the head again, so start from this node at the lower level
                start = node.nxt[level - 1].prev[level - 1]

        return return_value, prevs

    def ceiling(self, data):
        """Returns the least element greater than or equal to `elem`, or 0 if no such
element exists."""

        node, update = self._scan(data)

        if node:
            return data

        result = update[0].nxt[0]
        if result is self.tail:
            return 0
        else:
            return result.data


    def insert(self, data):
        """Inserts data into appropriate position."""

        node, update = self._scan(data)

        # The node was found, don't do anything
        if node:
            return

        node_height = np.random.geometric(p=0.5)
        # if node's height is greater than number of levels
        # then add new levels, if not do nothing
        height = len(self.head.nxt)

        # Maybe optimize, by only adding one new level.
        update.extend([self.head for _ in range(height, node_height)])

        self.head.nxt.extend([self.tail for _ in range(height, node_height)])

        self.tail.prev.extend([self.head for _ in range(height, node_height)])

        new_node = SkipNode(data,
                            nxt=[update[l].nxt[l] for l in range(node_height)],
                            prev=[update[l] for l in range(node_height)])

        for level in range(node_height):
            update[level].nxt[level] = new_node


        self._size += 1

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def __init__(self, **kwargs):

        self._tail = SkipNode(NIL(), [], [])
        self._head = SkipNode(None, [self.tail], [])
        self._tail.prev.extend([self.head])

        self._size = 0

        for k, v in kwargs.items():
            self[k] = v

    def __len__(self):
        return self._size

    def __str__(self):
        return 'skiplist({{{}}})'.format(
            ', '.join('{value}'.format(value=node.data) for node in self._level())
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
