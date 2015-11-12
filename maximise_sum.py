# https://www.hackerrank.com/challenges/maximise-sum
import heapq
import unittest

def heap_lower_entry(heap, n):
    """Find the largest number less than or equal to n."""

    def find_lower(index):
        try:
            best = -1
            if heap[index] < n:
                best = heap[index]
            else:
                return -1
            return max(best,
                       find_lower(2 * index + 1),
                       find_lower(2 * index + 2))
        except IndexError:
            return -1
    return find_lower(0)

class TestHeapLower(unittest.TestCase):
    def test_empty(self):
        heap = []
        n = 3
        actual = heap_lower_entry(heap, n)
        expected = -1
        self.assertEqual(actual, expected)


    def test_single_miss(self):
        heap = [4]
        n = 3
        actual = heap_lower_entry(heap, n)
        expected = -1
        self.assertEqual(actual, expected)


    def test_single_hit(self):
        heap = [1]
        n = 3
        actual = heap_lower_entry(heap, n)
        expected = 1
        self.assertEqual(actual, expected)


    def test_double_hit_second(self):
        heap = [1, 9]
        n = 10
        actual = heap_lower_entry(heap, n)
        expected = 9
        self.assertEqual(actual, expected)


    def test_double_hit_first(self):
        heap = [1, 4]
        n = 3
        actual = heap_lower_entry(heap, n)
        expected = 1
        self.assertEqual(actual, expected)


    def test_double_hit_miss(self):
        heap = [5, 9]
        n = 4
        actual = heap_lower_entry(heap, n)
        expected = -1
        self.assertEqual(actual, expected)

def maximise(array, m):
    sums_seen = set()
    sum_max = 0
    sum_running = 0
    for num in array:
        running_sum = (running_sum + num) % m
        sums_seen.add(running_sum)

def main():
    num_cases = int(input())
    for _ in range(num_cases):
        size,mod = [int(x) for x in input().split()]
        array = [int(x) for x in input().split()]
        print(maximise(array, mod))


if __name__ == '__main__':
    unittest.main()
