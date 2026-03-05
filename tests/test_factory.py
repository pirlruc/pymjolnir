"""Tests for pymjolnir.factory module."""

from __future__ import annotations

import math

import pytest
from pydantic import ValidationError

from pymjolnir.factory import (
    CircleProduct,
    ProductBase,
    ProductFactory,
    ProductType,
    RectangleProduct,
    TriangleProduct,
)

# ---------------------------------------------------------------------------
# ProductBase
# ---------------------------------------------------------------------------


class TestProductBase:
    """Tests for the abstract-like ProductBase model."""

    def test_describe_returns_name(self) -> None:
        """describe() should return 'I am a <name>'."""

        class ConcreteProduct(ProductBase):
            name: str = "Widget"

        product = ConcreteProduct()
        assert product.describe() == "I am a Widget"

    def test_area_raises_not_implemented(self) -> None:
        """area() should raise NotImplementedError on base class."""

        class ConcreteProduct(ProductBase):
            name: str = "Widget"

        product = ConcreteProduct()
        with pytest.raises(NotImplementedError):
            product.area()

    def test_perimeter_raises_not_implemented(self) -> None:
        """perimeter() should raise NotImplementedError on base class."""

        class ConcreteProduct(ProductBase):
            name: str = "Widget"

        product = ConcreteProduct()
        with pytest.raises(NotImplementedError):
            product.perimeter()


# ---------------------------------------------------------------------------
# CircleProduct
# ---------------------------------------------------------------------------


class TestCircleProduct:
    """Tests for CircleProduct."""

    def test_default_name(self) -> None:
        """Default name should be 'Circle'."""
        c = CircleProduct(radius=1.0)
        assert c.name == "Circle"

    def test_area(self) -> None:
        """area() should return pi * r^2."""
        c = CircleProduct(radius=3.0)
        assert math.isclose(c.area(), math.pi * 9, rel_tol=1e-9)

    def test_perimeter(self) -> None:
        """perimeter() should return 2 * pi * r."""
        c = CircleProduct(radius=3.0)
        assert math.isclose(c.perimeter(), 2 * math.pi * 3, rel_tol=1e-9)

    def test_describe(self) -> None:
        """describe() should return 'I am a Circle'."""
        c = CircleProduct(radius=1.0)
        assert c.describe() == "I am a Circle"

    @pytest.mark.parametrize("bad_radius", [0.0, -1.0, -100.0])
    def test_invalid_radius(self, bad_radius: float) -> None:
        """Radius ≤ 0 should raise ValidationError."""
        with pytest.raises(ValidationError):
            CircleProduct(radius=bad_radius)

    def test_custom_name(self) -> None:
        """name field can be overridden."""
        c = CircleProduct(name="SmallCircle", radius=1.0)
        assert c.name == "SmallCircle"


# ---------------------------------------------------------------------------
# RectangleProduct
# ---------------------------------------------------------------------------


class TestRectangleProduct:
    """Tests for RectangleProduct."""

    def test_default_name(self) -> None:
        """Default name should be 'Rectangle'."""
        r = RectangleProduct(width=2.0, height=3.0)
        assert r.name == "Rectangle"

    def test_area(self) -> None:
        """area() should return width * height."""
        r = RectangleProduct(width=4.0, height=5.0)
        assert r.area() == 20.0

    def test_perimeter(self) -> None:
        """perimeter() should return 2 * (width + height)."""
        r = RectangleProduct(width=4.0, height=5.0)
        assert r.perimeter() == 18.0

    def test_describe(self) -> None:
        """describe() should return 'I am a Rectangle'."""
        r = RectangleProduct(width=1.0, height=1.0)
        assert r.describe() == "I am a Rectangle"

    @pytest.mark.parametrize("bad_val", [0.0, -1.0])
    def test_invalid_width(self, bad_val: float) -> None:
        """Width ≤ 0 should raise ValidationError."""
        with pytest.raises(ValidationError):
            RectangleProduct(width=bad_val, height=1.0)

    @pytest.mark.parametrize("bad_val", [0.0, -1.0])
    def test_invalid_height(self, bad_val: float) -> None:
        """Height ≤ 0 should raise ValidationError."""
        with pytest.raises(ValidationError):
            RectangleProduct(width=1.0, height=bad_val)

    def test_square_is_rectangle(self) -> None:
        """A rectangle with equal sides is a valid square."""
        r = RectangleProduct(width=5.0, height=5.0)
        assert r.area() == 25.0
        assert r.perimeter() == 20.0


# ---------------------------------------------------------------------------
# TriangleProduct
# ---------------------------------------------------------------------------


