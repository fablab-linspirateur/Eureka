import unittest
from sources.ESP8266.displayer import displayer


class displayer_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions des fonctions du fichier boot ESP8266."""

    def setUp(self):
        self.COMPONENTS_EMPTY = "./Tests/components_empty.txt"
        self.COMPONENTS_ONE = "./Tests/components_one.txt"
        self.COMPONENTS_TWO = "./Tests/components_two.txt"
        self.COMPONENTS_FIFTEEN = "./Tests/components_fifteen.txt"
        self.COMPONENT_ONE_ID = "123"
        self.COMPONENT_TWO_ID = "456"

    def test_explode_topic_base_and_info(self):
        disp = displayer(self.COMPONENTS_ONE)
        etopic = disp.explode_topic("search/1")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1")

    def test_explode_topic_base_without_info(self):
        disp = displayer(self.COMPONENTS_ONE)
        etopic = disp.explode_topic("end")
        self.assertEqual(etopic["base"], "end")
        self.assertEqual(etopic["info"], "")

    def test_explode_topic_base_with_complex_info(self):
        disp = displayer(self.COMPONENTS_ONE)
        etopic = disp.explode_topic("search/1/2")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1/2")

    def test_to_color_off(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0x000000)
        self.assertEqual(color, (0, 0, 0))

    def test_to_color_white_half(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0x7f7f7f)
        self.assertEqual(color, (127, 127, 127))

    def test_to_color_red_full(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0xff0000)
        self.assertEqual(color, (255, 0, 0))

    def test_to_color_green_hundred(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0x006400)
        self.assertEqual(color, (0, 100, 0))

    def test_get_components_file_empty(self):
        disp = displayer(self.COMPONENTS_EMPTY)
        self.assertEqual(disp.displayed, {})

    def test_get_components_file_one(self):
        disp = displayer(self.COMPONENTS_ONE)
        self.assertEqual(disp.displayed, {self.COMPONENT_ONE_ID: []})

    def test_get_components_file_fifteen(self):
        disp = displayer(self.COMPONENTS_FIFTEEN)
        result = {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": [],
            "9": [],
            "10": [],
            "11": [],
            "12": [],
            "13": [],
            "14": [],
            "15": []
        }
        self.assertEqual(disp.displayed, result)

    def test_add_to_empty(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x640000)
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_to_one(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x006400)
        self.assertIn(0x006400, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_to_four(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000,
            0x006400,
            0x000064,
            0x7f7f7f
        ]
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x11111111)
        self.assertNotIn(0x11111111, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(4, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_existing(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x640000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_existing_solo(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x640000)
        self.assertEqual(0, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_existing_multi(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x006400,
            0x000064,
            0x640000
        ]
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_unexisting(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x000064,
            0x640000
        ]
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x000064, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_in_empty(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_in_filled(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x006400, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_unexisting(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component("unexisting", 0x006400)
        self.assertIn(self.COMPONENT_ONE_ID, disp.displayed)
        self.assertEqual(0, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn("unexisting", disp.displayed)

    def test_turn_off_if_present(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.turn_off(0x640000)
        self.assertEqual(0, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_turn_off_if_absent(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x000000,
            0x640000
        ]
        disp.turn_off(0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_to_neopixel_empty(self):
        disp = displayer(self.COMPONENTS_EMPTY)
        expected = []
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_no_color(self):
        disp = displayer(self.COMPONENTS_ONE)
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_one_color(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_two_color(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_three_color(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        disp.display_component(self.COMPONENT_ONE_ID, 0x000064)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 100), (0, 0, 100), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_four_color(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        disp.display_component(self.COMPONENT_ONE_ID, 0x000064)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006464)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 100), (0, 0, 100), (0, 100, 100), (0, 100, 100), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_two_no_color(self):
        disp = displayer(self.COMPONENTS_TWO)
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_one_component_one_color(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        result = disp.refresh(bytes(disp.TOPIC_END, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_one_component_two_colors(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        result = disp.refresh(bytes(disp.TOPIC_END, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 100, 0), (0, 100, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_two_components_one_color(self):
        disp = displayer(self.COMPONENTS_TWO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_TWO_ID, 0x640000)
        result = disp.refresh(bytes(disp.TOPIC_END, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_two_components_two_colors(self):
        disp = displayer(self.COMPONENTS_TWO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        disp.display_component(self.COMPONENT_TWO_ID, 0x640000)
        disp.display_component(self.COMPONENT_TWO_ID, 0x000064)
        result = disp.refresh(bytes(disp.TOPIC_END, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 100, 0), (0, 100, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 100), (0, 0, 100), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_search_existing(self):
        disp = displayer(self.COMPONENTS_ONE)
        result = disp.refresh(bytes(disp.TOPIC_SEARCH_BASE + "/" + self.COMPONENT_ONE_ID, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_search_unexisting(self):
        disp = displayer(self.COMPONENTS_ONE)
        result = disp.refresh(bytes(disp.TOPIC_SEARCH_BASE + "/" + self.COMPONENT_TWO_ID, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)
