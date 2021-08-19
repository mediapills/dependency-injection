from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional


__all__ = ["Container"]


# TODO make `dir(dict)` for more info
class Container(dict):  # type: ignore
    def __init__(self, *args, **kw) -> None:  # type: ignore
        super().__init__(*args, **kw)
        self._factories: Optional[Dict[Any, Any]] = None
        self._protected: Optional[Dict[Any, Any]] = None
        self._frozen: Optional[Dict[Any, Any]] = None
        self._raw: Optional[Dict[Any, Any]] = None

    def __getitem__(self, key: Any) -> Any:
        return dict.__getitem__(self, key)

    def __setitem__(self, key: Any, val: Any) -> None:
        dict.__setitem__(self, key, val)

    def factory(self, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Marks a callable as being a factory service."""

        raise NotImplementedError

    def protect(self, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Protects a callable from being interpreted as a service."""

        raise NotImplementedError

    def raw(self, key: Any) -> None:  # dead: disable
        """Gets a parameter or the closure defining an object."""

        raise NotImplementedError

    def extend(self, key: Any, callable: Callable[[Any], Any]) -> None:  # dead: disable
        """Extends an object definition."""

        raise NotImplementedError
