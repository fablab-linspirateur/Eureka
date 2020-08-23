import unittest
from sources.ESP8266.displayer import displayer


class displayer_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions de la classe displayer."""

    def setUp(self):
        self.COMPONENTS_EMPTY = "./Tests/components_empty.txt"
        self.COMPONENTS_ONE = "./Tests/components_one.txt"
        self.COMPONENTS_TWO = "./Tests/components_two.txt"
        self.COMPONENTS_FIFTEEN = "./Tests/components_fifteen.txt"
        self.COMPONENT_ONE_ID = "123"
        self.COMPONENT_TWO_ID = "456"
        self.CONFIG_EMPTY = "./Tests/config_empty.yaml"
        self.CONFIG_TOTO = "./Tests/config_toto.yaml"

    def test_init_no_arg(self):
        import os
        path_bckp = os.getcwd()
        os.chdir("./Tests")
        disp = displayer()
        os.chdir(path_bckp)
        self.assertEqual((0, 0, 0), disp.LED_OFF)
        self.assertEqual(0x000000, disp.COLOR_BLACK)
        self.assertEqual(4, disp.MAX_COLOR)
        self.assertEqual("end", disp.TOPIC_END)
        self.assertEqual("search", disp.TOPIC_SEARCH_BASE)
        self.assertEqual("error", disp.TOPIC_ERROR_BASE)
        self.assertEqual(0, disp.NB_LEDS)
        self.assertEqual(1, len(disp.displayed))
        self.assertEqual({"1": []}, disp.displayed)
        res_config = {
            "network": "demo-network",
            "password": "demo-password",
            "name": "demo-name",
            "broker": "demo-broker"
        }
        self.assertEqual(res_config, disp.config)

    def test_init_arg_nb_leds(self):
        import os
        path_bckp = os.getcwd()
        os.chdir("./Tests")
        nb = 10
        disp = displayer(nb_leds=nb)
        os.chdir(path_bckp)
        self.assertEqual(nb, disp.NB_LEDS)

    def test_init_arg_components_file(self):
        disp = displayer(components_file=self.COMPONENTS_ONE,
                         config_file=self.CONFIG_TOTO)
        self.assertEqual(1, len(disp.displayed))
        self.assertEqual({self.COMPONENT_ONE_ID: []}, disp.displayed)

    def test_init_arg_config_file(self):
        disp = displayer(components_file=self.COMPONENTS_ONE,
                         config_file=self.CONFIG_TOTO)
        result = {
            "network": "tata",
            "password": "titi",
            "name": "toto",
            "broker": "tutu"
        }
        self.assertEqual(result, disp.config)

    def test_explode_topic_base_and_info(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        etopic = disp.explode_topic("search/1")
        self.assertEqual("search", etopic["base"])
        self.assertEqual("1", etopic["info"])

    def test_explode_topic_base_without_info(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        etopic = disp.explode_topic("end")
        self.assertEqual("end", etopic["base"])
        self.assertEqual("", etopic["info"])

    def test_explode_topic_base_with_complex_info(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        etopic = disp.explode_topic("search/1/2")
        self.assertEqual("search", etopic["base"])
        self.assertEqual("1/2", etopic["info"])

    def test_to_color_off(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        color = disp.to_color(0x000000)
        self.assertEqual((0, 0, 0), color)

    def test_to_color_white_half(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        color = disp.to_color(0x7f7f7f)
        self.assertEqual((127, 127, 127), color)

    def test_to_color_red_full(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        color = disp.to_color(0xff0000)
        self.assertEqual((255, 0, 0), color)

    def test_to_color_green_hundred(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        color = disp.to_color(0x006400)
        self.assertEqual((0, 100, 0), color)

    def test_get_components_file_empty(self):
        disp = displayer(
            nb_leds=0, components_file=self.COMPONENTS_EMPTY, config_file=self.CONFIG_TOTO)
        self.assertEqual(disp.displayed, {})

    def test_get_components_file_one(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        self.assertEqual({self.COMPONENT_ONE_ID: []}, disp.displayed)

    def test_get_components_file_fifteen(self):
        disp = displayer(
            nb_leds=150, components_file=self.COMPONENTS_FIFTEEN, config_file=self.CONFIG_TOTO)
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
        self.assertEqual(result, disp.displayed)

    def test_get_config_empty(self):
        disp = displayer(config_file=self.CONFIG_EMPTY,
                         components_file=self.COMPONENTS_ONE)
        self.assertEqual({}, disp.config)

    def test_get_config_toto(self):
        disp = displayer(config_file=self.CONFIG_TOTO,
                         components_file=self.COMPONENTS_ONE)
        result = {
            "network": "tata",
            "password": "titi",
            "name": "toto",
            "broker": "tutu"
        }
        self.assertEqual(result, disp.config)

    def test_add_to_empty(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x640000)
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_to_one(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x006400)
        self.assertIn(0x006400, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_add_to_four(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
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
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.add(disp.displayed[self.COMPONENT_ONE_ID], 0x640000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_existing_solo(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x640000)
        self.assertEqual(0, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_existing_multi(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x006400,
            0x000064,
            0x640000
        ]
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_remove_unexisting(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x000064,
            0x640000
        ]
        disp.remove(disp.displayed[self.COMPONENT_ONE_ID], 0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x000064, disp.displayed[self.COMPONENT_ONE_ID])
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_in_empty(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        self.assertEqual(1, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_in_filled(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertIn(0x006400, disp.displayed[self.COMPONENT_ONE_ID])

    def test_display_component_unexisting(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component("unexisting", 0x006400)
        self.assertIn(self.COMPONENT_ONE_ID, disp.displayed)
        self.assertEqual(0, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn("unexisting", disp.displayed)

    def test_turn_off_if_present(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x640000
        ]
        disp.turn_off(0x640000)
        self.assertEqual(0, len(disp.displayed[self.COMPONENT_ONE_ID]))
        self.assertNotIn(0x640000, disp.displayed[self.COMPONENT_ONE_ID])

    def test_turn_off_if_absent(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.displayed[self.COMPONENT_ONE_ID] = [
            0x000000,
            0x640000
        ]
        disp.turn_off(0x006400)
        self.assertEqual(2, len(disp.displayed[self.COMPONENT_ONE_ID]))

    def test_to_neopixel_empty(self):
        disp = displayer(
            nb_leds=0, components_file=self.COMPONENTS_EMPTY, config_file=self.CONFIG_TOTO)
        expected = []
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_no_color(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_one_color(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_two_color(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_three_color(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        disp.display_component(self.COMPONENT_ONE_ID, 0x000064)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 100), (0, 0, 100), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_one_four_color(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        disp.display_component(self.COMPONENT_ONE_ID, 0x000064)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006464)
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 100, 0), (0, 100, 0),
                    (0, 0, 100), (0, 0, 100), (0, 100, 100), (0, 100, 100), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_to_neopixel_two_no_color(self):
        disp = displayer(
            nb_leds=20, components_file=self.COMPONENTS_TWO, config_file=self.CONFIG_TOTO)
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_one_component_one_color(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        result = disp.refresh(bytes(disp.TOPIC_END, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_one_component_two_colors(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        disp.display_component(self.COMPONENT_ONE_ID, 0x640000)
        disp.display_component(self.COMPONENT_ONE_ID, 0x006400)
        result = disp.refresh(bytes(disp.TOPIC_END, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 100, 0), (0, 100, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_end_two_components_one_color(self):
        disp = displayer(
            nb_leds=20, components_file=self.COMPONENTS_TWO, config_file=self.CONFIG_TOTO)
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
        disp = displayer(
            nb_leds=20, components_file=self.COMPONENTS_TWO, config_file=self.CONFIG_TOTO)
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
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        result = disp.refresh(bytes(disp.TOPIC_SEARCH_BASE + "/" + self.COMPONENT_ONE_ID, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (100, 0, 0), (100, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_refresh_search_unexisting(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        result = disp.refresh(bytes(disp.TOPIC_SEARCH_BASE + "/" + self.COMPONENT_TWO_ID, "utf-8"),
                              bytes(str(0x640000), "utf-8"))
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.to_neopixel()
        self.assertEqual(expected, result)

    def test_all_no_param(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        expected = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        result = disp.all()
        self.assertEqual(expected, result)

    def test_all_green_10_leds_1_component(self):
        disp = displayer(
            nb_leds=10, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        expected = [(0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0),
                    (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0)]
        result = disp.all(0x006400)
        self.assertEqual(expected, result)

    def test_all_green_20_leds_1_component(self):
        disp = displayer(
            nb_leds=20, components_file=self.COMPONENTS_ONE, config_file=self.CONFIG_TOTO)
        expected = [(0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0),
                    (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0),
                    (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0),
                    (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0), (0, 100, 0)]
        result = disp.all(0x006400)
        self.assertEqual(expected, result)
