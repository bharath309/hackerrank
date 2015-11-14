# https://www.hackerrank.com/challenges/maximise-sum
import math
import itertools
import random
import unittest
from fileinput import FileInput
from skiplist import SkipList


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
    with FileInput("maximise_sum_input14.txt") as file:
        num_cases = int(file.readline())
        for _ in range(num_cases):
            size, mod = [int(x) for x in file.readline().split()]
            array = [int(x) for x in file.readline().split()]
            print(maximise(array, mod))


if __name__ == '__main__':
    main()
