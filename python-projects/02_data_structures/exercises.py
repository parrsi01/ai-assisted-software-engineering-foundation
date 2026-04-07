"""
Module 02: Data Structures
Exercises — implement the classes and functions.
"""
from __future__ import annotations
from typing import Any, Optional


# Exercise 1: Stack using a list
class Stack:
    """LIFO stack. push(), pop(), peek(), is_empty(), size()"""
    def push(self, item): pass
    def pop(self): pass          # raise IndexError if empty
    def peek(self): pass         # raise IndexError if empty
    def is_empty(self) -> bool: pass
    def size(self) -> int: pass


# Exercise 2: Queue using collections.deque
class Queue:
    """FIFO queue. enqueue(), dequeue(), front(), is_empty(), size()"""
    def enqueue(self, item): pass
    def dequeue(self): pass      # raise IndexError if empty
    def front(self): pass        # raise IndexError if empty
    def is_empty(self) -> bool: pass
    def size(self) -> int: pass


# Exercise 3: Singly linked list node and list
class ListNode:
    def __init__(self, val: Any, next: Optional[ListNode] = None):
        self.val = val
        self.next = next


class LinkedList:
    """Singly linked list with append, prepend, delete, contains, to_list."""
    def __init__(self): self.head = None

    def append(self, val: Any) -> None:
        """Add val to the end."""
        pass

    def prepend(self, val: Any) -> None:
        """Add val to the front."""
        pass

    def delete(self, val: Any) -> bool:
        """Remove first occurrence of val. Return True if found, False otherwise."""
        pass

    def contains(self, val: Any) -> bool:
        """Return True if val is in the list."""
        pass

    def to_list(self) -> list:
        """Return all values as a Python list."""
        pass


# Exercise 4: Binary Search Tree
class BSTNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BST:
    """Binary search tree: insert, search, inorder traversal."""
    def __init__(self): self.root = None

    def insert(self, val: int) -> None:
        """Insert val maintaining BST property."""
        pass

    def search(self, val: int) -> bool:
        """Return True if val exists in the tree."""
        pass

    def inorder(self) -> list[int]:
        """Return values in sorted (inorder) traversal."""
        pass


# Exercise 5: Hash table (open addressing with linear probing)
class HashTable:
    """Fixed-size hash table. set(), get(), delete(), load_factor()."""
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0

    def _hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def set(self, key: str, value: Any) -> None:
        """Insert or update key-value pair."""
        pass

    def get(self, key: str) -> Any:
        """Return value for key, raise KeyError if not found."""
        pass

    def delete(self, key: str) -> bool:
        """Remove key. Return True if found."""
        pass

    def load_factor(self) -> float:
        """Return size / capacity."""
        pass


# Exercise 6: Two-pointer problems
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indices (i, j) where nums[i] + nums[j] == target, or None.
    Use a dict for O(n) solution.
    """
    pass


def reverse_list_inplace(lst: list) -> list:
    """Reverse a list in-place using two pointers. Return the same list."""
    pass


# Exercise 7: Sliding window
def max_subarray_sum(nums: list[int], k: int) -> int:
    """Return the maximum sum of any contiguous subarray of length k."""
    pass


# Exercise 8: LRU Cache
class LRUCache:
    """Least Recently Used cache. get(key), put(key, value). O(1) for both.
    Hint: use collections.OrderedDict
    """
    def __init__(self, capacity: int):
        self.capacity = capacity

    def get(self, key: int) -> int:
        """Return value or -1 if not present."""
        pass

    def put(self, key: int, value: int) -> None:
        """Insert or update. Evict LRU if at capacity."""
        pass


if __name__ == "__main__":
    # Stack
    s = Stack()
    s.push(1); s.push(2)
    assert s.pop() == 2
    assert s.peek() == 1
    assert s.size() == 1

    # Queue
    q = Queue()
    q.enqueue("a"); q.enqueue("b")
    assert q.dequeue() == "a"

    # Linked list
    ll = LinkedList()
    ll.append(1); ll.append(2); ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    ll.delete(2)
    assert ll.to_list() == [1, 3]

    # BST
    bst = BST()
    for v in [5, 3, 7, 1, 4]:
        bst.insert(v)
    assert bst.inorder() == [1, 3, 4, 5, 7]
    assert bst.search(4) is True
    assert bst.search(9) is False

    # Two sum
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)

    print("All assertions passed.")
