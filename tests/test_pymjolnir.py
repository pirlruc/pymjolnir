"""Smoke tests until the public API grows."""

import pymjolnir


def test_package_importable() -> None:
    """Import package; module docstring should be present."""
    assert pymjolnir.__doc__
