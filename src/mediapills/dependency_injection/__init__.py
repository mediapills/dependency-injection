import inspect
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import MutableMapping
from typing import Set
from typing import Union

from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import InvalidServiceIdentifierException
from mediapills.dependency_injection.exceptions import ProtectedServiceException
from mediapills.dependency_injection.exceptions import UnknownIdentifierException

__all__ = ["Injector"]


def handle_unknown_identifier(func: Callable[[Any, str], Any]) -> Any:
    @wraps(func)
    def wrapped(*args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        self, key = args

        if key not in self:
            raise UnknownIdentifierException(key)

        return func(*args, **kwargs)  # type: ignore

    return wrapped


# TODO make `dir(dict)` for more info
class Injector(dict):  # type: ignore
    def __init__(self, *args, **kw) -> None:  # type: ignore
        super().__init__(*args, **kw)

        self._warmed: bool = False
        self._raw: Dict[Any, Any] = dict()
        self._protected: Set[Any] = set()
        self._frozen: Set[Any] = set()
        self._factories: Dict[str, Any] = dict()

    def warm_up(self) -> None:
        """process all offsets."""

        if not self._warmed:
            [self.__getitem__(k) for k in self]

    @handle_unknown_identifier
    def process(self, key: Any) -> None:
        """Execute function or object as a function."""
        raw = dict.__getitem__(self, key)

        if key in self._raw or not hasattr(raw, "__call__") or inspect.isclass(raw):
            return

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

    @handle_unknown_identifier  # dead: disable
    def protect(self, key: Any) -> None:
        """Protects a callable from being interpreted as a service."""

        self._protected.add(key)

    def extend(self, key: Any, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Extends an object definition."""
        if key not in self:
            raise UnknownIdentifierException(key)

        if key in self._frozen:
            raise FrozenServiceException(key)

        if key in self._protected:
            raise ProtectedServiceException(key)

        raw = self.raw(key)

        if not hasattr(raw, "__call__"):
            raise InvalidServiceIdentifierException(key)

        extended = lambda di, func=callable, base=raw: func(base(di), di)  # noqa: E731

        self._factories[key] = extended

        self.__setitem__(key, extended)