class TestTriangleProduct:
    """Tests for TriangleProduct."""

    _valid_kwargs = {
        "base": 6.0,
        "height": 4.0,
        "side_a": 5.0,
        "side_b": 5.0,
        "side_c": 6.0,
    }

    def test_default_name(self) -> None:
        """Default name should be 'Triangle'."""
        t = TriangleProduct(**self._valid_kwargs)
        assert t.name == "Triangle"

    def test_area(self) -> None:
        """area() should return 0.5 * base * height."""
        t = TriangleProduct(**self._valid_kwargs)
        assert t.area() == 12.0

    def test_perimeter(self) -> None:
        """perimeter() should return side_a + side_b + side_c."""
        t = TriangleProduct(**self._valid_kwargs)
        assert t.perimeter() == 16.0

    def test_describe(self) -> None:
        """describe() should return 'I am a Triangle'."""
        t = TriangleProduct(**self._valid_kwargs)
        assert t.describe() == "I am a Triangle"

    @pytest.mark.parametrize(
        "field",
        ["base", "height", "side_a", "side_b", "side_c"],
    )
    def test_invalid_zero_field(self, field: str) -> None:
        """Any dimension ≤ 0 should raise ValidationError."""
        kwargs = dict(self._valid_kwargs)
        kwargs[field] = 0.0
        with pytest.raises(ValidationError):
            TriangleProduct(**kwargs)

    @pytest.mark.parametrize(
        "field",
        ["base", "height", "side_a", "side_b", "side_c"],
    )
    def test_invalid_negative_field(self, field: str) -> None:
        """Any negative dimension should raise ValidationError."""
        kwargs = dict(self._valid_kwargs)
        kwargs[field] = -1.0
        with pytest.raises(ValidationError):
            TriangleProduct(**kwargs)


# ---------------------------------------------------------------------------
# ProductFactory
# ---------------------------------------------------------------------------


class TestProductFactory:
    """Tests for ProductFactory."""

    def test_create_circle(self) -> None:
        """Factory should create a CircleProduct."""
        product = ProductFactory.create(ProductType.CIRCLE, radius=2.0)
        assert isinstance(product, CircleProduct)
        assert product.radius == 2.0

    def test_create_rectangle(self) -> None:
        """Factory should create a RectangleProduct."""
        product = ProductFactory.create(ProductType.RECTANGLE, width=3.0, height=4.0)
        assert isinstance(product, RectangleProduct)
        assert product.width == 3.0
        assert product.height == 4.0

    def test_create_triangle(self) -> None:
        """Factory should create a TriangleProduct."""
        product = ProductFactory.create(
            ProductType.TRIANGLE,
            base=6.0,
            height=4.0,
            side_a=5.0,
            side_b=5.0,
            side_c=6.0,
        )
        assert isinstance(product, TriangleProduct)

    def test_create_unknown_type_raises(self) -> None:
        """Creating an unregistered type should raise ValueError."""
        # Use a sentinel value not in the enum to simulate unregistered type
        # by temporarily removing a key from the registry.
        original = ProductFactory._registry.pop(ProductType.CIRCLE)
        try:
            with pytest.raises(ValueError, match="Unknown product type"):
                ProductFactory.create(ProductType.CIRCLE, radius=1.0)
        finally:
            ProductFactory._registry[ProductType.CIRCLE] = original

    def test_available_products_contains_all_types(self) -> None:
        """available_products() should contain all three default types."""
        available = ProductFactory.available_products()
        assert ProductType.CIRCLE in available
        assert ProductType.RECTANGLE in available
        assert ProductType.TRIANGLE in available

    def test_register_custom_product(self) -> None:
        """register() should add a new product type to the factory."""

        class HexagonProduct(ProductBase):
            name: str = "Hexagon"
            side: float

            def area(self) -> float:
                return (3 * math.sqrt(3) / 2) * self.side**2

            def perimeter(self) -> float:
                return 6 * self.side

        # Re-use TRIANGLE slot with a custom class temporarily
        original = ProductFactory._registry[ProductType.TRIANGLE]
        ProductFactory.register(ProductType.TRIANGLE, HexagonProduct)
        try:
            product = ProductFactory.create(ProductType.TRIANGLE, side=2.0)
            assert isinstance(product, HexagonProduct)
            assert product.name == "Hexagon"
        finally:
            ProductFactory.register(ProductType.TRIANGLE, original)

    def test_factory_create_validates_fields(self) -> None:
        """Factory.create() should propagate Pydantic ValidationError."""
        with pytest.raises(ValidationError):
            ProductFactory.create(ProductType.CIRCLE, radius=-5.0)

    def test_circle_area_via_factory(self) -> None:
        """End-to-end: circle area computed via factory."""
        product = ProductFactory.create(ProductType.CIRCLE, radius=1.0)
        assert math.isclose(product.area(), math.pi, rel_tol=1e-9)

    def test_rectangle_perimeter_via_factory(self) -> None:
        """End-to-end: rectangle perimeter computed via factory."""
        product = ProductFactory.create(ProductType.RECTANGLE, width=2.0, height=3.0)
        assert product.perimeter() == 10.0

    def test_triangle_area_via_factory(self) -> None:
        """End-to-end: triangle area computed via factory."""
        product = ProductFactory.create(
            ProductType.TRIANGLE,
            base=4.0,
            height=3.0,
            side_a=3.0,
            side_b=4.0,
            side_c=5.0,
        )
        assert product.area() == 6.0
