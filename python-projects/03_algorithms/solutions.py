"""
Module 03: Algorithms — Solutions
"""
from functools import lru_cache


# --- Searching ---

def binary_search(arr: list[int], target: int) -> int:
    """O(log n). Requires sorted array."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_recursive(arr: list[int], target: int, lo: int = 0, hi: int = None) -> int:
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, hi)
    else:
        return binary_search_recursive(arr, target, lo, mid - 1)


# --- Sorting ---

def bubble_sort(arr: list) -> list:
    """O(n²). Stable. Swaps adjacent elements."""
    arr = arr[:]  # don't mutate input
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(arr: list) -> list:
    """O(n²) worst, O(n) best (nearly sorted). Good for small/nearly-sorted arrays."""
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # shift right
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: list) -> list:
    """O(n log n). Stable. Divide and conquer."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list) -> list:
    """O(n log n) average, O(n²) worst. Not stable. In-place."""
    arr = arr[:]
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _quick_sort(arr: list, lo: int, hi: int) -> None:
    if lo < hi:
        p = _partition(arr, lo, hi)
        _quick_sort(arr, lo, p - 1)
        _quick_sort(arr, p + 1, hi)


def _partition(arr: list, lo: int, hi: int) -> int:
    pivot = arr[hi]  # last element as pivot
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# --- Recursion & Dynamic Programming ---

def fibonacci_recursive(n: int) -> int:
    """O(2^n) — exponential, for illustration only."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """O(n) time, O(1) space."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """O(n) time, O(n) space. @lru_cache adds memoization automatically."""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def is_palindrome(s: str) -> bool:
    """Ignores non-alphanumeric characters, case-insensitive."""
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def is_anagram(s1: str, s2: str) -> bool:
    """Return True if s1 and s2 are anagrams (same characters, different order)."""
    from collections import Counter
    return Counter(s1.lower()) == Counter(s2.lower())


def count_ways_stairs(n: int) -> int:
    """How many ways to climb n stairs taking 1 or 2 steps at a time?
    This is Fibonacci: ways(n) = ways(n-1) + ways(n-2)
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def find_max_subarray(nums: list[int]) -> int:
    """Kadane's algorithm: maximum subarray sum. O(n)."""
    max_ending_here = max_so_far = nums[0]
    for num in nums[1:]:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far


def search_rotated(nums: list[int], target: int) -> int:
    """Binary search in a rotated sorted array. O(log n)."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


if __name__ == "__main__":
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_arr = sorted(arr)

    assert binary_search(sorted_arr, 5) == sorted_arr.index(5)
    assert binary_search(sorted_arr, 99) == -1

    for sort_fn in [bubble_sort, insertion_sort, merge_sort, quick_sort]:
        assert sort_fn(arr) == sorted_arr, f"{sort_fn.__name__} failed"

    assert fibonacci_iterative(10) == 55
    assert fibonacci_memoized(10) == 55
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert is_anagram("listen", "silent")
    assert count_ways_stairs(5) == 8
    assert find_max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4

    print("All assertions passed.")
