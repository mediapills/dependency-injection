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
from typing import Any
from unittest import TestCase

from parameterized import parameterized

from mediapills.dependency_injection import Container
from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import RecursionInfiniteLoopError

DATA_TYPES_PARAMETRIZED_INPUT = [
    ("str", "value"),  # Check text type (str)
    ("int", 5),  # Check numeric type (int)
    ("float", 6.7),  # Check numeric type (float)
    ("list", ["apple", "banana", "cherry"]),  # Check sequence type (list)
    ("tuple", ("apple", "banana", "cherry")),  # Check sequence type (tuple)
    ("float", range(6)),  # Check sequence type (range)
    ("dict", {"name": "John", "age": 36}),  # Check mapping type (dict)
    ("set", {"apple", "banana", "cherry"}),  # Check set types (set)
    (  # Check set types (frozenset)
        "frozenset",
        frozenset({"apple", "banana", "cherry"}),
    ),
    ("bool", True),  # Check boolean type (bool)
    ("bytes", b"Hello"),  # Check binary types (bytes)
    ("bytearray", bytearray(5)),  # Check binary types (bytearray)
    ("memoryview", memoryview(bytes(5))),  # Check binary types (memoryview)
]


class TestContainerBase(TestCase):
    """Test Dict Base Container implementation."""

    def test_get_constructor_should_set(self) -> None:
        obj = Container(
            {"param1": "value 1", "param2": lambda di: di["param1"] + " changed"}
        )

        self.assertEqual("value 1", obj["param1"])
        self.assertEqual("value 1 changed", obj["param2"])

    def test_get_missing_should_raise_error(self) -> None:

        obj = Container()

        with self.assertRaises(KeyError):
            _ = obj["key"]

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_setter_should_set_value(self, key: str, val: Any) -> None:

        obj = Container()
        obj[key] = val

        self.assertEqual(val, obj[key])

    def test_list_should_be_empty(self) -> None:

        obj = Container()

        self.assertEqual([], list(obj))

    def test_list_should_return_keys(self) -> None:

        obj = Container()
        obj["apple"] = None
        obj["banana"] = None
        obj["cherry"] = None

        self.assertListEqual(["apple", "banana", "cherry"], list(obj))

    def test_del_missing_should_raise_error(self) -> None:

        obj = Container()

        with self.assertRaises(KeyError):
            del obj["key"]

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_del_should_remove_value(self, key: str, val: Any) -> None:

        obj = Container()
        obj[key] = val
        del obj[key]

        with self.assertRaises(KeyError):
            _ = obj["key"]

    def test_clear_empty_should_reset(self) -> None:

        obj = Container()
        obj.clear()

        self.assertEqual(0, len(obj))

    def test_clear_should_clear(self) -> None:

        obj = Container()
        obj["apple"] = None
        obj["banana"] = None
        obj["cherry"] = None
        obj.clear()

        self.assertEqual(0, len(obj))

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_get_should_return_value(self, key: str, val: Any) -> None:

        obj = Container()
        obj[key] = val

        self.assertEqual(val, obj.get(key, None))

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_get_should_return_default(self, key: str, val: Any) -> None:

        obj = Container()
        obj[key] = val

        self.assertIsNone(obj.get("non-existent", None))

    def test_recursive_get_should_raise_error(self) -> None:
        obj = Container()
        obj["a"] = lambda di: di["b"]
        obj["b"] = lambda di: di["a"]

        with self.assertRaises(RecursionInfiniteLoopError):
            _ = obj["a"]

    def test_keys_should_return_list(self) -> None:

        obj = Container()
        obj["apple"] = None
        obj["banana"] = None
        obj["cherry"] = None

        self.assertListEqual(["apple", "banana", "cherry"], [*obj.keys()])

    def test_pop_should_return_offset_and_remove(self) -> None:

        obj = Container()
        obj["1"] = "one"
        obj["2"] = "two"

        val = obj.pop("1")
        self.assertEqual("one", val)
        self.assertEqual(1, len(obj))

    def test_values_should_return_list(self) -> None:

        obj = Container()
        obj["1"] = lambda x: "one"
        obj["2"] = lambda x: "two"
        obj["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertListEqual(["one", "two", "one + two"], [*obj.values()])

    def test_items_should_return_list(self) -> None:

        obj = Container()
        obj["1"] = lambda x: "one"
        obj["2"] = lambda x: "two"
        obj["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertListEqual(
            [("1", "one"), ("2", "two"), ("1 + 2", "one + two")], [*obj.items()]
        )

    def test_copy_should_return_warmed_copy(self) -> None:

        obj = Container()
        obj["1"] = lambda x: "one"
        obj["2"] = lambda x: "two"
        obj["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertDictEqual({"1": "one", "1 + 2": "one + two", "2": "two"}, obj.copy())

    def test_update_should_change_value(self) -> None:

        obj = Container()
        obj["1"] = lambda x: "one"
        obj.update({"1": lambda x: "uno"})

        self.assertEqual("uno", obj["1"])

    def test_update_should_raise_error(self) -> None:

        obj = Container()
        obj["1"] = lambda x: "one"
        _ = obj["1"]

        with self.assertRaises(FrozenServiceException):
            obj.update({"1": lambda x: "uno"})


class TestContainer(TestCase):
    """Test Custom Dict Container implementation."""

    def test_raw_warmed_should_be_same_as_initial(self) -> None:

        func = lambda i: "test"  # noqa: E731

        obj = Container()
        obj["func"] = func

        _ = obj["func"]

        self.assertEqual(func, obj.raw("func"))

    def test_raw_cold_should_be_same_as_initial(self) -> None:

        func = lambda i: "test"  # noqa: E731

        obj = Container()
        obj["func"] = func

        self.assertEqual(func, obj.raw("func"))

    def test_service_decorator_should_set_callable(self) -> None:
        obj = Container()

        @obj.service("test")
        def dummy(di: Container):  # type: ignore
            return "Dummy output"

        self.assertEqual("Dummy output", obj["test"])

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_service_decorator_should_set_value(self, key: str, val: Any) -> None:

        obj = Container()
        obj.service(key)(val)

        self.assertEqual(val, obj[key])

    # def test_call_protected_should_return_different(self) -> None:
    #
    #     obj = Container()
    #     obj["func"] = lambda i: "time: '{}', rnad: '{}'".format(
    #         time.time() * 1000, random()
    #     )
    #     obj.protect("func")
    #
    #     self.assertNotEqual(obj["func"], obj["func"])
    #
    # def test_call_protected_unavailable_should_raise_exception(self) -> None:
    #     obj = Container()
    #
    #     with self.assertRaises(UnknownIdentifierException):
    #         obj.protect("func")
    #
    # def test_call_non_protected_should_return_same(self) -> None:
    #
    #     obj = Container()
    #     obj["func"] = lambda i: "time: '{}', rnad: '{}'".format(
    #         time.time() * 1000, random()
    #     )
    #
    #     self.assertEqual(obj["func"], obj["func"])
    #
    # def test_extend_nonexistent_should_raise_error(self) -> None:
    #
    #     obj = Container()
    #
    #     with self.assertRaises(UnknownIdentifierException):
    #         obj.extend("any", lambda i: "error")
    #
    # def test_extend_frozen_should_raise_error(self) -> None:
    #
    #     obj = Container()
    #     obj["any"] = lambda i: "test"
    #     _ = obj["any"]
    #
    #     with self.assertRaises(FrozenServiceException):
    #         obj.extend("any", lambda i: "error")
    #
    # def test_extend_protected_should_raise_error(self) -> None:
    #
    #     obj = Container()
    #     obj["any"] = lambda i: "test"
    #     obj.protect("any")
    #
    #     with self.assertRaises(ProtectedServiceException):
    #         obj.extend("any", lambda i: "error")
    #
    # def test_extend_scalar_should_raise_error(self) -> None:
    #
    #     obj = Container()
    #     obj["any"] = "test"
    #
    #     with self.assertRaises(ExpectedInvokableException):
    #         obj.extend("any", lambda i: "error")
    #
    # def test_extend_should_ok(self) -> None:
    #
    #     obj = Container()
    #     obj["any"] = lambda i: "base"
    #
    #     obj.extend("any", lambda base, di: "extended " + base)
    #
    #     self.assertEqual("extended base", obj["any"])
