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


class BaseInjectorException(Exception):
    """Base Dependency Injection Container Exception."""

    pass


class ExpectedCallableException(BaseInjectorException):
    """A closure or invokable object was expected."""

    pass


class FrozenServiceException(BaseInjectorException):
    """An attempt to modify a frozen service was made."""

    pass


class ProtectedServiceException(BaseInjectorException):  # dead: disable
    """An attempt to extend a protected service was made."""

    pass


class UnknownIdentifierException(BaseInjectorException, KeyError):
    """The identifier of a valid service or parameter was expected."""

    pass


class RecursionInfiniteLoopError(BaseInjectorException, RecursionError):
    """The interpreter detect infinite services dependency depth."""

    pass
