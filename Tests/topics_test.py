import unittest
from sources.ESP8266.topics import explode_topic


class topics_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions du fichier topics."""

    def test_explode_topic_base_and_info(self):
        etopic = explode_topic("search/1")
        self.assertEqual("search", etopic["base"])
        self.assertEqual("1", etopic["info"])

    def test_explode_topic_base_without_info(self):
        etopic = explode_topic("end")
        self.assertEqual("end", etopic["base"])
        self.assertEqual("", etopic["info"])

    def test_explode_topic_base_with_complex_info(self):
        etopic = explode_topic("search/1/2")
        self.assertEqual("search", etopic["base"])
        self.assertEqual("1/2", etopic["info"])
