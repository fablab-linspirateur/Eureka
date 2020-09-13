import unittest
from sources.ESP8266.configuration import get_config


class configuration_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions de la classe displayer."""

    def setUp(self):
        self.CONFIG_EMPTY = "./Tests/config_empty.yaml"
        self.CONFIG_TOTO = "./Tests/config_toto.yaml"

    def test_get_config_no_arg(self):
        expected = {
            "network": "demo-network",
            "password": "demo-password",
            "name": "demo-name",
            "broker": "demo-broker",
            "port": 42
        }
        import os
        path_bckp = os.getcwd()
        os.chdir("./Tests")
        result = get_config()
        os.chdir(path_bckp)
        self.assertEqual(expected, result)

    def test_get_config_empty(self):
        expected = {}
        result = get_config(self.CONFIG_EMPTY)
        self.assertEqual(expected, result)

    def test_get_config_toto(self):
        expected = {
            "network": "tata",
            "password": "titi",
            "name": "toto",
            "broker": "tutu",
            "port": 42
        }
        result = get_config(self.CONFIG_TOTO)
        self.assertEqual(expected, result)
