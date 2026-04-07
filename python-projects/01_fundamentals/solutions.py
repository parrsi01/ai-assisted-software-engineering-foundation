"""
Module 01: Python Fundamentals — Solutions
"""
import json
import re
from pathlib import Path


def describe_type(value) -> str:
    return type(value).__name__


def reverse_words(sentence: str) -> str:
    return " ".join(sentence.split()[::-1])


def fizzbuzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
    # One-liner alternative:
    # return ["FizzBuzz" if i%15==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else str(i) for i in range(1,n+1)]


def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


def squares(n: int) -> list[int]:
    return [i ** 2 for i in range(1, n + 1)]


def word_count(text: str) -> dict[str, int]:
    # Strip punctuation using regex, lowercase, split
    words = re.sub(r"[^\w\s]", "", text.lower()).split()
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts
    # Alternative with Counter:
    # from collections import Counter
    # return dict(Counter(re.sub(r"[^\w\s]", "", text.lower()).split()))


def safe_divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b


def count_lines(filepath: str) -> int:
    try:
        with open(filepath, "r") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def fibonacci_gen(n: int):
    """Generator: yields n Fibonacci numbers without storing all in memory."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b  # simultaneous assignment avoids temp variable


def flatten(nested: list) -> list:
    """Recursive flatten. Handles arbitrary nesting depth."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))  # recurse into sublists
        else:
            result.append(item)
    return result


def format_table(rows: list[tuple]) -> str:
    if not rows:
        return ""
    max_name = max(len(r[0]) for r in rows)
    lines = []
    for name, score in rows:
        lines.append(f"{name:>{max_name}} | {score:>3}")
    return "\n".join(lines)


def sort_by_last_name(names: list[str]) -> list[str]:
    return sorted(names, key=lambda name: name.split()[-1])


def read_json_safe(filepath: str) -> dict | None:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def log_event(event_type: str, *args, **kwargs) -> str:
    parts = [str(a) for a in args]
    kv_parts = [f"{k}={v}" for k, v in kwargs.items()]
    all_parts = parts + kv_parts
    return f"{event_type}: {' | '.join(all_parts)}"


def power(base: int, exp: int) -> int:
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half  # fast exponentiation: O(log n) multiplications
    return base * power(base, exp - 1)


if __name__ == "__main__":
    assert describe_type(42) == "int"
    assert describe_type("hi") == "str"
    assert reverse_words("hello world") == "world hello"
    assert fizzbuzz(15)[-1] == "FizzBuzz"
    assert greet("Alice") == "Hello, Alice!"
    assert squares(5) == [1, 4, 9, 16, 25]
    assert word_count("the cat sat on the mat")["the"] == 2
    assert safe_divide(10, 0) is None
    assert safe_divide(10, 2) == 5.0
    assert list(fibonacci_gen(5)) == [0, 1, 1, 2, 3]
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert power(2, 10) == 1024
    assert sort_by_last_name(["Charlie Brown", "Alice Smith", "Bob Adams"]) == [
        "Bob Adams", "Charlie Brown", "Alice Smith"
    ]
    assert log_event("LOGIN", "alice", ip="10.0.0.1") == "LOGIN: alice | ip=10.0.0.1"
    print("All assertions passed.")
