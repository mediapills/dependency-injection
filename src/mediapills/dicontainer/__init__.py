from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Set

from mediapills.dicontainer.exceptions import FrozenServiceException  # type: ignore
from mediapills.dicontainer.exceptions import UnknownIdentifierException  # type: ignore

__all__ = ["Container"]


# TODO make `dir(dict)` for more info
class Container(dict):  # type: ignore
    def __init__(self, *args, **kw) -> None:  # type: ignore
        super().__init__(*args, **kw)
        self._factories: Optional[Dict[Any, Any]] = None
        self._protected: Optional[Dict[Any, Any]] = None
        self._frozen: Optional[Set[Any]] = None
        self._raw: Optional[Dict[Any, Any]] = None

    def _is_frozen(self, key: Any) -> bool:
        return self._frozen is not None and key in self._frozen

    def __getitem__(self, key: Any) -> Any:
        """ x.__getitem__(y) <==> x[y] """

        if key not in self:
            raise UnknownIdentifierException(key)

        # if any(
        #         (self._raw is not None and key in self._raw),
        # ):
        #     return dict.__getitem__(self, key)

        # TODO: implement this

        # raw = dict.__getitem__(self, key)
        # val = raw(self)
        # dict.__setitem__(self, key, val)
        # self._raw[key] = raw
        # return val

        return dict.__getitem__(self, key)

    def __setitem__(self, key: Any, val: Any) -> None:
        """ Set self[key] to value. """

        if self._is_frozen(key=key):
            raise FrozenServiceException(key)

        dict.__setitem__(self, key, val)

    def __delitem__(self, key: Any) -> None:
        """ Delete self[key]. """

        # TODO: implement this

        dict.__delitem__(self, key)

    def clear(self) -> None:

        # TODO: implement this

        dict.clear(self)

    def factory(self, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Marks a callable as being a factory service."""

        raise NotImplementedError

    def protect(self, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Protects a callable from being interpreted as a service."""

        raise NotImplementedError

    def raw(self, key: Any) -> None:  # dead: disable
        """Gets a parameter or the closure defining an object."""

        if self._is_frozen(key=key):
            raise UnknownIdentifierException(key)

        if self._raw is not None and key in self._raw:
            return self._raw[key]

        return dict.__getitem__(self, key)

    def extend(self, key: Any, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Extends an object definition."""

        if key not in self:
            raise UnknownIdentifierException(key)

        if self._is_frozen(key=key):
            raise FrozenServiceException(key)

        # TODO: implement this

        raise NotImplementedError
