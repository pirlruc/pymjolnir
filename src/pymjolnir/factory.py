"""Factory design pattern implementation using Pydantic.

This module provides a flexible Factory pattern that allows creating
geometric shape objects (products) without coupling the caller to
concrete product classes. Products are registered in a central registry
and instantiated via :class:`ProductFactory`.

Example:
    >>> from pymjolnir.factory import ProductFactory, ProductType
    >>> circle = ProductFactory.create(ProductType.CIRCLE, radius=3.0)
    >>> print(circle.area())
    28.274333882308138
    >>> print(circle.describe())
    I am a Circle
"""

from __future__ import annotations

import math
from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator


class ProductType(Enum):
    """Enumeration of supported product types.

    Attributes:
        CIRCLE: Represents a circular shape.
        RECTANGLE: Represents a rectangular shape.
        TRIANGLE: Represents a triangular shape.
    """

    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    TRIANGLE = "triangle"


class ProductBase(BaseModel):
    """Abstract base model for all factory products.

    All concrete product classes should inherit from this class and
    implement the :meth:`area` and :meth:`perimeter` methods.

    Attributes:
        name: Human-readable name of the product.
    """

    name: str

    def area(self) -> float:
        """Calculate and return the area of the product.

        Returns:
            The area as a float.

        Raises:
            NotImplementedError: If the subclass has not implemented this method.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement area()")

    def perimeter(self) -> float:
        """Calculate and return the perimeter of the product.

        Returns:
            The perimeter as a float.

        Raises:
            NotImplementedError: If the subclass has not implemented this method.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement perimeter()")

    def describe(self) -> str:
        """Return a human-readable description of the product.

        Returns:
            A string of the form ``"I am a <name>"``.
        """
        return f"I am a {self.name}"


class CircleProduct(ProductBase):
    """A circle product with a given radius.

    Attributes:
        name: Product name, defaults to ``"Circle"``.
        radius: The radius of the circle; must be positive.

    Example:
        >>> c = CircleProduct(radius=1.0)
        >>> round(c.area(), 5)
        3.14159
    """

    name: str = "Circle"
    radius: float

    @field_validator("radius")
    @classmethod
    def radius_must_be_positive(cls, v: float) -> float:
        """Validate that radius is strictly positive.

        Args:
            v: The radius value to validate.

        Returns:
            The validated radius value.

        Raises:
            ValueError: If ``v`` is not greater than zero.
        """
        if v <= 0:
            raise ValueError("radius must be greater than 0")
        return v

    def area(self) -> float:
        """Return the area of the circle (π * r²).

        Returns:
            Area of the circle.
        """
        return math.pi * self.radius**2

    def perimeter(self) -> float:
        """Return the circumference of the circle (2 * π * r).

        Returns:
            Circumference of the circle.
        """
        return 2 * math.pi * self.radius


class RectangleProduct(ProductBase):
    """A rectangle product with given width and height.

    Attributes:
        name: Product name, defaults to ``"Rectangle"``.
        width: The width of the rectangle; must be positive.
        height: The height of the rectangle; must be positive.

    Example:
        >>> r = RectangleProduct(width=4.0, height=5.0)
        >>> r.area()
        20.0
    """

    name: str = "Rectangle"
    width: float
    height: float

    @field_validator("width", "height")
    @classmethod
    def dimensions_must_be_positive(cls, v: float) -> float:
        """Validate that width and height are strictly positive.

        Args:
            v: The dimension value to validate.

        Returns:
            The validated dimension value.

        Raises:
            ValueError: If ``v`` is not greater than zero.
        """
        if v <= 0:
            raise ValueError("width and height must be greater than 0")
        return v

    def area(self) -> float:
        """Return the area of the rectangle (width * height).

        Returns:
            Area of the rectangle.
        """
        return self.width * self.height

    def perimeter(self) -> float:
        """Return the perimeter of the rectangle (2 * (width + height)).

        Returns:
            Perimeter of the rectangle.
        """
        return 2 * (self.width + self.height)


class TriangleProduct(ProductBase):
    """A triangle product defined by base, height, and three sides.

    Attributes:
        name: Product name, defaults to ``"Triangle"``.
        base: The base length of the triangle; must be positive.
        height: The height of the triangle; must be positive.
        side_a: First side length; must be positive.
        side_b: Second side length; must be positive.
        side_c: Third side length; must be positive.

    Example:
        >>> t = TriangleProduct(base=6.0, height=4.0, side_a=5.0, side_b=5.0, side_c=6.0)
        >>> t.area()
        12.0
    """

    name: str = "Triangle"
    base: float
    height: float
    side_a: float
    side_b: float
    side_c: float

    @field_validator("base", "height", "side_a", "side_b", "side_c")
    @classmethod
    def values_must_be_positive(cls, v: float) -> float:
        """Validate that all triangle dimensions are strictly positive.

        Args:
            v: The dimension value to validate.

        Returns:
            The validated dimension value.

        Raises:
            ValueError: If ``v`` is not greater than zero.
        """
        if v <= 0:
            raise ValueError("all triangle dimensions must be greater than 0")
        return v

    def area(self) -> float:
        """Return the area of the triangle (0.5 * base * height).

        Returns:
            Area of the triangle.
        """
        return 0.5 * self.base * self.height

    def perimeter(self) -> float:
        """Return the perimeter of the triangle (side_a + side_b + side_c).

        Returns:
            Perimeter of the triangle.
        """
        return self.side_a + self.side_b + self.side_c


class ProductFactory:
    """Factory class for creating :class:`ProductBase` instances.

    Products are resolved from a class-level registry that maps
    :class:`ProductType` values to their corresponding model classes.
    New product types can be registered at runtime via :meth:`register`.

    Example:
        >>> factory = ProductFactory()
        >>> circle = ProductFactory.create(ProductType.CIRCLE, radius=2.0)
        >>> circle.name
        'Circle'
    """

    _registry: dict[ProductType, type[ProductBase]] = {
        ProductType.CIRCLE: CircleProduct,
        ProductType.RECTANGLE: RectangleProduct,
        ProductType.TRIANGLE: TriangleProduct,
    }

    @classmethod
    def create(cls, product_type: ProductType, **kwargs: Any) -> ProductBase:
        """Instantiate and return a product of the requested type.

        Args:
            product_type: The :class:`ProductType` enum value identifying the
                product to create.
            **kwargs: Keyword arguments forwarded to the product model constructor.

        Returns:
            A concrete :class:`ProductBase` instance.

        Raises:
            ValueError: If ``product_type`` is not registered in the factory.
        """
        product_class = cls._registry.get(product_type)
        if product_class is None:
            raise ValueError(
                f"Unknown product type: {product_type!r}. "
                f"Available types: {list(cls._registry.keys())}"
            )
        return product_class(**kwargs)

    @classmethod
    def register(cls, product_type: ProductType, product_class: type[ProductBase]) -> None:
        """Register a new product class for a given product type.

        Args:
            product_type: The :class:`ProductType` enum value to associate with
                the new class.
            product_class: The class to instantiate when ``product_type`` is
                requested.
        """
        cls._registry[product_type] = product_class

    @classmethod
    def available_products(cls) -> list[ProductType]:
        """Return a list of all currently registered product types.

        Returns:
            A list of :class:`ProductType` values that have been registered.
        """
        return list(cls._registry.keys())
