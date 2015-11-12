# https://www.hackerrank.com/challenges/maximise-sum
import heapq
import itertools
import unittest

class LLRB(object):

    class Node(object):
        RED = True
        BLACK = False

        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
            self.color = LLRB.Node.RED


        def flip_colors(self):
            self.color = not self.color
            self.left.color = not self.left.color
            self.right.color = not self.right.color


    def __init__(self):
        self.root = None


    def search_lower(self, value):
        """Return an item less than or equal to value.  If no such value can be found,
        return 0.

        """
        x = self.root
        best = 0
        while x is not None:
            if x.value == value:
                return value
            elif x.value < value:
                best = max(best, x.value)
                x = x.left
            else:
                x = x.right

        return best


    @staticmethod
    def is_red(node):
        if node is None:
            return False
        else:
            return node.color == LLRB.Node.RED


    def insert(self, value):
        self.root = LLRB.insert_at(self.root, value)
        self.root.color = LLRB.Node.BLACK


    @staticmethod
    def insert_at(node, value):
        if node is None:
            return LLRB.Node(value)

        if LLRB.is_red(node.left) and LLRB.is_red(node.right):
            node.flip_colors()

        if node.value == value:
            node.value = value
        elif node.value < value:
            node.left = LLRB.insert_at(node.left, value)
        else:
            node.right = LLRB.insert_at(node.right, value)


        if LLRB.is_red(node.right) and not LLRB.is_red(node.left):
            node = LLRB.rotate_left(node)
        if LLRB.is_red(node.left) and LLRB.is_red(node.left.left):
            node = LLRB.rotate_right(node)

        return node


    @staticmethod
    def rotate_left(node):
        x = node.right
        node.right = x.left
        x.left = node
        x.color = node.color
        node.color = LLRB.Node.RED
        return x


    @staticmethod
    def rotate_right(node):
        x = node.left
        node.left = x.right
        x.right = node
        x.color = node.color
        node.color = LLRB.Node.RED
        return x


class TestLLRB(unittest.TestCase):

    def test_empty(self):
        tree = LLRB()
        self.assertIsNone(tree.root)


    def test_single_elem(self):
        tree = LLRB()
        tree.insert(1)
        self.assertEqual(tree.root.value, 1)
        self.assertEqual(tree.search_lower(3), 1)
        self.assertEqual(tree.search_lower(0), 0)
        self.assertEqual(tree.search_lower(-2), 0)


    def test_two_elems(self):
        tree = LLRB()
        tree.insert(1)
        tree.insert(3)
        self.assertEqual(tree.root.value, 1)
        self.assertEqual(tree.search_lower(3), 3)
        self.assertEqual(tree.search_lower(4), 3)
        self.assertEqual(tree.search_lower(8), 3)
        self.assertEqual(tree.search_lower(2), 1)
        self.assertEqual(tree.search_lower(0), 0)
        self.assertEqual(tree.search_lower(-2), 0)



    def test_three_elems(self):
        tree = LLRB()
        tree.insert(7)
        tree.insert(12)
        tree.insert(2)
        self.assertEqual(tree.search_lower(2), 2)
        self.assertEqual(tree.search_lower(6), 2)
        self.assertEqual(tree.search_lower(7), 7)
        self.assertEqual(tree.search_lower(8), 7)
        self.assertEqual(tree.search_lower(11), 7)
        self.assertEqual(tree.search_lower(12), 12)
        self.assertEqual(tree.search_lower(13), 12)

        self.assertEqual(tree.search_lower(0), 0)
        self.assertEqual(tree.search_lower(1), 0)
        self.assertEqual(tree.search_lower(-2), 0)


    def test_three_elems_different_insert_order(self):
        tree = LLRB()
        elements = [7, 12, 2]

        for permutation in itertools.permutations(elements):
            tree = LLRB()
            for elem in permutation:
                tree.insert(elem)

            self.assertEqual(tree.search_lower(2), 2)
            self.assertEqual(tree.search_lower(6), 2)
            self.assertEqual(tree.search_lower(7), 7)
            self.assertEqual(tree.search_lower(8), 7)
            self.assertEqual(tree.search_lower(11), 7)
            self.assertEqual(tree.search_lower(12), 12)
            self.assertEqual(tree.search_lower(13), 12)

            self.assertEqual(tree.search_lower(0), 0)
            self.assertEqual(tree.search_lower(1), 0)
            self.assertEqual(tree.search_lower(-2), 0)


def maximise(array, m):
    sums_seen = LLRB()
    sums_seen.insert(0)
    total = 0
    best = 0
    for num in array:
        total += num
        sum_mod = total % m
        sums_seen.insert(sum_mod)
        if total > m:
            sum_mod += m
        goal = max(sum_mod - (total  % m) - 1, 0)
        nearest_goal = sums_seen.search_lower(goal)
        best = max(best, total % m, (sum_mod - nearest_goal) % m)
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


def main():
    num_cases = int(input())
    for _ in range(num_cases):
        size,mod = [int(x) for x in input().split()]
        array = [int(x) for x in input().split()]
        print(maximise(array, mod))


if __name__ == '__main__':
    main()
