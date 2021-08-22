import time
import unittest
from random import random
from typing import Any

from parameterized import parameterized

from mediapills.dependency_injection import Injector
from mediapills.dependency_injection.exceptions import FrozenServiceException
from mediapills.dependency_injection.exceptions import InvalidServiceIdentifierException
from mediapills.dependency_injection.exceptions import ProtectedServiceException
from mediapills.dependency_injection.exceptions import UnknownIdentifierException

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


class TestInjectorBase(unittest.TestCase):
    def test_get_missing_should_raise_error(self) -> None:

        obj = Injector()

        with self.assertRaises(KeyError):
            obj["key"]

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_setter_should_set_value(self, key: str, val: Any) -> None:

        obj = Injector()
        obj[key] = val

        self.assertEqual(val, obj[key])

    def test_list_should_be_empty(self) -> None:

        obj = Injector()

        self.assertEqual([], list(obj))

    def test_list_should_return_keys(self) -> None:

        obj = Injector()
        obj["apple"] = None
        obj["banana"] = None
        obj["cherry"] = None

        self.assertListEqual(["apple", "banana", "cherry"], list(obj))

    def test_del_missing_should_raise_error(self) -> None:

        obj = Injector()

        with self.assertRaises(KeyError):
            del obj["key"]

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_del_should_remove_value(self, key: str, val: Any) -> None:

        obj = Injector()
        obj[key] = val
        del obj[key]

        with self.assertRaises(KeyError):
            obj["key"]

    def test_clear_empty_should_reset(self) -> None:

        obj = Injector()
        obj.clear()

        self.assertEqual(0, len(obj))

    def test_clear_should_clear(self) -> None:

        obj = Injector()
        obj["apple"] = None
        obj["banana"] = None
        obj["cherry"] = None
        obj.clear()

        self.assertEqual(0, len(obj))

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_get_should_return_value(self, key: str, val: Any) -> None:

        obj = Injector()
        obj[key] = val

        self.assertEqual(val, obj.get(key, None))

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_get_should_return_default(self, key: str, val: Any) -> None:

        obj = Injector()
        obj[key] = val

        self.assertIsNone(obj.get("non-existent", None))

    def test_keys_should_return_list(self) -> None:

        obj = Injector()
        obj["apple"] = None
        obj["banana"] = None
        obj["cherry"] = None

        self.assertListEqual(["apple", "banana", "cherry"], [*obj.keys()])

    def test_pop_should_return_offset_and_remove(self) -> None:

        obj = Injector()
        obj["1"] = "one"
        obj["2"] = "two"

        val = obj.pop("1")
        self.assertEqual("one", val)
        self.assertEqual(1, len(obj))

    def test_values_should_return_list(self) -> None:

        obj = Injector()
        obj["1"] = lambda x: "one"
        obj["2"] = lambda x: "two"
        obj["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertListEqual(["one", "two", "one + two"], [*obj.values()])

    def test_items_should_return_list(self) -> None:

        obj = Injector()
        obj["1"] = lambda x: "one"
        obj["2"] = lambda x: "two"
        obj["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertListEqual(
            [("1", "one"), ("2", "two"), ("1 + 2", "one + two")], [*obj.items()]
        )

    def test_copy_should_return_warmed_copy(self) -> None:

        obj = Injector()
        obj["1"] = lambda x: "one"
        obj["2"] = lambda x: "two"
        obj["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertDictEqual({"1": "one", "1 + 2": "one + two", "2": "two"}, obj.copy())

    def test_update_should_change_value(self) -> None:

        obj = Injector()
        obj["1"] = lambda x: "one"
        obj.update({"1": lambda x: "uno"})

        self.assertEqual("uno", obj["1"])

    def test_update_should_raise_error(self) -> None:

        obj = Injector()
        obj["1"] = lambda x: "one"
        _ = obj["1"]

        with self.assertRaises(FrozenServiceException):
            obj.update({"1": lambda x: "uno"})


class TestInjector(unittest.TestCase):
    def test_raw_warmed_should_be_same_as_initial(self) -> None:
        func = lambda i: "test"  # noqa: E731

        obj = Injector()
        obj["func"] = func

        _ = obj["func"]

        self.assertEqual(func, obj.raw("func"))

    def test_raw_cold_should_be_same_as_initial(self) -> None:
        func = lambda i: "test"  # noqa: E731

        obj = Injector()
        obj["func"] = func

        self.assertEqual(func, obj.raw("func"))

    def test_call_protected_should_return_different(self) -> None:
        obj = Injector()
        obj["func"] = lambda i: "time: '{}', rnad: '{}'".format(
            time.time() * 1000, random()
        )
        obj.protect("func")

        self.assertNotEqual(obj["func"], obj["func"])

    def test_call_non_protected_should_return_same(self) -> None:
        obj = Injector()
        obj["func"] = lambda i: "time: '{}', rnad: '{}'".format(
            time.time() * 1000, random()
        )

        self.assertEqual(obj["func"], obj["func"])

    def test_extend_nonexistent_should_raise_error(self) -> None:

        obj = Injector()

        with self.assertRaises(UnknownIdentifierException):
            obj.extend("any", lambda i: "error")

    def test_extend_frozen_should_raise_error(self) -> None:

        obj = Injector()
        obj["any"] = lambda i: "test"
        _ = obj["any"]

        with self.assertRaises(FrozenServiceException):
            obj.extend("any", lambda i: "error")

    def test_extend_protected_should_raise_error(self) -> None:

        obj = Injector()
        obj["any"] = lambda i: "test"
        obj.protect("any")

        with self.assertRaises(ProtectedServiceException):
            obj.extend("any", lambda i: "error")

    def test_extend_scalar_should_raise_error(self) -> None:

        obj = Injector()
        obj["any"] = "test"

        with self.assertRaises(InvalidServiceIdentifierException):
            obj.extend("any", lambda i: "error")

    def test_extend_should_ok(self) -> None:

        obj = Injector()
        obj["any"] = lambda i: "base"

        obj.extend("any", lambda base, di: "extended " + base)

        self.assertEqual("extended base", obj["any"])
