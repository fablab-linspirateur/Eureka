import random
import unittest
from sources.ESP8266.displayer import explode_topic


class displayer_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions des fonctions du fichier boot ESP8266."""

    def test_explode_topic_base_and_info(self):
        etopic = explode_topic("search/1")
        print(etopic)
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1")

    def test_explode_topic_base_without_info(self):
        etopic = explode_topic("end")
        self.assertEqual(etopic["base"], "end")
        self.assertEqual(etopic["info"], "")

    def test_explode_topic_base_with_complex_info(self):
        etopic = explode_topic("search/1/2")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1/2")
