# Copyright The Mediapills Dependency Injection Authors.
# SPDX-License-Identifier: MIT
from unittest import TestCase

from mediapills.dependency_injection.decorators import ProtectedDecorator
from typing import List, Dict, Any


class TestProtectedDecorator(TestCase):
    def test_lambda_function_decoration_should_work(self) -> None:
        func = ProtectedDecorator(lambda: "test")

        result = func()

        self.assertEqual("test", result)

    def test_function_decoration_should_work(self) -> None:
        @ProtectedDecorator
        def dummy(*args: List[Any], **kwargs: Dict[Any, Any]):
            return "test"

        result = dummy()

        self.assertEqual("test", result)


class TestFactoryDecorator(TestCase):
    def test_lambda_function_decoration_should_work(self) -> None:
        func = ProtectedDecorator(lambda: "test")

        result = func()

        self.assertEqual("test", result)


class TestStringDecorator(TestCase):
    def test_lambda_function_decoration_should_work(self) -> None:
        func = ProtectedDecorator(lambda: "test")

        result = func()

        self.assertEqual("test", result)


class TestAutowiredDecorator(TestCase):
    def test_lambda_function_decoration_should_work(self) -> None:
        func = ProtectedDecorator(lambda: "test")

        result = func()

        self.assertEqual("test", result)
