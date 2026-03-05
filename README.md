# pymjolnir

[![PyPI version](https://img.shields.io/pypi/v/pymjolnir.svg)](https://pypi.org/project/pymjolnir/)
[![Python versions](https://img.shields.io/pypi/pyversions/pymjolnir.svg)](https://pypi.org/project/pymjolnir/)
[![License](https://img.shields.io/github/license/pymjolnir/pymjolnir.svg)](LICENSE)
[![CI](https://github.com/pymjolnir/pymjolnir/actions/workflows/ci.yml/badge.svg)](https://github.com/pymjolnir/pymjolnir/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/pymjolnir/pymjolnir)

A Python library implementing classic design patterns — **Factory** and **Singleton** — using
modern tooling such as [Pydantic](https://docs.pydantic.dev/) for data validation.

---

## Features

- **Factory Pattern** — create geometric shape objects via a central registry without coupling
  callers to concrete classes. Supports Circle, Rectangle, and Triangle out of the box, plus
  custom product types.
- **Singleton Pattern** — thread-safe metaclass ensuring one-instance-per-class semantics,
  with a ready-to-use `ApplicationConfig` example.
- Full type annotations and Google-style docstrings throughout.
- ≥ 95 % test coverage enforced by CI.

---

## Installation

```bash
pip install pymjolnir
```

Requires Python **3.11+**.

---

## Usage

### Factory Pattern

```python
from pymjolnir import ProductFactory, ProductType

# Create a circle with radius 5
circle = ProductFactory.create(ProductType.CIRCLE, radius=5.0)
print(circle.area())        # 78.53981633974483
print(circle.perimeter())   # 31.41592653589793
print(circle.describe())    # I am a Circle

# Create a rectangle
rect = ProductFactory.create(ProductType.RECTANGLE, width=4.0, height=6.0)
print(rect.area())          # 24.0

# Create a triangle
tri = ProductFactory.create(
    ProductType.TRIANGLE,
    base=6.0, height=4.0,
    side_a=5.0, side_b=5.0, side_c=6.0,
)
print(tri.perimeter())      # 16.0

# List available product types
print(ProductFactory.available_products())

# Register a custom product type
from pymjolnir.factory import ProductBase
import math

class HexagonProduct(ProductBase):
    name: str = "Hexagon"
    side: float

    def area(self) -> float:
        return (3 * math.sqrt(3) / 2) * self.side ** 2

    def perimeter(self) -> float:
        return 6 * self.side

ProductFactory.register(ProductType.TRIANGLE, HexagonProduct)  # reuse any key
```

### Singleton Pattern

```python
from pymjolnir import SingletonMeta

class AppConfig(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.settings: dict = {}

cfg1 = AppConfig()
cfg2 = AppConfig()
assert cfg1 is cfg2  # same instance

# Built-in ApplicationConfig
from pymjolnir.singleton import ApplicationConfig

config = ApplicationConfig()
config.set("debug", True)
config.set("log_level", "INFO")

print(config.get("debug"))          # True
print(config.get("missing", 42))    # 42  (default value)
config.clear()                      # reset settings
```

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/pymjolnir/pymjolnir.git
cd pymjolnir

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package with development extras
pip install -e ".[dev]"

# Run tests
pytest

# Run the linter
ruff check src/ tests/

# Type-check
mypy src/pymjolnir/
```

A [Dev Container](.devcontainer/devcontainer.json) configuration is included for VS Code /
GitHub Codespaces — open the repository and click **Reopen in Container**.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Ensure all tests pass (`pytest`) and coverage remains ≥ 95 %.
3. Run `ruff check` and `mypy` — fix any issues before opening a PR.
4. Open a pull request against `main`.

Please follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
conventions and add docstrings to every public symbol.

---

## License

Distributed under the terms of the [LICENSE](LICENSE) file in this repository.
