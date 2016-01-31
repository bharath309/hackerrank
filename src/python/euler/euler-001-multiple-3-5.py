"""
# Project Euler #1: Multiples of 3 and 5

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below N.

Input Format
First line contains T that denotes the number of test cases. This is followed by T lines, each containing an integer, N.

Output Format
For each test case, print an integer that denotes the sum of all the multiples of 3 or 5 below N.

Constraints
1 ≤ T ≤ 10^5
1 ≤ N ≤ 10^9
"""

import unittest

def sum_to_n(n):
    return n * (n + 1) // 2

def euler_1(n):
    n -= 1
    num_3s = n // 3
    num_5s = n // 5
    num_15s = n // 15

    sum_3s = 3 * sum_to_n(num_3s)
    sum_5s = 5 * sum_to_n(num_5s)
    sum_15s = 15 * sum_to_n(num_15s)

    return sum_3s + sum_5s - sum_15s



class TestEuler1(unittest.TestCase):
    def test_empty(self):
        actual = euler_1(0)
        expected = 0
        self.assertEqual(actual, expected)


    def test_small(self):
        for i in range(3):
            self.assertEqual(euler_1(i), 0)

        self.assertEqual(euler_1(3), 0)
        self.assertEqual(euler_1(4), 3)
        self.assertEqual(euler_1(5), 3)
        self.assertEqual(euler_1(6), 8)
        self.assertEqual(euler_1(7), 14)
        self.assertEqual(euler_1(8), 14)
        self.assertEqual(euler_1(9), 14)
        self.assertEqual(euler_1(10), 23)
        self.assertEqual(euler_1(11), 33)
        self.assertEqual(euler_1(12), 33)


    def test_15(self):
        self.assertEqual(euler_1(14), 45)
        self.assertEqual(euler_1(15), 45)
        self.assertEqual(euler_1(16), 60)
        self.assertEqual(euler_1(17), 60)
        self.assertEqual(euler_1(18), 60)
        self.assertEqual(euler_1(19), 78)


def parse_input():
    num_cases = int(input())
    for _ in range(num_cases):
        n = int(input())
        print(euler_1(n))


if __name__ == '__main__':
    # unittest.main()
    parse_input()
