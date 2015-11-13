# https://www.hackerrank.com/challenges/maximise-sum
import math
import itertools
import random
import unittest
from fileinput import FileInput

# http://pythonsweetness.tumblr.com/post/45227295342/fast-pypy-compatible-ordered-map-in-89-lines-of
class SkipList(object):
    """Doubly linked non-indexable skip list, providing logarithmic insertion
    and deletion. Keys are any orderable Python object.

        `maxsize`:
            Maximum number of items expected to exist in the list. Performance
            will degrade when this number is surpassed.
    """
    def __init__(self, maxsize=65535):
        self.max_level = int(math.log(maxsize, 2))
        self.level = 0
        self.head = self._makeNode(self.max_level, None, None)
        self.nil = self._makeNode(-1, None, None)
        self.tail = self.nil
        self.head[3:] = [self.nil for x in range(self.max_level)]
        self._update = [self.head] * (1 + self.max_level)
        self.p = 1/math.e

    def _makeNode(self, level, key, value):
        node = [None] * (4 + level)
        node[0] = key
        node[1] = value
        return node

    def _randomLevel(self):
        lvl = 0
        max_level = min(self.max_level, self.level + 1)
        while random.random() < self.p and lvl < max_level:
            lvl += 1
        return lvl

    def items(self, searchKey=None, reverse=False):
        """Yield (key, value) pairs starting from `searchKey`, or the next
        greater key, or the end of the list. Subsequent iterations move
        backwards if `reverse=True`. If `searchKey` is ``None`` then start at
        either the beginning or end of the list."""
        if reverse:
            node = self.tail
        else:
            node = self.head[3]
        if searchKey is not None:
            update = self._update[:]
            found = self._findLess(update, searchKey)
            if found[3] is not self.nil:
                node = found[3]
        idx = 2 if reverse else 3
        while node[0] is not None:
            yield node[0], node[1]
            node = node[idx]

    def search_higher(self, value):
        result = next(self.items (value), (0, 0))[0]
        if result < value:
            result = 0
        return result

    def _findLess(self, update, searchKey):
        node = self.head
        for i in range(self.level, -1, -1):
            key = node[3 + i][0]
            while key is not None and key < searchKey:
                node = node[3 + i]
                key = node[3 + i][0]
            update[i] = node
        return node

    def insert(self, key):
        self._insert(key, key)

    def _insert(self, searchKey, value):
        """Insert `searchKey` into the list with `value`. If `searchKey`
        already exists, its previous value is overwritten."""
        assert searchKey is not None
        update = self._update[:]
        node = self._findLess(update, searchKey)
        prev = node
        node = node[3]
        if node[0] == searchKey:
            node[1] = value
        else:
            lvl = self._randomLevel()
            self.level = max(self.level, lvl)
            node = self._makeNode(lvl, searchKey, value)
            node[2] = prev
            for i in range(0, lvl+1):
                node[3 + i] = update[i][3 + i]
                update[i][3 + i] = node
            if node[3] is self.nil:
                self.tail = node
            else:
                node[3][2] = node

    def delete(self, searchKey):
        """Delete `searchKey` from the list, returning ``True`` if it
        existed."""
        update = self._update[:]
        node = self._findLess(update, searchKey)
        node = node[3]
        if node[0] == searchKey:
            node[3][2] = update[0]
            for i in range(self.level + 1):
                if update[i][3 + i] is not node:
                    break
                update[i][3 + i] = node[3 + i]
            while self.level > 0 and self.head[3 + self.level][0] is None:
                self.level -= 1
            if self.tail is node:
                self.tail = node[2]
            return True

    def search(self, searchKey):
        """Return the value associated with `searchKey`, or ``None`` if
        `searchKey` does not exist."""
        node = self.head
        for i in range(self.level, -1, -1):
            key = node[3 + i][0]
            while key is not None and key < searchKey:
                node = node[3 + i]
                key = node[3 + i][0]
        node = node[3]
        if node[0] == searchKey:
            return node[1]


