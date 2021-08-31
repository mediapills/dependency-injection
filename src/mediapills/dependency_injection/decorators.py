# Copyright The Mediapills Dependency Injection Authors.
# SPDX-License-Identifier: MIT
from abc import ABCMeta
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from functools import update_wrapper


class BaseDecorator(metaclass=ABCMeta):
    def __init__(self, func: Callable[..., Any]):
        update_wrapper(self, func)

        self._func = func

    @property
    def raw(self):
        """Gets a parameter or the closure defining an object."""

        return self._func


class ProtectedDecorator(BaseDecorator):  # dead: disable
    """Protects a callable from being interpreted as a service helper."""

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:

        a = self._func

        return self._func(*args, **kwargs)


class FactoryDecorator(BaseDecorator):  # dead: disable
    """Protects a callable from being replaced as a result helper."""

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:

        return self._func(*args, **kwargs)


class StringDecorator(BaseDecorator):  # dead: disable
    """Concatenate strings entries helper."""

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:

        return self._func(*args, **kwargs)


class AutowiredDecorator(BaseDecorator):  # dead: disable
    """Help override what we need from the autowiring, instead of configuring
    from scratch how the object will be built."""

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:

        return self._func(*args, **kwargs)
