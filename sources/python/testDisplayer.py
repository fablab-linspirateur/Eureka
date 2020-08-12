import unittest
import a_displayer as displayer

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dspl = displayer.displayer("testConfiguration.yaml")

    def test_creation(self):
        test_cfg = {'ilot':"/Fablab", 'chariot':"/Demo", 'broker':"192.168.1.2"}
        config = self.dspl.get_components("testConfiguration.yaml")
        self.assertEqual(config,test_cfg)

    def test_componants(self):
        test_components = {'1': '0,9', '2': '10, 19', '3': '20, 29'}
        config = self.dspl.get_components("testComponents.txt")
        self.assertEqual(config,test_components)


if __name__ == '__main__':
    unittest.main()
