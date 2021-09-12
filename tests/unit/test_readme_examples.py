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
import unittest

from mediapills.dependency_injection import Container


class DummySessionStorage:
    def __init__(self, cookie_name: str):
        self._cookie_name: str = cookie_name

    @property
    def cookie_name(self) -> str:

        return self._cookie_name


class DummySession:
    def __init__(self, storage: DummySessionStorage):

        self._storage = storage

    @property
    def storage(self) -> DummySessionStorage:

        return self._storage


class TestContainerExamples(unittest.TestCase):
    def test_defining_services_section(self) -> None:
        obj = Container()

        obj["session_storage"] = lambda i: (DummySessionStorage("SESSION_ID"))

        obj["session"] = lambda i: (DummySession(i["session_storage"]))

        obj_session = obj["session"]

        storage = DummySessionStorage("SESSION_ID")
        raw_session = DummySession(storage)

        self.assertEqual(
            raw_session.storage.cookie_name, obj_session.storage.cookie_name
        )

    def test_defining_factory_services_section(self) -> None:

        # TODO: implement this test
        pass

    def test_defining_defining_parameters_section(self) -> None:

        obj = Container()

        obj["cookie_name"] = "SESSION_ID"
        obj["session_storage_cls"] = DummySessionStorage
        obj["session_storage"] = lambda i: (i["session_storage_cls"](i["cookie_name"]))

        _ = obj["session_storage"]
        storage = obj["session_storage"]

        self.assertEqual("SESSION_ID", storage.cookie_name)

    def test_example_modifying_services_after_definition(self) -> None:

        # TODO: implement this test
        pass

    def test_fetching_the_service_creation_function(self) -> None:

        # TODO: implement this test
        pass
