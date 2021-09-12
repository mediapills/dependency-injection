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
