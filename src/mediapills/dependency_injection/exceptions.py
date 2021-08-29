# Copyright The Mediapills Dependency Injection Authors.
# SPDX-License-Identifier: MIT


class BaseInjectorException(Exception):
    """Base Dependency Injection Container Exception."""

    pass


class ExpectedInvokableException(BaseInjectorException):
    """A closure or invokable object was expected."""

    pass


class FrozenServiceException(BaseInjectorException):
    """An attempt to modify a frozen service was made."""

    pass


class ProtectedServiceException(BaseInjectorException):
    """An attempt to extend a protected service was made."""

    pass


class UnknownIdentifierException(BaseInjectorException, KeyError):
    """The identifier of a valid service or parameter was expected."""

    pass


class RecursionInfiniteLoopError(BaseInjectorException, RecursionError):
    """The interpreter detect infinite services dependency depth."""

    pass
