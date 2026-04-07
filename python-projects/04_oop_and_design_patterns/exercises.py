"""
Module 04: OOP and Design Patterns
Exercises — implement the class bodies.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable


# Exercise 1: Basic class with dunder methods
class Animal:
    """Animal with name and sound. Implement speak(), __repr__, __eq__."""
    def __init__(self, name: str, sound: str):
        pass

    def speak(self) -> str:
        """'{name} says {sound}'"""
        pass

    def __repr__(self) -> str: pass
    def __eq__(self, other) -> bool: pass


class Dog(Animal):
    def __init__(self, name: str):
        pass  # hint: super().__init__(name, "woof")

    def fetch(self, item: str) -> str: pass


class Cat(Animal):
    def __init__(self, name: str): pass
    def purr(self) -> str: pass


# Exercise 2: Abstract base class
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...
    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float): pass
    def area(self) -> float: pass
    def perimeter(self) -> float: pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float): pass
    def area(self) -> float: pass
    def perimeter(self) -> float: pass


# Exercise 3: Properties and validation
class Temperature:
    """Celsius with Fahrenheit property. Reject < -273.15°C."""
    def __init__(self, celsius: float): pass

    @property
    def celsius(self) -> float: pass

    @celsius.setter
    def celsius(self, value: float): pass  # raise ValueError if below absolute zero

    @property
    def fahrenheit(self) -> float: pass  # formula: C * 9/5 + 32

    def __repr__(self) -> str: pass
    def __lt__(self, other: Temperature) -> bool: pass


# Exercise 4: Singleton pattern
class DatabaseConnection:
    """Only one instance can ever exist."""
    _instance = None
    def __new__(cls): pass
    def connect(self, url: str): pass


# Exercise 5: Factory pattern
class NotificationFactory:
    @staticmethod
    def create(notification_type: str, message: str):
        """Return Email/SMS/PushNotification based on type string."""
        pass


class Notification(ABC):
    def __init__(self, message: str): self.message = message
    @abstractmethod
    def send(self) -> str: ...

class EmailNotification(Notification):
    def send(self) -> str: pass

class SMSNotification(Notification):
    def send(self) -> str: pass

class PushNotification(Notification):
    def send(self) -> str: pass


# Exercise 6: Observer pattern
class EventEmitter:
    """on(event, callback), emit(event, *args), off(event, callback)"""
    def __init__(self): pass
    def on(self, event: str, callback: Callable) -> None: pass
    def emit(self, event: str, *args, **kwargs) -> None: pass
    def off(self, event: str, callback: Callable) -> None: pass


# Exercise 7: Strategy pattern
class Sorter:
    """Accepts a sort strategy (callable). sort(data) applies it."""
    def __init__(self, strategy: Callable[[list], list]): pass
    def sort(self, data: list) -> list: pass
    def set_strategy(self, strategy: Callable[[list], list]) -> None: pass


if __name__ == "__main__":
    import math
    assert Dog("Rex").speak() == "Rex says woof"
    assert Circle(5).area() == math.pi * 25
    assert Rectangle(4, 6).perimeter() == 20
    t = Temperature(0)
    assert t.fahrenheit == 32
    assert DatabaseConnection() is DatabaseConnection()
    n = NotificationFactory.create("sms", "hi")
    assert n.send() == "SMS: hi"
    emitter = EventEmitter()
    results = []
    emitter.on("x", lambda v: results.append(v))
    emitter.emit("x", 1)
    assert results == [1]
    print("All assertions passed.")
