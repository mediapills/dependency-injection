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
import types
import typing as t
from functools import update_wrapper
from functools import wraps

from mediapills.dependency_injection.exceptions import ExpectedCallableException
from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import RecursionInfiniteLoopError
from mediapills.dependency_injection.exceptions import UnknownIdentifierException

__all__ = ["Container"]

Callable = t.Callable[..., t.Any]
Dict = t.Dict[t.Any, t.Any]

"""Callable value with lazy load implementation."""
SERVICE_MODE_COMMON = 2 ** 0

"""Callable value without lazy load implementation."""
SERVICE_MODE_FACTORY = 2 ** 1

"""Extended callable value."""
SERVICE_MODE_EXTENDED = 2 ** 2

"""Prevent callable from being modified."""
SERVICE_MODE_FINAL = 2 ** 3

"""Callable value with enabled autowiring."""
SERVICE_MODE_KEYWORDED = 2 ** 4

"""Available service types"""
SERVICE_MODES = frozenset(
    [
        SERVICE_MODE_COMMON,
        SERVICE_MODE_FACTORY,
        SERVICE_MODE_EXTENDED,
        SERVICE_MODE_FINAL,
        SERVICE_MODE_KEYWORDED,
    ]
)


# class ServiceMode(Enum):
#     COMMON = SERVICE_MODE_COMMON
#     FACTORY = SERVICE_MODE_FACTORY
#     EXTENDED = SERVICE_MODE_EXTENDED
#     FINAL = SERVICE_MODE_FINAL
#     KEYWORDED = SERVICE_MODE_KEYWORDED


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
        self._templates: t.Set[t.Any] = set()

    def _freeze(self) -> None:
        """Warm up all offsets."""
        for k in self:
            if k not in self._frozen:
                self.__getitem__(k)

    @handle_unknown_identifier
    def __getitem__(self, key: t.Any) -> t.Any:
        """Return the value at specified offset."""
        # TODO: add __dependency_injection_result__ attr
        if key in self._protected:
            return dict.__getitem__(self, key)(self)

        raw = dict.__getitem__(self, key)

        if key in self._raw or not hasattr(raw, "__call__") or inspect.isclass(raw):
            return raw

        dict.__setitem__(
            self,
            key,
            lambda di, k=key: (_ for _ in ()).throw(RecursionInfiniteLoopError(k)),
        )

        result = raw(self)
        dict.__setitem__(self, key, result)
        self._raw[key] = raw

        self._frozen.add(key)

        return result

    def __setitem__(self, key: t.Any, val: t.Any) -> None:
        """Assign a value to the specified offset."""
        if key in self._frozen:
            raise FrozenServiceException(key)

        if callable(val) and not hasattr(val, "__dependency_injection_mode__"):
            val.__dependency_injection_mode__ = SERVICE_MODE_COMMON

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

    def template(self, key: str, template: str) -> None:
        """Format the specified value(s) and insert them inside the string's
        placeholder.
        """
        self.__setitem__(key, template)

        self._templates.add(key)

    @staticmethod
    def _cp_func(func: t.Any) -> t.Any:
        """Make deepcopy of a function.
        Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)
        """
        copy = types.FunctionType(
            func.__code__,
            func.__globals__,
            name=func.__name__,
            argdefs=func.__defaults__,
            closure=func.__closure__,
        )

        copy.__kwdefaults__ = func.__kwdefaults__

        return update_wrapper(copy, func)

    def service(  # dead: disable
        self, key: str, mode: int = SERVICE_MODE_COMMON
    ) -> Callable:
        """Assign a callable value to the specified offset."""

        def decorator(func: Callable) -> t.Any:
            if not callable(func):
                raise ExpectedCallableException()

            if mode > sum(SERVICE_MODES):
                raise ValueError(mode)

            if mode & SERVICE_MODE_EXTENDED and key not in self:
                raise UnknownIdentifierException(key)

            val = self._cp_func(func=func)
            val.__dependency_injection_mode__ = mode
            if mode & SERVICE_MODE_EXTENDED:
                val.__dependency_injection_callable_base__ = self.get(key, None)
            if mode & SERVICE_MODE_KEYWORDED:
                val.__dependency_injection_callable_args__ = val.__code__.co_varnames

            self.__setitem__(key=key, val=val)  # type: ignore

            return func

        return decorator

    # def factory(self, key: str) -> Callable:e
    #     """Mark a callable as being a factory service."""
    #
    #     def decorator(func: Callable) -> t.Any:
    #         func = self._wraps(key=key, func=func, mode=ServiceMode.FACTORY)
    #
    #         raise NotImplementedError()
    #
    #     return decorator
    #
    # def extend(self, key: str) -> Callable:
    #     """Extend an object definition."""
    #
    #     def decorator(func: Callable) -> t.Any:
    #         func = self._wraps(key=key, func=func, mode=ServiceMode.EXTENDED)
    #
    #         # TODO: save extension chain
    #         raise NotImplementedError()
    #
    #     return decorator
    #
    # def keyworded(self, key: str) -> Callable:
    #     """Mark a callable arguments as named auto full filled."""
    #
    #     def decorator(func: Callable) -> t.Any:
    #         func = self._wraps(key=key, func=func, mode=ServiceMode.KEYWORDED)
    #
    #         raise NotImplementedError()
    #
    #     return decorator

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
