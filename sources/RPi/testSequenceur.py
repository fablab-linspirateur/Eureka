import unittest
import sequenceur
import pandas as pd
import pandas.testing as pd_testing

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.df_totest = pd.DataFrame([[123, 1], [123, 2], [123, 3], [456, 4], [456, 5], [456, 6]], columns=["of", "id"])

    def test_idents(self):
        df = sequenceur.initialise_idents("testfile.csv")
        pd_testing.assert_frame_equal(df, self.df_totest)

    def test_scan_to_ident(self):
        self.assertEqual(sequenceur.Scan2Ident("43487459001000012300010000001000"), 123)

if __name__ == '__main__':
    unittest.main()
