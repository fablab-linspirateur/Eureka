import unittest
from sources.ESP8266.displayer import displayer


class displayer_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions des fonctions du fichier boot ESP8266."""

    def test_explode_topic_base_and_info(self):
        disp = displayer("./Tests/components_one.txt")
        etopic = disp.explode_topic("search/1")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1")

    def test_explode_topic_base_without_info(self):
        disp = displayer("./Tests/components_one.txt")
        etopic = disp.explode_topic("end")
        self.assertEqual(etopic["base"], "end")
        self.assertEqual(etopic["info"], "")

    def test_explode_topic_base_with_complex_info(self):
        disp = displayer("./Tests/components_one.txt")
        etopic = disp.explode_topic("search/1/2")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1/2")

    def test_to_color_off(self):
        disp = displayer("./Tests/components_one.txt")
        color = disp.to_color(0x00000000)
        self.assertEqual(color, (0, 0, 0, 0))

    def test_to_color_white_half(self):
        disp = displayer("./Tests/components_one.txt")
        color = disp.to_color(0x0000007f)
        self.assertEqual(color, (0, 0, 0, 127))

    def test_to_color_red_full(self):
        disp = displayer("./Tests/components_one.txt")
        color = disp.to_color(0xff000000)
        self.assertEqual(color, (255, 0, 0, 0))

    def test_to_color_green_hundred(self):
        disp = displayer("./Tests/components_one.txt")
        color = disp.to_color(0x00640000)
        self.assertEqual(color, (0, 100, 0, 0))

    def test_get_components_file_empty(self):
        disp = displayer("./Tests/components_empty.txt")
        self.assertEqual(disp.displayed, {})

    def test_get_components_file_one(self):
        disp = displayer("./Tests/components_one.txt")
        self.assertEqual(disp.displayed, {"123": {}})

    def test_get_components_file_fifteen(self):
        disp = displayer("./Tests/components_fifteen.txt")
        result = {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
            "10": {},
            "11": {},
            "12": {},
            "13": {},
            "14": {},
            "15": {}
        }
        self.assertEqual(disp.displayed, result)
