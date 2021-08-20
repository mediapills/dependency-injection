from typing import Any
from typing import Callable
from typing import Dict
from typing import Set

from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import UnknownIdentifierException


__all__ = ["Container"]


# TODO make `dir(dict)` for more info
class Container(dict):  # type: ignore
    def __init__(self, *args, **kw) -> None:  # type: ignore
        super().__init__(*args, **kw)
        # self._factories: Optional[Dict[Any, Any]] = None
        self._protected: Set[Any] = set()
        self._frozen: Set[Any] = set()
        self._raw: Dict[Any, Any] = dict()

    def __getitem__(self, key: Any) -> Any:
        """ x.__getitem__(y) <==> x[y] """

        if key not in self:
            raise UnknownIdentifierException(key)

        val = dict.__getitem__(self, key)

        if key in self._raw or key in self._protected or not hasattr(val, "__call__"):
            return dict.__getitem__(self, key)

        # TODO: add factories check

        raw = dict.__getitem__(self, key)
        result = raw(self)
        dict.__setitem__(self, key, result)
        self._raw[key] = raw

        self._frozen.add(key)

        return result

    def __setitem__(self, key: Any, val: Any) -> None:
        """ Set self[key] to value. """

        if key in self._frozen:
            raise FrozenServiceException(key)

        dict.__setitem__(self, key, val)

    def __delitem__(self, key: Any) -> None:
        """ Delete self[key]. """

        # TODO: implement for factories

        self._protected.discard(key)
        self._frozen.discard(key)
        self._raw.pop(key, None)

        dict.__delitem__(self, key)

    def clear(self) -> None:

        # TODO: implement for factories

        self._protected.clear()
        self._frozen.clear()
        self._raw.clear()

        dict.clear(self)

    def factory(self, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Marks a callable as being a factory service."""

        raise NotImplementedError

    def protect(self, key: Any) -> None:  # dead: disable
        """Protects a callable from being interpreted as a service."""

        if key not in self:
            raise UnknownIdentifierException(key)

        self._protected.add(key)

    def raw(self, key: Any) -> Any:
        """Gets a parameter or the closure defining an object."""

        if key not in self:
            raise UnknownIdentifierException(key)

        if key in self._raw:
            return self._raw[key]

        return dict.__getitem__(self, key)

    def extend(self, key: Any, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Extends an object definition."""

        #     if key not in self:
        #         raise UnknownIdentifierException(key)
        #
        #     if self._is_frozen(key=key):
        #         raise FrozenServiceException(key)
        #
        #     # TODO: implement this

        raise NotImplementedError
