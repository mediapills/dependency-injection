import unittest
from typing import Any

from parameterized import parameterized

from mediapills.dependency_injection import Container

# TODO cover all functions https://docs.python.org/3/library/stdtypes.html#typesmapping

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


class TestContainer(unittest.TestCase):
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

        self.assertEqual(["apple", "banana", "cherry"], list(c))

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


"""

copy()

    Return a shallow copy of the dictionary.

classmethod fromkeys(iterable[, value])

    Create a new dictionary with keys from iterable and values set to value.

    fromkeys() is a class method that returns a new dictionary. value defaults to None.
    All of the values refer to just a single instance, so it generally doesn’t make sense
    for value to be a mutable object such as an empty list. To get distinct values, use a
    dict comprehension instead.

items()

    Return a new view of the dictionary’s items ((key, value) pairs). See the
    documentation of view objects.

keys()

    Return a new view of the dictionary’s keys. See the documentation of view objects.

pop(key[, default])

    If key is in the dictionary, remove it and return its value, else return default. If
    default is not given and key is not in the dictionary, a KeyError is raised.

popitem()

    Remove and return a (key, value) pair from the dictionary. Pairs are returned in LIFO
    order.

    popitem() is useful to destructively iterate over a dictionary, as often used in set
    algorithms. If the dictionary is empty, calling popitem() raises a KeyError.

    Changed in version 3.7: LIFO order is now guaranteed. In prior versions, popitem()
    would return an arbitrary key/value pair.

reversed(d)

    Return a reverse iterator over the keys of the dictionary. This is a shortcut for
    reversed(d.keys()).

    New in version 3.8.

setdefault(key[, default])

    If key is in the dictionary, return its value. If not, insert key with a value of
    default and return default. default defaults to None.

update([other])

    Update the dictionary with the key/value pairs from other, overwriting existing keys.
    Return None.

    update() accepts either another dictionary object or an iterable of key/value pairs
    (as tuples or other iterables of length two). If keyword arguments are specified, the
    dictionary is then updated with those key/value pairs: d.update(red=1, blue=2).

values()

    Return a new view of the dictionary’s values. See the documentation of view objects.
"""
