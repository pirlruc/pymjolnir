"""Singleton design pattern implementation.

This module provides a thread-safe Singleton metaclass and an example
``ApplicationConfig`` class that leverages it. Only one instance of any
class using :class:`SingletonMeta` as its metaclass will ever be created
per Python process; subsequent instantiation attempts return the existing
instance.

Example:
    >>> from pymjolnir.singleton import ApplicationConfig
    >>> cfg1 = ApplicationConfig()
    >>> cfg2 = ApplicationConfig()
    >>> assert cfg1 is cfg2
    >>> cfg1.set("debug", True)
    >>> cfg2.get("debug")
    True
"""

from __future__ import annotations

import threading
from typing import Any


class SingletonMeta(type):
    """Thread-safe metaclass implementing the Singleton pattern.

    Classes that specify ``metaclass=SingletonMeta`` will only ever have
    one instance created. Each class gets its own dedicated lock to avoid
    unnecessary contention between unrelated singletons under concurrent
    access. A lightweight meta-lock guards the one-time creation of each
    per-class lock.

    Attributes:
        _instances: Mapping from class to its single instance.
        _locks: Per-class locks used during instance creation.
        _meta_lock: Guards creation of entries in ``_locks``.

    Example:
        >>> class MyService(metaclass=SingletonMeta):
        ...     pass
        >>> a = MyService()
        >>> b = MyService()
        >>> assert a is b
    """

    _instances: dict[type, Any] = {}
    _locks: dict[type, threading.Lock] = {}
    _meta_lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Return the singleton instance, creating it on first call.

        Each class using this metaclass gets its own dedicated lock, avoiding
        contention between unrelated singletons during concurrent instantiation.

        Args:
            *args: Positional arguments forwarded to ``__init__`` on first
                creation.
            **kwargs: Keyword arguments forwarded to ``__init__`` on first
                creation.

        Returns:
            The single instance of ``cls``.
        """
        if cls not in cls._instances:
            with cls._meta_lock:
                if cls not in cls._locks:
                    cls._locks[cls] = threading.Lock()
            with cls._locks[cls]:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class ApplicationConfig(metaclass=SingletonMeta):
    """Singleton application configuration store.

    Provides a simple key/value store accessible from anywhere in the
    application. Because :class:`SingletonMeta` is used as the metaclass,
    only a single :class:`ApplicationConfig` instance exists per process.

    Attributes:
        settings: Internal dictionary holding all configuration entries.

    Example:
        >>> config = ApplicationConfig()
        >>> config.set("log_level", "INFO")
        >>> config.get("log_level")
        'INFO'
    """

    def __init__(self) -> None:
        """Initialise the configuration store with an empty settings dict."""
        self.settings: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value by key.

        Args:
            key: The configuration key to look up.
            default: Value returned when ``key`` is not present. Defaults to
                ``None``.

        Returns:
            The stored value for ``key``, or ``default`` if not found.
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Store a configuration value.

        Args:
            key: The configuration key to set.
            value: The value to associate with ``key``.
        """
        self.settings[key] = value

    def clear(self) -> None:
        """Clear all stored configuration settings.

        This method empties the settings dictionary. It also removes the
        singleton instance from :attr:`SingletonMeta._instances` so that a
        fresh :class:`ApplicationConfig` can be created (useful in tests).
        """
        self.settings.clear()
        SingletonMeta._instances.pop(ApplicationConfig, None)
