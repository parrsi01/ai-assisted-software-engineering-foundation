"""
Module 04: OOP and Design Patterns — Solutions
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable


# --- OOP Fundamentals ---

class Animal:
    def __init__(self, name: str, sound: str):
        self.name = name
        self._sound = sound  # convention: _ prefix = "protected"

    def speak(self) -> str:
        return f"{self.name} says {self._sound}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Animal) and self.name == other.name


class Dog(Animal):
    def __init__(self, name: str):
        super().__init__(name, "woof")  # super() avoids hardcoding parent class name

    def fetch(self, item: str) -> str:
        return f"{self.name} fetches the {item}!"


class Cat(Animal):
    def __init__(self, name: str):
        super().__init__(name, "meow")

    def purr(self) -> str:
        return f"{self.name} purrs..."


# Polymorphism: same interface, different behavior
def make_noise(animals: list[Animal]) -> list[str]:
    return [a.speak() for a in animals]


# --- Abstract Base Classes ---

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


# --- Properties and Dunder Methods ---

class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    def __repr__(self) -> str:
        return f"Temperature({self._celsius}°C)"

    def __lt__(self, other: Temperature) -> bool:
        return self._celsius < other._celsius

    def __add__(self, other: Temperature) -> Temperature:
        return Temperature(self._celsius + other._celsius)


# --- Design Patterns ---

# Singleton
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
        return cls._instance

    def connect(self, url: str):
        self.url = url
        self.connected = True


# Factory
class NotificationFactory:
    @staticmethod
    def create(notification_type: str, message: str):
        types = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification,
        }
        cls = types.get(notification_type.lower())
        if cls is None:
            raise ValueError(f"Unknown notification type: {notification_type}")
        return cls(message)


class Notification(ABC):
    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    def send(self) -> str: ...


class EmailNotification(Notification):
    def send(self) -> str:
        return f"Email: {self.message}"


class SMSNotification(Notification):
    def send(self) -> str:
        return f"SMS: {self.message}"


class PushNotification(Notification):
    def send(self) -> str:
        return f"Push: {self.message}"


# Observer
class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, *args, **kwargs) -> None:
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

    def off(self, event: str, callback: Callable) -> None:
        if event in self._listeners:
            self._listeners[event] = [cb for cb in self._listeners[event] if cb != callback]


# Strategy
class Sorter:
    def __init__(self, strategy: Callable[[list], list]):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy(data)

    def set_strategy(self, strategy: Callable[[list], list]) -> None:
        self._strategy = strategy


if __name__ == "__main__":
    # OOP
    animals = [Dog("Rex"), Cat("Whiskers")]
    assert make_noise(animals) == ["Rex says woof", "Whiskers says meow"]
    assert Dog("Rex") == Dog("Rex")
    assert Dog("Rex") != Dog("Buddy")

    # Shapes
    import math
    c = Circle(5)
    assert abs(c.area() - math.pi * 25) < 1e-9
    r = Rectangle(4, 6)
    assert r.area() == 24 and r.perimeter() == 20

    # Temperature
    t = Temperature(100)
    assert t.fahrenheit == 212
    try:
        t.celsius = -300
        assert False, "Should raise"
    except ValueError:
        pass

    # Singleton
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2

    # Factory
    n = NotificationFactory.create("email", "Hello")
    assert n.send() == "Email: Hello"

    # Observer
    emitter = EventEmitter()
    results = []
    emitter.on("data", lambda x: results.append(x))
    emitter.emit("data", 42)
    assert results == [42]

    # Strategy
    sorter = Sorter(sorted)
    assert sorter.sort([3, 1, 2]) == [1, 2, 3]
    sorter.set_strategy(lambda lst: sorted(lst, reverse=True))
    assert sorter.sort([3, 1, 2]) == [3, 2, 1]

    print("All assertions passed.")
