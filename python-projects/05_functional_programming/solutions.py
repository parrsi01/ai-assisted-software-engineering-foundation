"""
Module 05: Functional Programming — Solutions
"""
from functools import reduce, partial, wraps
from typing import Callable, TypeVar, Iterable
import time

T = TypeVar("T")


# Higher-order functions
def apply_twice(f: Callable, x):
    """Apply f twice: f(f(x))"""
    return f(f(x))


def compose(*fns: Callable) -> Callable:
    """Compose functions right-to-left: compose(f, g, h)(x) == f(g(h(x)))"""
    def composed(x):
        result = x
        for fn in reversed(fns):
            result = fn(result)
        return result
    return composed


def pipe(*fns: Callable) -> Callable:
    """Pipe functions left-to-right: pipe(f, g, h)(x) == h(g(f(x)))"""
    def piped(x):
        result = x
        for fn in fns:
            result = fn(result)
        return result
    return piped


# Map, filter, reduce
def double_evens(nums: list[int]) -> list[int]:
    """Return doubled values of even numbers only."""
    return list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums)))


def product(nums: list[int]) -> int:
    """Product of all numbers using reduce."""
    return reduce(lambda a, b: a * b, nums, 1)


def flatten_map(lists: list[list]) -> list:
    """Flatten one level using reduce."""
    return reduce(lambda acc, lst: acc + lst, lists, [])


# Closures
def make_counter(start: int = 0):
    """Return a counter function that increments each call."""
    count = [start]  # mutable container to allow closure mutation

    def counter():
        count[0] += 1
        return count[0]

    return counter


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a function that multiplies its argument by factor."""
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier


# Decorators
def timer(fn: Callable) -> Callable:
    """Decorator that prints execution time."""
    @wraps(fn)  # preserves __name__ and __doc__ of fn
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts: int = 3, exceptions=(Exception,)):
    """Decorator factory: retry on exception up to max_attempts times."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}, retrying...")
        return wrapper
    return decorator


def memoize(fn: Callable) -> Callable:
    """Simple memoization decorator (dict-based cache)."""
    cache = {}

    @wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]

    wrapper.cache = cache  # expose cache for testing
    return wrapper


# Partial application
def add(a: int, b: int) -> int:
    return a + b


add5 = partial(add, 5)  # partial application: fix first argument


# Generators as functional tools
def take(n: int, iterable: Iterable):
    """Take first n elements from iterable."""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item


def infinite_counter(start: int = 0):
    """Infinite counter generator."""
    n = start
    while True:
        yield n
        n += 1


def chunk(lst: list, size: int):
    """Yield successive chunks of length size from lst."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


if __name__ == "__main__":
    # Higher-order
    assert apply_twice(lambda x: x + 1, 3) == 5
    pipeline = pipe(lambda x: x * 2, lambda x: x + 1, str)
    assert pipeline(5) == "11"

    # Map/filter/reduce
    assert double_evens([1, 2, 3, 4, 5, 6]) == [4, 8, 12]
    assert product([1, 2, 3, 4, 5]) == 120
    assert flatten_map([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]

    # Closures
    counter = make_counter(0)
    assert counter() == 1
    assert counter() == 2
    triple = make_multiplier(3)
    assert triple(7) == 21

    # Decorators
    @memoize
    def fib(n):
        return n if n <= 1 else fib(n - 1) + fib(n - 2)

    assert fib(10) == 55
    assert (0, ) in fib.cache

    # Partial
    assert add5(3) == 8

    # Generators
    assert list(take(3, infinite_counter(10))) == [10, 11, 12]
    assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    print("All assertions passed.")
