# Copyright (c) 2021-2021 Mediapills Dependency Injection Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import inspect
import typing as t
from functools import wraps

from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import RecursionInfiniteLoopError
from mediapills.dependency_injection.exceptions import UnknownIdentifierException

__all__ = ["Container"]

Callable = t.Callable[..., t.Any]


def handle_unknown_identifier(func: Callable) -> t.Any:
    @wraps(func)
    def wrapped(*args: t.List[t.Any], **kwargs: t.Dict[t.Any, t.Any]) -> t.Any:
        self, key = args

        if key not in self:
            raise UnknownIdentifierException(key)

        return func(*args, **kwargs)

    return wrapped


class Container(dict):  # type: ignore
    """Container DI implementation."""

    def __init__(self, *args, **kw) -> None:  # type: ignore
        """Create a new object."""
        super().__init__(*args, **kw)

        self._raw: t.Dict[str, t.Any] = dict()
        self._protected: t.Set[t.Any] = set()
        self._frozen: t.Set[t.Any] = set()
        # self._factories: t.Dict[str, t.Any] = dict()

    def _freeze(self) -> None:
        """Warm up all offsets."""
        for k in self:
            if k not in self._frozen:
                self.__getitem__(k)

    @handle_unknown_identifier
    def process(self, key: t.Any) -> None:
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
    def __getitem__(self, key: t.Any) -> t.Any:
        """Return the value at specified offset."""
        # TODO: add factories check
        # TODO: add __dependency_injection_result__ attr
        if key in self._protected:
            return dict.__getitem__(self, key)(self)

        self.process(key)

        return dict.__getitem__(self, key)

    def __setitem__(self, key: t.Any, val: t.Any) -> None:
        """Assign a value to the specified offset."""
        if key in self._frozen:
            raise FrozenServiceException(key)

        dict.__setitem__(self, key, val)

    def __delitem__(self, key: t.Any) -> None:
        """Unset an offset."""
        # TODO: implement for factories

        self._protected.discard(key)
        self._frozen.discard(key)
        self._raw.pop(key, None)

        dict.__delitem__(self, key)

    def clear(self) -> None:
        """Remove all offsets."""
        # TODO: implement for factories

        self._protected.clear()
        self._frozen.clear()
        self._raw.clear()

        dict.clear(self)

    def values(self) -> t.Any:
        """Return a new view of the dictionary’s values."""
        self._freeze()

        return dict.values(self)

    def items(self) -> t.Any:
        """Return a new view of the dictionary’s items."""
        self._freeze()

        return dict.items(self)

    def copy(self) -> t.Any:
        """Return a shallow copy of the dictionary."""
        self._freeze()

        return dict.copy(self)

    def update(self, others: t.Union[dict, t.MutableMapping]) -> None:  # type: ignore
        """Update the dictionary with the key/value pairs from other,
        overwriting existing keys.
        """
        for key, value in others.items():
            self.__setitem__(key, value)

        return dict.update(self)

    @handle_unknown_identifier
    def raw(self, key: t.Any) -> t.Any:
        """Get a parameter or the closure defining an object."""
        if key in self._raw:
            return self._raw[key]

        return dict.__getitem__(self, key)

    def template(self, key: str, template: str) -> None:  # dead: disable
        """Format the specified value(s) and insert them inside the string's
        placeholder.
        """
        # TODO: save str key in self._templates set
        raise NotImplementedError()

    def service(self, key: str) -> Callable:  # dead: disable
        """Assign a callable value to the specified offset."""

        def decorator(func: Callable) -> t.Any:
            # TODO: add __dependency_injection_service__ attr
            self.__setitem__(key, func)

            return func

        return decorator

    def factory(self, key: str) -> Callable:  # dead: disable
        """Mark a callable as being a factory service."""

        def decorator(func: Callable) -> t.Any:
            # TODO: add __dependency_injection_factory__ attr
            raise NotImplementedError()

        return decorator

    def extend(self, key: str) -> Callable:  # dead: disable
        """Extend an object definition."""

        def decorator(func: Callable) -> t.Any:
            # TODO: add __dependency_injection_extend__ attr
            # TODO: save extension chain
            raise NotImplementedError()

        return decorator

    def keyworded(self, key: str) -> Callable:  # dead: disable
        """Mark a callable arguments as named auto full filled."""

        def decorator(func: Callable) -> t.Any:
            # TODO: add __dependency_injection_keyworded__ attr
            raise NotImplementedError()

        return decorator

    # def protect(self, key: t.Any) -> None:
    #     """Protects a callable from being interpreted as a service."""
    #
    #     if key not in self:
    #         raise UnknownIdentifierException(key)
    #
    #     self._protected.add(key)
    #
    # def extend(self, key: t.Any, callable: Callable) -> None:
    #     """Extends an object definition."""
    #     if key not in self:
    #         raise UnknownIdentifierException(key)
    #
    #     if key in self._frozen:
    #         raise FrozenServiceException(key)
    #
    #     if key in self._protected:
    #         raise ProtectedServiceException(key)
    #
    #     raw = self.raw(key)
    #
    #     if not hasattr(raw, "__call__"):
    #         raise ExpectedInvokableException(key)
    #
    #     extended = lambda di, func=callable, base=raw: func(base(di), di)  # noqa: E731
    #
    #     self._factories[key] = extended
    #
    #     self.__setitem__(key, extended)
