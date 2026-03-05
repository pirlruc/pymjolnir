"""pymjolnir - Design patterns Python library.

This package provides clean, modern implementations of common design patterns
using Python best practices and Pydantic for data validation.

Available patterns:
    - Factory: Create objects without specifying the exact class.
    - Singleton: Ensure a class has only one instance.

Example:
    >>> from pymjolnir import ProductFactory, ProductType
    >>> circle = ProductFactory.create(ProductType.CIRCLE, radius=5.0)
    >>> print(circle.area())

    >>> from pymjolnir import SingletonMeta
    >>> class MyConfig(metaclass=SingletonMeta):
    ...     pass
"""

from __future__ import annotations

from pymjolnir.factory import ProductBase, ProductFactory, ProductType
from pymjolnir.singleton import SingletonMeta

__version__ = "0.1.0"
__author__ = "pymjolnir"

__all__ = [
    "ProductFactory",
    "ProductBase",
    "ProductType",
    "SingletonMeta",
]