class TestSkipList(unittest.TestCase):

    def test_single_elem(self):
        tree = SkipList()
        tree.insert(1)
        self.assertEqual(tree.search_higher(-2), 1)
        self.assertEqual(tree.search_higher(0), 1)
        self.assertEqual(tree.search_higher(3), 0)


    def test_two_elems(self):
        tree = SkipList()
        tree.insert(1)
        tree.insert(3)
        self.assertEqual(tree.search_higher(-2), 1)
        self.assertEqual(tree.search_higher(0), 1)
        self.assertEqual(tree.search_higher(2), 3)
        self.assertEqual(tree.search_higher(3), 3)
        self.assertEqual(tree.search_higher(4), 0)
        self.assertEqual(tree.search_higher(8), 0)



    def test_three_elems(self):
        tree = SkipList()
        tree.insert(7)
        tree.insert(12)
        tree.insert(2)
        self.assertEqual(tree.search_higher(-2), 2)
        self.assertEqual(tree.search_higher(0), 2)
        self.assertEqual(tree.search_higher(1), 2)
        self.assertEqual(tree.search_higher(2), 2)
        self.assertEqual(tree.search_higher(6), 7)
        self.assertEqual(tree.search_higher(7), 7)
        self.assertEqual(tree.search_higher(8), 12)
        self.assertEqual(tree.search_higher(11), 12)
        self.assertEqual(tree.search_higher(12), 12)
        self.assertEqual(tree.search_higher(13), 0)

    def test_three_elems_different_insert_order(self):
        tree = SkipList()
        elements = [7, 12, 2]

        for permutation in itertools.permutations(elements):
            tree = SkipList()
            for elem in permutation:
                tree.insert(elem)

            self.assertEqual(tree.search_higher(-2), 2)
            self.assertEqual(tree.search_higher(0), 2)
            self.assertEqual(tree.search_higher(1), 2)
            self.assertEqual(tree.search_higher(2), 2)
            self.assertEqual(tree.search_higher(6), 7)
            self.assertEqual(tree.search_higher(7), 7)
            self.assertEqual(tree.search_higher(8), 12)
            self.assertEqual(tree.search_higher(11), 12)
            self.assertEqual(tree.search_higher(12), 12)
            self.assertEqual(tree.search_higher(13), 0)


def maximise(array, m):
    sums_seen = SkipList(maxsize=10**14)
    sums_seen.insert(0)
    mod_running = 0
    best = 0
    for num in array:
        mod_running = (mod_running + num) % m
        sums_seen.insert(mod_running)
        goal = (mod_running + 1) % m
        nearest_goal = sums_seen.search_higher(goal)
        best = max(best, (mod_running - nearest_goal) % m)
    return best


class TestMaximise(unittest.TestCase):

    def test_single(self):
        a = [1]
        m = 2
        actual = maximise(a, m)
        expected = 1
        self.assertEqual(actual, expected)


    def test_single_overflow(self):
        a = [3]
        m = 2
        actual = maximise(a, m)
        expected = 1
        self.assertEqual(actual, expected)


    def test_example(self):
        self.assertEqual(maximise([3, 3, 9, 9, 5], 7), 6)


    def test_zeroes(self):
        self.assertEqual(maximise([0, 0, 0], 1), 0)
        self.assertEqual(maximise([0, 0, 0], 3), 0)


    def test_ones(self):
        self.assertEqual(maximise([1, 1, 1, 1], 1), 0)
        self.assertEqual(maximise([1, 1, 1, 1], 2), 1)
        self.assertEqual(maximise([1, 1, 1, 1], 3), 2)
        self.assertEqual(maximise([1, 1, 1, 1], 4), 3)

    def test_simple(self):
        self.assertEqual(maximise([5, 4], 7), 5)
        self.assertEqual(maximise([3, 1, 2], 7), 6)
        self.assertEqual(maximise([1, 1, 8], 7), 3)


def main():
    with FileInput("maximise_sum_input14.txt") as file:
        num_cases = int(file.readline())
        for _ in range(num_cases):
            size, mod = [int(x) for x in file.readline().split()]
            array = [int(x) for x in file.readline().split()]
            print(maximise(array, mod))


if __name__ == '__main__':
    main()
