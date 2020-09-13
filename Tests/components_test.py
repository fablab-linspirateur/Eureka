import unittest
from sources.ESP8266.components import get_components


class components_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions de la classe displayer."""

    def setUp(self):
        self.COMPONENTS_EMPTY = "./Tests/components_empty.txt"
        self.COMPONENTS_ONE = "./Tests/components_one.txt"
        self.COMPONENTS_FIFTEEN = "./Tests/components_fifteen.txt"
        self.COMPONENT_ONE_ID = "123"

    def test_get_components_no_arg(self):
        import os
        path_bckp = os.getcwd()
        os.chdir("./Tests")
        expected = ["1"]
        result = get_components()
        os.chdir(path_bckp)
        self.assertEqual(expected, result)

    def test_get_components_file_empty(self):
        expected = []
        result = get_components(self.COMPONENTS_EMPTY)
        self.assertEqual(expected, result)

    def test_get_components_file_one(self):
        expected = [self.COMPONENT_ONE_ID]
        result = get_components(self.COMPONENTS_ONE)
        self.assertEqual(expected, result)

    def test_get_components_file_fifteen(self):
        expected = ["1", "2", "3", "4", "5", "6", "7",
                    "8", "9", "10", "11", "12", "13", "14", "15"]
        result = get_components(self.COMPONENTS_FIFTEEN)
        self.assertEqual(expected, result)

