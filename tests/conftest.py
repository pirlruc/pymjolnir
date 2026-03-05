"""Pytest configuration and shared fixtures for pymjolnir tests."""

from __future__ import annotations

import pytest

from pymjolnir.singleton import SingletonMeta


@pytest.fixture()
def reset_singletons() -> None:
    """Reset all SingletonMeta instances between tests.

    Yields:
        None — clears the singleton registry before and after each test
        that requests this fixture.
    """
    SingletonMeta._instances.clear()
    yield
    SingletonMeta._instances.clear()
