# https://www.hackerrank.com/challenges/maximise-sum
import unittest
from fileinput import FileInput


class Node(object):

    __slots__ = ['value', 'left', 'right', 'color']

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.color = True


    def flip_colors(self):
        self.color = not self.color
        self.left.color = not self.left.color
        self.right.color = not self.right.color


def insert_at(node, value):
    if node is None:
        return Node(value)

    if is_red(node.left) and is_red(node.right):
        node.flip_colors()

    if node.value == value:
        node.value = value
    elif node.value < value:
        node.left = insert_at(node.left, value)
    else:
        node.right = insert_at(node.right, value)


    if is_red(node.right) and not is_red(node.left):
        node = rotate_left(node)
    if is_red(node.left) and is_red(node.left.left):
        node = rotate_right(node)

    return node


def is_red(node):
    if node is None:
        return False
    else:
        return node.color == True


def rotate_left(node):
    x = node.right
    node.right = x.left
    x.left = node
    x.color = node.color
    node.color = True
    return x


def rotate_right(node):
    x = node.left
    node.left = x.right
    x.right = node
    x.color = node.color
    node.color = True
    return x

class LLRB(object):

    def __init__(self):
        self.root = None


    def search_higher(self, value):
        """Return the smallest item greater than or equal to value.  If no such value
        can be found, return 0.

        """
        x = self.root
        best = None
        while x is not None:
            if x.value == value:
                return value
            elif x.value < value:
                x = x.left
            else:
                best = x.value if best is None else min(best, x.value)
                x = x.right

        return 0 if best is None else best

    def insert(self, value):
        self.root = insert_at(self.root, value)
        self.root.color = False


class TestLLRB(unittest.TestCase):

    def test_empty(self):
        tree = LLRB()
        self.assertIsNone(tree.root)


    def test_single_elem(self):
        tree = LLRB()
        tree.insert(1)
        self.assertEqual(tree.root.value, 1)
        self.assertEqual(tree.search_higher(-2), 1)
        self.assertEqual(tree.search_higher(0), 1)
        self.assertEqual(tree.search_higher(3), 0)


    def test_two_elems(self):
        tree = LLRB()
        tree.insert(1)
        tree.insert(3)
        self.assertEqual(tree.root.value, 1)
        self.assertEqual(tree.search_higher(-2), 1)
        self.assertEqual(tree.search_higher(0), 1)
        self.assertEqual(tree.search_higher(2), 3)
        self.assertEqual(tree.search_higher(3), 3)
        self.assertEqual(tree.search_higher(4), 0)
        self.assertEqual(tree.search_higher(8), 0)



    def test_three_elems(self):
        tree = LLRB()
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

        self.assertTrue(tree.contains(2))
        self.assertTrue(tree.contains(7))
        self.assertTrue(tree.contains(12))
        self.assertFalse(tree.contains(13))



    def test_three_elems_different_insert_order(self):
        tree = LLRB()
        elements = [7, 12, 2]

        for permutation in itertools.permutations(elements):
            tree = LLRB()
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
    sums_seen = LLRB()
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
    with FileInput("-") as file:
        num_cases = int(file.readline())
        for _ in range(num_cases):
            size, mod = [int(x) for x in file.readline().split()]
            array = [int(x) for x in file.readline().split()]
            print(maximise(array, mod))


if __name__ == '__main__':
    main()
    # unittest.main()
