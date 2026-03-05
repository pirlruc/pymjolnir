"""Tests for pymjolnir.singleton module."""

from __future__ import annotations

import threading
from typing import Any

from pymjolnir.singleton import ApplicationConfig, SingletonMeta

# ---------------------------------------------------------------------------
# SingletonMeta
# ---------------------------------------------------------------------------


class TestSingletonMeta:
    """Tests for SingletonMeta metaclass."""

    def test_same_instance_returned(self, reset_singletons: Any) -> None:
        """Two instantiations should return the exact same object."""

        class MyService(metaclass=SingletonMeta):
            pass

        a = MyService()
        b = MyService()
        assert a is b

    def test_different_classes_different_instances(self, reset_singletons: Any) -> None:
        """Different classes should each have their own singleton."""

        class ServiceA(metaclass=SingletonMeta):
            pass

        class ServiceB(metaclass=SingletonMeta):
            pass

        a = ServiceA()
        b = ServiceB()
        assert a is not b

    def test_thread_safety(self, reset_singletons: Any) -> None:
        """Concurrent threads should all receive the same instance."""

        class SharedService(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 0

        instances: list[SharedService] = []
        lock = threading.Lock()

        def create_instance() -> None:
            instance = SharedService()
            with lock:
                instances.append(instance)

        threads = [threading.Thread(target=create_instance) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        first = instances[0]
        assert all(inst is first for inst in instances)

    def test_reset_via_fixture(self, reset_singletons: Any) -> None:
        """After reset_singletons, a new instance should be created."""

        class ResetService(metaclass=SingletonMeta):
            pass

        a = ResetService()
        SingletonMeta._instances.clear()
        b = ResetService()
        # b is a fresh instance; a and b are not the same object
        assert a is not b

    def test_instances_dict_is_populated(self, reset_singletons: Any) -> None:
        """_instances should contain the class key after first instantiation."""

        class TrackedService(metaclass=SingletonMeta):
            pass

        TrackedService()
        assert TrackedService in SingletonMeta._instances


# ---------------------------------------------------------------------------
# ApplicationConfig
# ---------------------------------------------------------------------------


class TestApplicationConfig:
    """Tests for ApplicationConfig singleton."""

    def test_singleton_behaviour(self, reset_singletons: Any) -> None:
        """Two ApplicationConfig() calls should return the same object."""
        cfg1 = ApplicationConfig()
        cfg2 = ApplicationConfig()
        assert cfg1 is cfg2

    def test_set_and_get(self, reset_singletons: Any) -> None:
        """set() stores a value that get() retrieves."""
        cfg = ApplicationConfig()
        cfg.set("key", "value")
        assert cfg.get("key") == "value"

    def test_get_default(self, reset_singletons: Any) -> None:
        """get() returns the default when the key does not exist."""
        cfg = ApplicationConfig()
        assert cfg.get("missing") is None
        assert cfg.get("missing", "fallback") == "fallback"

    def test_set_overwrites_value(self, reset_singletons: Any) -> None:
        """set() should overwrite an existing key."""
        cfg = ApplicationConfig()
        cfg.set("x", 1)
        cfg.set("x", 2)
        assert cfg.get("x") == 2

    def test_clear_removes_settings(self, reset_singletons: Any) -> None:
        """clear() should empty the settings dict."""
        cfg = ApplicationConfig()
        cfg.set("a", 1)
        cfg.set("b", 2)
        cfg.clear()
        assert cfg.get("a") is None
        assert cfg.get("b") is None
        assert cfg.settings == {}

    def test_clear_resets_singleton(self, reset_singletons: Any) -> None:
        """clear() should remove the singleton so a fresh one can be created."""
        cfg1 = ApplicationConfig()
        cfg1.set("debug", True)
        cfg1.clear()
        cfg2 = ApplicationConfig()
        # A fresh instance is created; settings should be empty
        assert cfg2.get("debug") is None

    def test_settings_shared_across_references(self, reset_singletons: Any) -> None:
        """Changes via one reference should be visible through another."""
        cfg1 = ApplicationConfig()
        cfg2 = ApplicationConfig()
        cfg1.set("shared", 42)
        assert cfg2.get("shared") == 42

    def test_multiple_keys(self, reset_singletons: Any) -> None:
        """Multiple keys can coexist in settings."""
        cfg = ApplicationConfig()
        cfg.set("host", "localhost")
        cfg.set("port", 8080)
        cfg.set("debug", False)
        assert cfg.get("host") == "localhost"
        assert cfg.get("port") == 8080
        assert cfg.get("debug") is False

    def test_value_types(self, reset_singletons: Any) -> None:
        """Settings can store various Python types."""
        cfg = ApplicationConfig()
        cfg.set("list_val", [1, 2, 3])
        cfg.set("dict_val", {"a": 1})
        cfg.set("none_val", None)
        assert cfg.get("list_val") == [1, 2, 3]
        assert cfg.get("dict_val") == {"a": 1}
        assert cfg.get("none_val") is None
