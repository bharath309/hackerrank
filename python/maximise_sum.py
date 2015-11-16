# https://www.hackerrank.com/challenges/maximise-sum
import itertools
from random import random
import unittest
from fileinput import FileInput
import unittest

# Profiling
# Baseline: 64.1s
# Without head and tail properties: 59.0s
# without next and dropwhile: 11.067s
# with self.level 17s
# only lists 8.8s
# inline ceiling 7.8s
# while loop for node_height: 5.9s


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

        node_height = 0
        while random() < 0.5:
            node_height += 1

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

def maximise(array, m):
    sums_seen = SkipList()
    sums_seen.insert(0)
    mod_running = 0
    best = 0
    for num in array:
        mod_running = (mod_running + num) % m
        sums_seen.insert(mod_running)
        goal = (mod_running + 1) % m
        nearest_goal = sums_seen.ceiling(goal)
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
