"""
Module 01: Python Fundamentals
Exercises — implement the function bodies.
"""


# Exercise 1: Variables and types
def describe_type(value) -> str:
    """Return the type name of value as a string. E.g. describe_type(42) -> 'int'"""
    pass


# Exercise 2: String operations
def reverse_words(sentence: str) -> str:
    """Reverse the order of words in a sentence.
    E.g. reverse_words("hello world") -> "world hello"
    """
    pass


# Exercise 3: Control flow
def fizzbuzz(n: int) -> list[str]:
    """Return list of strings 1..n where multiples of 3 are 'Fizz',
    multiples of 5 are 'Buzz', multiples of both are 'FizzBuzz'.
    """
    pass


# Exercise 4: Functions and default arguments
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting string. greet('Alice') -> 'Hello, Alice!'"""
    pass


# Exercise 5: List comprehension
def squares(n: int) -> list[int]:
    """Return list of squares from 1 to n inclusive using a list comprehension."""
    pass


# Exercise 6: Dictionary operations
def word_count(text: str) -> dict[str, int]:
    """Count occurrences of each word in text (case-insensitive, ignore punctuation).
    word_count("the cat sat on the mat") -> {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
    """
    pass


# Exercise 7: Error handling
def safe_divide(a: float, b: float) -> float | None:
    """Return a / b, or None if b is zero. Never raise an exception."""
    pass


# Exercise 8: File I/O
def count_lines(filepath: str) -> int:
    """Return the number of lines in a file. Return 0 if file doesn't exist."""
    pass


# Exercise 9: Generator
def fibonacci_gen(n: int):
    """Yield the first n Fibonacci numbers. fibonacci_gen(5) -> 0, 1, 1, 2, 3"""
    pass


# Exercise 10: Nested data structures
def flatten(nested: list) -> list:
    """Flatten a nested list of arbitrary depth.
    flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]
    """
    pass


# Exercise 11: String formatting
def format_table(rows: list[tuple]) -> str:
    """Format a list of (name, score) tuples as a right-aligned table.
    Input: [('Alice', 95), ('Bob', 87)]
    Output:
    Alice |  95
      Bob |  87
    """
    pass


# Exercise 12: Lambda and sorting
def sort_by_last_name(names: list[str]) -> list[str]:
    """Sort a list of 'First Last' names by last name.
    sort_by_last_name(['Charlie Brown', 'Alice Smith', 'Bob Adams']) -> ['Bob Adams', 'Charlie Brown', 'Alice Smith']
    """
    pass


# Exercise 13: Context manager
def read_json_safe(filepath: str) -> dict | None:
    """Read a JSON file and return its contents as a dict.
    Return None if file doesn't exist or JSON is invalid.
    Use a context manager (with open(...)) for file handling.
    """
    pass


# Exercise 14: *args and **kwargs
def log_event(event_type: str, *args, **kwargs) -> str:
    """Format an event log entry.
    log_event('LOGIN', 'alice', ip='10.0.0.1') -> 'LOGIN: alice | ip=10.0.0.1'
    """
    pass


# Exercise 15: Recursive function
def power(base: int, exp: int) -> int:
    """Compute base^exp using recursion (no ** operator).
    power(2, 10) -> 1024
    """
    pass


if __name__ == "__main__":
    # Quick self-tests — uncomment as you implement each exercise
    print(describe_type(42))          # int
    print(reverse_words("hello world"))  # world hello
    print(fizzbuzz(15))
    print(greet("Alice"))             # Hello, Alice!
    print(squares(5))                 # [1, 4, 9, 16, 25]
    print(word_count("the cat sat on the mat"))
    print(safe_divide(10, 0))         # None
    print(list(fibonacci_gen(8)))     # [0, 1, 1, 2, 3, 5, 8, 13]
    print(flatten([1, [2, [3, 4]], 5]))  # [1, 2, 3, 4, 5]
    print(power(2, 10))               # 1024
