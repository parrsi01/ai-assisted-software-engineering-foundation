"""
Module 03: Algorithms
Exercises — implement the function bodies.
"""
from functools import lru_cache


# Exercise 1: Binary search (iterative)
def binary_search(arr: list[int], target: int) -> int:
    """Return index of target in sorted arr, or -1 if not found. O(log n)."""
    pass


# Exercise 2: Bubble sort
def bubble_sort(arr: list) -> list:
    """Return a new sorted list using bubble sort. O(n²)."""
    pass


# Exercise 3: Insertion sort
def insertion_sort(arr: list) -> list:
    """Return a new sorted list using insertion sort."""
    pass


# Exercise 4: Merge sort
def merge_sort(arr: list) -> list:
    """Return a new sorted list using merge sort. O(n log n)."""
    pass


# Exercise 5: Quick sort
def quick_sort(arr: list) -> list:
    """Return a new sorted list using quick sort."""
    pass


# Exercise 6: Fibonacci — 3 approaches
def fibonacci_recursive(n: int) -> int:
    """Naive recursive Fibonacci. (Do not use for large n.)"""
    pass


def fibonacci_iterative(n: int) -> int:
    """Iterative Fibonacci. O(n) time, O(1) space."""
    pass


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """Memoized recursive Fibonacci using @lru_cache."""
    pass


# Exercise 7: Palindrome check
def is_palindrome(s: str) -> bool:
    """Return True if s is a palindrome (ignore non-alphanumeric, case-insensitive).
    is_palindrome("A man, a plan, a canal: Panama") -> True
    """
    pass


# Exercise 8: Anagram check
def is_anagram(s1: str, s2: str) -> bool:
    """Return True if s1 and s2 are anagrams."""
    pass


# Exercise 9: Staircase problem (DP)
def count_ways_stairs(n: int) -> int:
    """How many ways to climb n stairs taking 1 or 2 steps at a time?
    count_ways_stairs(4) -> 5  (1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2)
    """
    pass


# Exercise 10: Kadane's algorithm
def find_max_subarray(nums: list[int]) -> int:
    """Return the maximum contiguous subarray sum. O(n).
    find_max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6
    """
    pass


# Exercise 11: Binary search in rotated sorted array
def search_rotated(nums: list[int], target: int) -> int:
    """Search for target in a rotated sorted array. Return index or -1. O(log n).
    search_rotated([4, 5, 6, 7, 0, 1, 2], 0) -> 4
    """
    pass


if __name__ == "__main__":
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_arr = sorted(arr)
    assert binary_search(sorted_arr, 5) != -1
    for fn in [bubble_sort, insertion_sort, merge_sort, quick_sort]:
        assert fn(arr) == sorted_arr
    assert fibonacci_iterative(10) == 55
    assert is_palindrome("racecar")
    assert is_anagram("listen", "silent")
    assert count_ways_stairs(4) == 5
    assert find_max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    print("All assertions passed.")
