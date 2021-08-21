import unittest
from typing import Any

from parameterized import parameterized

from mediapills.dependency_injection import Container
from mediapills.dependency_injection.exceptions import FrozenServiceException

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


class TestContainerBase(unittest.TestCase):
    def test_get_missing_should_raise_error(self) -> None:

        c = Container()

        with self.assertRaises(KeyError):
            c["key"]

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_setter_should_set_value(self, key: str, val: Any) -> None:

        c = Container()
        c[key] = val

        self.assertEqual(val, c[key])

    def test_list_should_be_empty(self) -> None:

        c = Container()

        self.assertEqual([], list(c))

    def test_list_should_return_keys(self) -> None:

        c = Container()
        c["apple"] = None
        c["banana"] = None
        c["cherry"] = None

        self.assertListEqual(["apple", "banana", "cherry"], list(c))

    def test_del_missing_should_raise_error(self) -> None:

        c = Container()

        with self.assertRaises(KeyError):
            del c["key"]

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_del_should_remove_value(self, key: str, val: Any) -> None:

        c = Container()
        c[key] = val
        del c[key]

        with self.assertRaises(KeyError):
            c["key"]

    def test_clear_empty_should_reset(self) -> None:

        c = Container()
        c.clear()

        self.assertEqual(0, len(c))

    def test_clear_should_clear(self) -> None:

        c = Container()
        c["apple"] = None
        c["banana"] = None
        c["cherry"] = None
        c.clear()

        self.assertEqual(0, len(c))

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_get_should_return_value(self, key: str, val: Any) -> None:

        c = Container()
        c[key] = val

        self.assertEqual(val, c.get(key, None))

    @parameterized.expand(DATA_TYPES_PARAMETRIZED_INPUT)  # type: ignore
    def test_get_should_return_default(self, key: str, val: Any) -> None:

        c = Container()
        c[key] = val

        self.assertIsNone(c.get("non-existent", None))

    def test_keys_should_return_list(self) -> None:

        c = Container()
        c["apple"] = None
        c["banana"] = None
        c["cherry"] = None

        self.assertListEqual(["apple", "banana", "cherry"], [*c.keys()])

    def test_pop_should_return_offset_and_remove(self) -> None:

        c = Container()
        c["1"] = "one"
        c["2"] = "two"

        val = c.pop("1")
        self.assertEqual("one", val)
        self.assertEqual(1, len(c))

    def test_values_should_return_list(self) -> None:

        c = Container()
        c["1"] = lambda x: "one"
        c["2"] = lambda x: "two"
        c["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertListEqual(["one", "two", "one + two"], [*c.values()])

    def test_items_should_return_list(self) -> None:

        c = Container()
        c["1"] = lambda x: "one"
        c["2"] = lambda x: "two"
        c["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertListEqual(
            [("1", "one"), ("2", "two"), ("1 + 2", "one + two")], [*c.items()]
        )

    def test_copy_should_return_warmed_copy(self) -> None:

        c = Container()
        c["1"] = lambda x: "one"
        c["2"] = lambda x: "two"
        c["1 + 2"] = lambda x: "{} + {}".format(x["1"], x["2"])

        self.assertDictEqual({"1": "one", "1 + 2": "one + two", "2": "two"}, c.copy())

    def test_update_should_change_value(self) -> None:

        c = Container()
        c["1"] = lambda x: "one"
        c.update({"1": lambda x: "uno"})

        self.assertEqual("uno", c["1"])

    def test_update_should_raise_error(self) -> None:

        c = Container()
        c["1"] = lambda x: "one"
        _ = c["1"]

        with self.assertRaises(FrozenServiceException):
            c.update({"1": lambda x: "uno"})
