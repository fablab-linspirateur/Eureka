import unittest
from sources.ESP8266.displayer import displayer


class displayer_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions des fonctions du fichier boot ESP8266."""

    def setUp(self):
        self.COMPONENTS_EMPTY = "./Tests/components_empty.txt"
        self.COMPONENTS_ONE = "./Tests/components_one.txt"
        self.COMPONENTS_FIFTEEN = "./Tests/components_fifteen.txt"
        self.COMPONENT_ONE_ID = "123"

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
        color = disp.to_color(0x00000000)
        self.assertEqual(color, (0, 0, 0, 0))

    def test_to_color_white_half(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0x0000007f)
        self.assertEqual(color, (0, 0, 0, 127))

    def test_to_color_red_full(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0xff000000)
        self.assertEqual(color, (255, 0, 0, 0))

    def test_to_color_green_hundred(self):
        disp = displayer(self.COMPONENTS_ONE)
        color = disp.to_color(0x00640000)
        self.assertEqual(color, (0, 100, 0, 0))

    def test_get_components_file_empty(self):
        disp = displayer(self.COMPONENTS_EMPTY)
        self.assertEqual(disp.displayed, {})

    def test_get_components_file_one(self):
        disp = displayer(self.COMPONENTS_ONE)
        self.assertEqual(disp.displayed, {
                         self.COMPONENT_ONE_ID: {0x00000000: [1, 8]}})

    def test_get_components_file_fifteen(self):
        disp = displayer(self.COMPONENTS_FIFTEEN)
        result = {
            "1": {0x00000000: [1, 8]},
            "2": {0x00000000: [1, 8]},
            "3": {0x00000000: [1, 8]},
            "4": {0x00000000: [1, 8]},
            "5": {0x00000000: [1, 8]},
            "6": {0x00000000: [1, 8]},
            "7": {0x00000000: [1, 8]},
            "8": {0x00000000: [1, 8]},
            "9": {0x00000000: [1, 8]},
            "10": {0x00000000: [1, 8]},
            "11": {0x00000000: [1, 8]},
            "12": {0x00000000: [1, 8]},
            "13": {0x00000000: [1, 8]},
            "14": {0x00000000: [1, 8]},
            "15": {0x00000000: [1, 8]}
        }
        self.assertEqual(disp.displayed, result)

    def test_update_component_black(self):
        disp = displayer(self.COMPONENTS_ONE)
        result = {
            self.COMPONENT_ONE_ID: {0x00000000: [1, 8]}
        }
        disp.update(disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(disp.displayed, result)

    def test_update_component_one(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: []
            }
        }
        result = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 8]
            }
        }
        disp.update(disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(disp.displayed, result)

    def test_update_component_two(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 8],
                0x00640000: []
            }
        }
        result = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 4],
                0x00640000: [5, 8]
            }
        }
        disp.update(disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(disp.displayed, result)

    def test_update_component_three(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 4],
                0x00640000: [5, 8],
                0x00006400: []
            }
        }
        result = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 3],
                0x00640000: [4, 5],
                0x00006400: [6, 8]
            }
        }
        disp.update(disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(disp.displayed, result)

    def test_update_component_four(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 3],
                0x00640000: [4, 6],
                0x00006400: [7, 8],
                0x00000064: []
            }
        }
        result = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 2],
                0x00640000: [3, 4],
                0x00006400: [5, 6],
                0x00000064: [7, 8]
            }
        }
        disp.update(disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(disp.displayed, result)

    def test_update_component_five(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 2],
                0x00640000: [3, 4],
                0x00006400: [5, 6],
                0x00000064: [7, 8],
                0x64000064: []
            }
        }
        result = {
            self.COMPONENT_ONE_ID: {
                0x00000000: [1, 8],
                0x64000000: [1, 2],
                0x00640000: [3, 4],
                0x00006400: [5, 6],
                0x00000064: [7, 8]
            }
        }
        disp.update(disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(disp.displayed, result)

    def test_add_component_to_black(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x64000000)
        self.assertIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_component_to_black_plus_one(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x00640000)
        self.assertIn(0x00640000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(3, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_component_to_black_plus_four(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: [],
            0x00640000: [],
            0x00006400: [],
            0x00000064: []
        }
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x11111111)
        self.assertNotIn(0x11111111, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(5, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_component_existing_black(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x00000000)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_add_component_existing_other(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x64000000)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x00000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_component_existing(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x64000000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x00000000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertNotIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_component_black(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x00000000)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x00000000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_component_unexisting(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x00640000)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x00000000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_component_existing_from_multiple(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: [],
            0x00640000: [],
            0x00006400: [],
            0x00000064: []
        }
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x00640000)
        self.assertEqual(4, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x00640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_in_empty(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component(self.COMPONENT_ONE_ID, 0x64000000)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_in_filled(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.display_component(self.COMPONENT_ONE_ID, 0x00640000)
        self.assertEqual(3, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x00640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_unexisting(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.display_component("unexisting", 0x00640000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn("unexisting", disp.displayed)

    def test_turn_off_if_present(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.turn_off(0x64000000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x64000000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_turn_off_if_absent(self):
        disp = displayer(self.COMPONENTS_ONE)
        disp.displayed[self.COMPONENT_ONE_ID] = {
            0x00000000: [1, 8],
            0x64000000: []
        }
        disp.turn_off(0x00640000)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
