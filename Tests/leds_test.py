import unittest
from sources.ESP8266.leds import init_component_leds, to_color, component_leds, display_component, display_background, turn_off, LED_OFF, turn_all, to_neopixel, add, remove, COLOR_BLACK, MAX_COLOR


class leds_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions du fichier leds."""

    def setUp(self):
        self.COMPONENT_ONE_ID = "123"
        self.COMPONENT_TWO_ID = "456"
        self.component_leds = {}
        self.backgrounds = {}
        self.NB_LEDS = 10

    def test_init_component_leds_empty(self):
        expected = {}
        init_component_leds([], self.component_leds)
        self.assertEqual(expected, self.component_leds)

    def test_init_component_leds_filled(self):
        expected = {self.COMPONENT_ONE_ID: []}
        init_component_leds([self.COMPONENT_ONE_ID], self.component_leds)
        self.assertEqual(expected, self.component_leds)

    def test_display_component_in_empty(self):
        self.component_leds[self.COMPONENT_ONE_ID] = []
        display_component(self.COMPONENT_ONE_ID, 0x640000, self.component_leds)
        self.assertEqual(1, len(self.component_leds[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, self.component_leds[self.COMPONENT_ONE_ID])

    def test_display_component_in_filled(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        display_component(self.COMPONENT_ONE_ID, 0x006400, self.component_leds)
        self.assertEqual(2, len(self.component_leds[self.COMPONENT_ONE_ID]))
        self.assertIn(0x006400, self.component_leds[self.COMPONENT_ONE_ID])

    def test_display_component_unexisting(self):
        self.component_leds[self.COMPONENT_ONE_ID] = []
        display_component("unexisting", 0x006400, self.component_leds)
        self.assertIn(self.COMPONENT_ONE_ID, self.component_leds)
        self.assertEqual(0, len(self.component_leds[self.COMPONENT_ONE_ID]))
        self.assertNotIn("unexisting", self.component_leds)

    def test_display_background_unexisting(self):
        components = [self.COMPONENT_ONE_ID]
        display_background("unexisting", 0x006400,
                           components, self.backgrounds)
        self.assertNotIn(self.COMPONENT_ONE_ID, self.backgrounds.keys())

    def test_display_background_existing(self):
        components = [self.COMPONENT_ONE_ID]
        display_background(self.COMPONENT_ONE_ID, 0x006400,
                           components, self.backgrounds)
        self.assertIn(self.COMPONENT_ONE_ID, self.backgrounds.keys())

    def test_turn_off_if_present(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        turn_off(0x640000, self.component_leds)
        self.assertEqual(0, len(self.component_leds[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x640000, self.component_leds[self.COMPONENT_ONE_ID])

    def test_turn_off_if_absent(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [
            0x000000,
            0x640000
        ]
        turn_off(0x006400, self.component_leds)
        self.assertEqual(2, len(self.component_leds[self.COMPONENT_ONE_ID]))

    def test_turn_all_no_param(self):
        expected = [LED_OFF]*self.NB_LEDS
        result = turn_all(nb=self.NB_LEDS)
        self.assertEqual(expected, result)

    def test_turn_all_green(self):
        expected = [(0, 100, 0)]*self.NB_LEDS
        result = turn_all(0x006400, nb=self.NB_LEDS)
        self.assertEqual(expected, result)

    def test_to_color_off(self):
        expected = (0, 0, 0)
        result = to_color(0x000000)
        self.assertEqual(expected, result)

    def test_to_color_white_half(self):
        expected = (127, 127, 127)
        result = to_color(0x7f7f7f)
        self.assertEqual(expected, result)

    def test_to_color_red_full(self):
        expected = (255, 0, 0)
        result = to_color(0xff0000)
        self.assertEqual(expected, result)

    def test_to_color_green_hundred(self):
        expected = (0, 100, 0)
        result = to_color(0x006400)
        self.assertEqual(expected, result)

    def test_to_neopixel_empty(self):
        expected = []
        result = to_neopixel(self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_no_color(self):
        self.component_leds[self.COMPONENT_ONE_ID] = []
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID], self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_one_color(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [0x640000]
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (100, 0, 0),
                    (100, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID], self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_two_color(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [0x640000, 0x006400]
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (100, 0, 0), (100, 0, 0),
                    (0, 100, 0), (0, 100, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID], self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_three_color(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [
            0x640000, 0x006400, 0x000064]
        expected = [(0, 0, 0), (0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0),
                    (0, 100, 0), (0, 0, 100), (0, 0, 100), (0, 0, 0), (0, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID], self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_four_color(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [
            0x640000, 0x006400, 0x000064, 0x006464]
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 100), (0, 0, 100), (0, 100, 100), (0, 100, 100), (0, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID], self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_two_no_color(self):
        self.component_leds[self.COMPONENT_ONE_ID] = []
        self.component_leds[self.COMPONENT_TWO_ID] = []
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = to_neopixel(
            [self.COMPONENT_ONE_ID, self.COMPONENT_TWO_ID], self.component_leds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_no_color_one_background(self):
        self.component_leds[self.COMPONENT_ONE_ID] = []
        self.backgrounds = {self.COMPONENT_ONE_ID: 0xff0000}
        expected = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),
                    (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID],
                             self.component_leds, self.backgrounds)
        self.assertEqual(expected, result)

    def test_to_neopixel_one_one_color_one_background(self):
        self.component_leds[self.COMPONENT_ONE_ID] = [0x640000]
        self.backgrounds = {self.COMPONENT_ONE_ID: 0xff0000}
        expected = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (100, 0, 0),
                    (100, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]
        result = to_neopixel([self.COMPONENT_ONE_ID],
                             self.component_leds, self.backgrounds)
        self.assertEqual(expected, result)

    def test_add_to_empty(self):
        components_color = []
        add(components_color, 0x640000)
        self.assertIn(0x640000, components_color)
        self.assertEqual(1, len(components_color))

    def test_add_black(self):
        components_color = []
        add(components_color, COLOR_BLACK)
        self.assertNotIn(COLOR_BLACK, components_color)
        self.assertEqual(0, len(components_color))

    def test_add_to_one(self):
        components_color = [0x640000]
        add(components_color, 0x006400)
        self.assertIn(0x006400, components_color)
        self.assertEqual(2, len(components_color))

    def test_add_to_max(self):
        components_color = [0x640000]*MAX_COLOR
        add(components_color, 0x006400)
        self.assertNotIn(0x006400, components_color)
        self.assertEqual(MAX_COLOR, len(components_color))

    def test_add_existing(self):
        components_color = [0x640000]
        add(components_color, 0x640000)
        self.assertEqual(1, len(components_color))
        self.assertIn(0x640000, components_color)

    def test_remove_existing_solo(self):
        components_color = [0x640000]
        remove(components_color, 0x640000)
        self.assertEqual(0, len(components_color))
        self.assertNotIn(0x640000, components_color)

    def test_remove_existing_multi(self):
        components_color = [0x640000, 0x000064, 0x640000]
        remove(components_color, 0x640000)
        self.assertEqual(2, len(components_color))
        self.assertIn(0x640000, components_color)

    def test_remove_unexisting(self):
        components_color = [0x640000, 0x000064]
        remove(components_color, 0x006400)
        self.assertEqual(2, len(components_color))
        self.assertIn(0x000064, components_color)
        self.assertIn(0x640000, components_color)
