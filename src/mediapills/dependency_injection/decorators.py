# Copyright The Mediapills Dependency Injection Authors.
# SPDX-License-Identifier: MIT
from abc import ABCMeta


class BaseDecorator(metaclass=ABCMeta):

    pass


class ProtectedDecorator(BaseDecorator):  # dead: disable
    """Protects a callable from being interpreted as a service helper."""

    pass


class FactoryDecorator(BaseDecorator):  # dead: disable
    """Protects a callable from being replaced as a result helper."""

    pass


class StringDecorator(BaseDecorator):  # dead: disable
    """Concatenate strings entries helper."""

    pass


class AutowiredDecorator(BaseDecorator):  # dead: disable
    """Help override what we need from the autowiring, instead of configuring
    from scratch how the object will be built."""

    pass
