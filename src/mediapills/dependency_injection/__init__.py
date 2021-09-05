# Copyright The Mediapills Dependency Injection Authors.
# SPDX-License-Identifier: MIT
import inspect
import warnings
from enum import Enum
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import MutableMapping
from typing import Set
from typing import Union

from mediapills.dependency_injection.exceptions import ExpectedInvokableException
from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import ProtectedServiceException
from mediapills.dependency_injection.exceptions import RecursionInfiniteLoopError
from mediapills.dependency_injection.exceptions import UnknownIdentifierException

__all__ = ["Container", "Injector"]

"""The stacklevel argument can be used by wrapper functions written in Python."""
ROUTINE_STACKLEVEL = 2

"""Base class for warnings about deprecated features."""
WARN_CATEGORY = DeprecationWarning

"""Protects a callable from being interpreted as a service helper."""
ITEM_DEFINITION_PROTECTED = "protected"

"""Marks a callable as being a factory service."""
ITEM_DEFINITION_FACTORY = "factory"

"""Concatenate strings entries helper."""
ITEM_DEFINITION_STRING = "string"

"""Help override what we need from the autowiring, instead of configuring from
scratch how the object will be built."""
ITEM_DEFINITION_AUTOWIRED = "autowired"


class ItemDefinition(Enum):
    PROTECTED = ITEM_DEFINITION_PROTECTED  # dead: disable
    FACTORY = ITEM_DEFINITION_FACTORY
    STRING = ITEM_DEFINITION_STRING
    AUTOWIRED = ITEM_DEFINITION_AUTOWIRED


def handle_unknown_identifier(func: Callable[[Any, str], Any]) -> Any:
    @wraps(func)
    def wrapped(*args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        self, key = args

        if key not in self:
            raise UnknownIdentifierException(key)

        return func(*args, **kwargs)  # type: ignore

    return wrapped


class Injector(dict):  # type: ignore
    """Container main class (deprecated)."""

    def deprecated(self, version: str, reason: str) -> None:
        """Issue a warning when the function is used."""

        fmt = (
            "The class '{name}' is deprecated."
            " ({reason})"
            " -- Deprecated since version {version}."
        )

        msg = fmt.format(name=self.__class__.__name__, reason=reason, version=version)

        warnings.warn(msg, category=WARN_CATEGORY, stacklevel=ROUTINE_STACKLEVEL)

    def __init__(self, *args, **kw) -> None:  # type: ignore
        self.deprecated(
            version="0.1.1",
            reason="This class is no longer available. Use {Container} instead.",
        )

        super().__init__(*args, **kw)

        self._warmed: bool = False
        self._raw: Dict[Any, Any] = dict()
        self._protected: Set[Any] = set()
        self._frozen: Set[Any] = set()
        self._factories: Dict[str, Any] = dict()

    def warm_up(self) -> None:
        """Process all offsets."""

        if not self._warmed:
            [self.__getitem__(k) for k in self]

    @handle_unknown_identifier
    def process(self, key: Any) -> None:
        """Execute function or object as a function."""

        raw = dict.__getitem__(self, key)

        if key in self._raw or not hasattr(raw, "__call__") or inspect.isclass(raw):
            return

        dict.__setitem__(
            self,
            key,
            lambda di, k=key: (_ for _ in ()).throw(RecursionInfiniteLoopError(k)),
        )
        result = raw(self)
        dict.__setitem__(self, key, result)
        self._raw[key] = raw

        self._frozen.add(key)

    @handle_unknown_identifier
    def __getitem__(self, key: Any) -> Any:
        """Returns the value at specified offset."""

        # TODO: add factories check

        if key in self._protected:
            return dict.__getitem__(self, key)(self)

        self.process(key)

        return dict.__getitem__(self, key)

    def __setitem__(self, key: Any, val: Any) -> None:
        """Assigns a value to the specified offset."""

        if key in self._frozen:
            raise FrozenServiceException(key)

        dict.__setitem__(self, key, val)

    def __delitem__(self, key: Any) -> None:
        """Unsets an offset."""

        # TODO: implement for factories

        self._protected.discard(key)
        self._frozen.discard(key)
        self._raw.pop(key, None)
        self._factories.pop(key, None)

        dict.__delitem__(self, key)

    def clear(self) -> None:
        """Remove all offsets."""

        # TODO: implement for factories

        self._protected.clear()
        self._frozen.clear()
        self._raw.clear()
        self._factories.clear()

        dict.clear(self)

    def values(self) -> Any:
        """Return a new view of the dictionary’s values."""

        self.warm_up()

        return dict.values(self)

    def items(self) -> Any:
        """Return a new view of the dictionary’s items ((key, value) pairs)."""

        self.warm_up()

        return dict.items(self)

    def copy(self) -> Any:
        """Return a shallow copy of the dictionary."""

        self.warm_up()

        return dict.copy(self)

    def update(self, others: Union[dict, MutableMapping]) -> None:  # type: ignore
        """Update the dictionary with the key/value pairs from other, overwriting
        existing keys."""

        for key, value in others.items():
            self.__setitem__(key, value)

        return dict.update(self)

    @handle_unknown_identifier
    def raw(self, key: Any) -> Any:
        """Gets a parameter or the closure defining an object."""

        if key in self._raw:
            return self._raw[key]

        return dict.__getitem__(self, key)

    def protect(self, key: Any) -> None:  # dead: disable
        """Protects a callable from being interpreted as a service."""

        if key not in self:
            raise UnknownIdentifierException(key)

        self._protected.add(key)

    def extend(self, key: Any, func: Callable[[Any], Any]) -> None:  # dead: disable
        """Extends an object definition."""
        if key not in self:
            raise UnknownIdentifierException(key)

        if key in self._frozen:
            raise FrozenServiceException(key)

        if key in self._protected:
            raise ProtectedServiceException(key)

        raw = self.raw(key)

        if not hasattr(raw, "__call__"):
            raise ExpectedInvokableException(key)

        extended = lambda di, f=func, r=raw: f(r(di), di)  # noqa: E731

        self._factories[key] = extended

        self.__setitem__(key, extended)

    def set_custom(
        self,
        definition: ItemDefinition,
        key: str,  # dead: disable
        func: Callable[..., Any],  # dead: disable
    ) -> None:

        if definition.value == ITEM_DEFINITION_PROTECTED:
            pass

        elif definition.value == ITEM_DEFINITION_FACTORY:
            pass

        elif definition.value == ITEM_DEFINITION_STRING:
            pass

        elif definition.value == ITEM_DEFINITION_AUTOWIRED:
            pass

    def factory(self, key: Any) -> Callable[..., Any]:  # dead: disable
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.set_custom(ItemDefinition.FACTORY, key=key, func=func)
            return func

        return decorator

    def string(self, key: Any) -> Callable[..., Any]:  # dead: disable
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.set_custom(ItemDefinition.STRING, key=key, func=func)
            return func

        return decorator

    def autowired(self, key: Any) -> Callable[..., Any]:  # dead: disable
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.set_custom(ItemDefinition.AUTOWIRED, key=key, func=func)
            return func

        return decorator


class Container(Injector):
    """Container main class."""

    def deprecated(self, version: str, reason: str) -> None:
        """Issue a warning when the function is used (disabled)."""

        pass
