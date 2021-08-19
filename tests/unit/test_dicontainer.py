import unittest

from mediapills.dicontainer import Container  # type: ignore

# TODO cover all functions https://docs.python.org/3/library/stdtypes.html#typesmapping


class TestContainer(unittest.TestCase):
    def test_dummy(self) -> None:
        Container()

        self.assertTrue(True)
