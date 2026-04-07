"""
Module 09: Advanced Algorithms — Solutions
Dynamic programming, graph algorithms, Trie, Segment Tree, Union-Find
"""
from __future__ import annotations
from collections import defaultdict, deque
import heapq
from typing import Optional


# ============================================================
# DYNAMIC PROGRAMMING
# ============================================================

def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """0/1 Knapsack: maximize value without exceeding capacity.
    Each item can be taken at most once.
    Time: O(n * capacity), Space: O(n * capacity)
    """
    n = len(weights)
    # dp[i][w] = max value using items 0..i-1 with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]  # don't take item i
            if cap >= w:
                dp[i][cap] = max(dp[i][cap], dp[i - 1][cap - w] + v)  # take item i
    return dp[n][capacity]


def lcs(s1: str, s2: str) -> str:
    """Longest Common Subsequence. Returns the actual LCS string.
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to reconstruct the LCS
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1; j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(result))


def edit_distance(s1: str, s2: str) -> int:
    """Levenshtein edit distance: minimum insertions, deletions, substitutions.
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i  # delete all chars from s1
    for j in range(n + 1):
        dp[0][j] = j  # insert all chars of s2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # no operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete from s1
                    dp[i][j - 1],      # insert into s1
                    dp[i - 1][j - 1],  # substitute
                )
    return dp[m][n]


def coin_change(coins: list[int], amount: int) -> int:
    """Minimum number of coins to make amount. Return -1 if impossible.
    Time: O(amount * len(coins))
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1


def longest_increasing_subsequence(nums: list[int]) -> int:
    """LIS length using patience sorting. O(n log n)."""
    tails = []  # tails[i] = smallest tail of IS of length i+1
    for num in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < num:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(num)
        else:
            tails[lo] = num
    return len(tails)


# ============================================================
# GRAPH ALGORITHMS
# ============================================================

class Graph:
    """Weighted directed/undirected graph represented as adjacency list."""
    def __init__(self, directed: bool = True):
        self.adj: dict[int, list[tuple[int, float]]] = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def bfs(self, start: int) -> list[int]:
        """Breadth-first search. Returns nodes in BFS order."""
        visited = set()
        order = []
        queue = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: int) -> list[int]:
        """Depth-first search. Returns nodes in DFS order (iterative)."""
        visited = set()
        order = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor, _ in self.adj[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

    def dijkstra(self, start: int) -> dict[int, float]:
        """Dijkstra's shortest path from start to all reachable nodes.
        Time: O((V + E) log V) with a binary heap.
        """
        dist = defaultdict(lambda: float("inf"))
        dist[start] = 0
        heap = [(0, start)]  # (distance, node)
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue  # stale entry
            for v, weight in self.adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    heapq.heappush(heap, (dist[v], v))
        return dict(dist)

    def has_cycle_directed(self) -> bool:
        """Detect cycle in a directed graph using DFS coloring."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = defaultdict(int)

        def dfs(node):
            color[node] = GRAY
            for neighbor, _ in self.adj[node]:
                if color[neighbor] == GRAY:
                    return True  # back edge = cycle
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[node] = BLACK
            return False

        return any(
            color[node] == WHITE and dfs(node)
            for node in self.adj
        )

    def topological_sort(self) -> list[int]:
        """Kahn's algorithm (BFS-based). Returns topological order or [] if cycle."""
        in_degree = defaultdict(int)
        nodes = set(self.adj.keys())
        for u in self.adj:
            for v, _ in self.adj[u]:
                in_degree[v] += 1
                nodes.add(v)

        queue = deque(n for n in nodes if in_degree[n] == 0)
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return order if len(order) == len(nodes) else []


# ============================================================
# TRIE
# ============================================================

class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end = False


class Trie:
    """Prefix tree for efficient string insertion, search, and prefix matching."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if word is in the Trie."""
        node = self._traverse(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word starts with prefix."""
        return self._traverse(prefix) is not None

    def _traverse(self, s: str) -> Optional[TrieNode]:
        node = self.root
        for char in s:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def autocomplete(self, prefix: str) -> list[str]:
        """Return all words with the given prefix."""
        node = self._traverse(prefix)
        if node is None:
            return []
        results = []
        self._collect(node, prefix, results)
        return results

    def _collect(self, node: TrieNode, current: str, results: list) -> None:
        if node.is_end:
            results.append(current)
        for char, child in node.children.items():
            self._collect(child, current + char, results)


# ============================================================
# UNION-FIND (DISJOINT SET UNION)
# ============================================================

class UnionFind:
    """Union-Find with path compression and union by rank.
    Time: O(α(n)) per operation (effectively O(1)).
    """
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union x and y. Return False if already in same component."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


def count_islands(grid: list[list[str]]) -> int:
    """Count connected components of '1's in a binary grid.
    Uses Union-Find.
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                for dr, dc in [(0, 1), (1, 0)]:  # only need right and down
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        if uf.union(r * cols + c, nr * cols + nc):
                            count -= 1  # merged two islands
    return count


# ============================================================
# SEGMENT TREE
# ============================================================

class SegmentTree:
    """Range sum query with point updates. O(log n) per operation."""
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)
        # Build: leaf nodes at positions n..2n-1
        for i, v in enumerate(nums):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, idx: int, value: int) -> None:
        """Set nums[idx] = value."""
        pos = idx + self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def query(self, left: int, right: int) -> int:
        """Sum of nums[left..right] inclusive."""
        result = 0
        l, r = left + self.n, right + self.n + 1
        while l < r:
            if l & 1:  # l is right child
                result += self.tree[l]; l += 1
            if r & 1:  # r is right child (exclusive)
                r -= 1; result += self.tree[r]
            l //= 2; r //= 2
        return result


if __name__ == "__main__":
    # DP
    assert knapsack_01([1, 2, 3], [6, 10, 12], 5) == 22
    assert lcs("ABCBDAB", "BDCAB") == "BCAB"
    assert edit_distance("kitten", "sitting") == 3
    assert coin_change([1, 5, 10, 25], 41) == 4
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    # Graph
    g = Graph(directed=False)
    for u, v in [(1, 2), (1, 3), (2, 4), (3, 4)]:
        g.add_edge(u, v)
    assert set(g.bfs(1)) == {1, 2, 3, 4}

    wg = Graph(directed=True)
    for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)]:
        wg.add_edge(u, v, w)
    dist = wg.dijkstra(0)
    assert dist[3] == 4  # 0->2->1->3 = 1+2+1

    # Trie
    trie = Trie()
    for word in ["apple", "app", "application", "apply", "banana"]:
        trie.insert(word)
    assert trie.search("apple")
    assert not trie.search("ap")
    assert trie.starts_with("app")
    completions = trie.autocomplete("app")
    assert "apple" in completions and "apply" in completions

    # Union-Find
    uf = UnionFind(5)
    uf.union(0, 1); uf.union(1, 2)
    assert uf.connected(0, 2)
    assert not uf.connected(0, 3)
    assert uf.components == 3

    # Islands
    grid = [
        ["1", "1", "0", "0"],
        ["1", "1", "0", "0"],
        ["0", "0", "1", "0"],
        ["0", "0", "0", "1"],
    ]
    assert count_islands(grid) == 3

    # Segment tree
    st = SegmentTree([1, 3, 5, 7, 9, 11])
    assert st.query(1, 3) == 15  # 3+5+7
    st.update(1, 10)
    assert st.query(1, 3) == 22  # 10+5+7

    print("All assertions passed.")
