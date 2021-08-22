import unittest

from mediapills.dependency_injection import Injector


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


class TestInjectorExamples(unittest.TestCase):
    def test_defining_services_section(self) -> None:
        obj = Injector()

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

        obj = Injector()

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
