"""
Module 02: Data Structures — Solutions
"""
from __future__ import annotations
from collections import deque, OrderedDict
from typing import Any, Optional


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)  # O(1) amortized

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()  # O(1)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._data[-1]  # last element without removing

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)


class Queue:
    def __init__(self):
        # deque is O(1) for both append and popleft; list.pop(0) is O(n)
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def front(self):
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)


class ListNode:
    def __init__(self, val: Any, next: Optional[ListNode] = None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val: Any) -> None:
        new_node = ListNode(val)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:  # traverse to end
            current = current.next
        current.next = new_node  # O(n)

    def prepend(self, val: Any) -> None:
        self.head = ListNode(val, self.head)  # O(1)

    def delete(self, val: Any) -> bool:
        if self.head is None:
            return False
        if self.head.val == val:
            self.head = self.head.next  # special case: head is target
            return True
        current = self.head
        while current.next:
            if current.next.val == val:
                current.next = current.next.next  # skip the target node
                return True
            current = current.next
        return False

    def contains(self, val: Any) -> bool:
        current = self.head
        while current:
            if current.val == val:
                return True
            current = current.next
        return False

    def to_list(self) -> list:
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result


class BSTNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, val: int) -> None:
        self.root = self._insert(self.root, val)

    def _insert(self, node: Optional[BSTNode], val: int) -> BSTNode:
        if node is None:
            return BSTNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        # val == node.val: duplicates ignored
        return node

    def search(self, val: int) -> bool:
        return self._search(self.root, val)

    def _search(self, node: Optional[BSTNode], val: int) -> bool:
        if node is None:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def inorder(self) -> list[int]:
        result = []
        self._inorder(self.root, result)
        return result
        # Inorder (left → root → right) of a BST always produces sorted order

    def _inorder(self, node: Optional[BSTNode], result: list) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.val)
        self._inorder(node.right, result)


class HashTable:
    _DELETED = object()  # sentinel for deleted slots (tombstone)

    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.table: list = [None] * capacity
        self.size = 0

    def _hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def set(self, key: str, value: Any) -> None:
        idx = self._hash(key)
        for i in range(self.capacity):
            slot = (idx + i) % self.capacity  # linear probing
            entry = self.table[slot]
            if entry is None or entry is self._DELETED:
                self.table[slot] = (key, value)
                self.size += 1
                return
            if entry[0] == key:  # update existing key
                self.table[slot] = (key, value)
                return
        raise RuntimeError("Hash table is full")

    def get(self, key: str) -> Any:
        idx = self._hash(key)
        for i in range(self.capacity):
            slot = (idx + i) % self.capacity
            entry = self.table[slot]
            if entry is None:
                raise KeyError(key)
            if entry is not self._DELETED and entry[0] == key:
                return entry[1]
        raise KeyError(key)

    def delete(self, key: str) -> bool:
        idx = self._hash(key)
        for i in range(self.capacity):
            slot = (idx + i) % self.capacity
            entry = self.table[slot]
            if entry is None:
                return False
            if entry is not self._DELETED and entry[0] == key:
                self.table[slot] = self._DELETED  # tombstone, not None
                self.size -= 1
                return True
        return False

    def load_factor(self) -> float:
        return self.size / self.capacity


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None
    # Time: O(n), Space: O(n) — vs O(n²) brute force with no extra space


def reverse_list_inplace(lst: list) -> list:
    left, right = 0, len(lst) - 1
    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
    return lst


def max_subarray_sum(nums: list[int], k: int) -> int:
    if len(nums) < k:
        raise ValueError("k larger than array")
    window_sum = sum(nums[:k])  # initial window
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # slide: add right, remove left
        max_sum = max(max_sum, window_sum)
    return max_sum
    # O(n) — avoids O(n*k) recomputation of each window sum


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = OrderedDict()  # maintains insertion order

    def get(self, key: int) -> int:
        if key not in self._cache:
            return -1
        self._cache.move_to_end(key)  # mark as recently used
        return self._cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)  # evict least recently used (front)


if __name__ == "__main__":
    # Stack
    s = Stack()
    s.push(1); s.push(2)
    assert s.pop() == 2
    assert s.peek() == 1

    # Queue
    q = Queue()
    q.enqueue("a"); q.enqueue("b")
    assert q.dequeue() == "a"
    assert q.front() == "b"

    # Linked list
    ll = LinkedList()
    for v in [1, 2, 3]: ll.append(v)
    assert ll.to_list() == [1, 2, 3]
    ll.delete(2)
    assert ll.to_list() == [1, 3]
    assert ll.contains(3)
    assert not ll.contains(2)

    # BST
    bst = BST()
    for v in [5, 3, 7, 1, 4]: bst.insert(v)
    assert bst.inorder() == [1, 3, 4, 5, 7]
    assert bst.search(4) and not bst.search(9)

    # Two sum
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 3], 6) == (0, 1)

    # Sliding window
    assert max_subarray_sum([1, 2, 3, 4, 5], 3) == 12

    # LRU
    cache = LRUCache(2)
    cache.put(1, 1); cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)       # evicts key 2
    assert cache.get(2) == -1

    print("All assertions passed.")
