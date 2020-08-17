import unittest
import pandas as pd
from sources.RPi.finder import finder


class finder_test(unittest.TestCase):
    """Test case utilisé pour tester les fonctions de la classe finder."""

    def setUp(self):
        self.COMPOUNDS_EMPTY = "./Tests/compounds_empty.csv"
        self.COMPOUNDS_EMPTY_WITH_HEADERS = "./Tests/compounds_empty_with_headers.csv"
        self.COMPOUNDS_ONE = "./Tests/compounds_one.csv"

    def test_init_no_arg(self):
        import os
        path_bckp = os.getcwd()
        os.chdir("./Tests")
        find = finder()
        os.chdir(path_bckp)
        self.assertEqual(pd.DataFrame, type(find.compounds))
        self.assertEqual(["compound", "component"],
                         list(find.compounds.columns))
        self.assertEqual(12, find.compounds.size)

    def test_init_arg_compounds_file_empty(self):
        find = finder(compounds_file=self.COMPOUNDS_EMPTY)
        self.assertEqual(pd.DataFrame, type(find.compounds))
        self.assertEqual(["compound", "component"],
                         list(find.compounds.columns))
        self.assertEqual(0, find.compounds.size)

    def test_init_arg_compounds_file_empty_with_headers(self):
        find = finder(compounds_file=self.COMPOUNDS_EMPTY_WITH_HEADERS)
        self.assertEqual(pd.DataFrame, type(find.compounds))
        self.assertEqual(["compound", "component"],
                         list(find.compounds.columns))
        self.assertEqual(0, find.compounds.size)

    def test_init_arg_compounds_file_one(self):
        find = finder(compounds_file=self.COMPOUNDS_ONE)
        self.assertEqual(pd.DataFrame, type(find.compounds))
        self.assertEqual(["compound", "component"],
                         list(find.compounds.columns))
        self.assertEqual(6, find.compounds.size)

    def test_explode_topic_base_and_info(self):
        find = finder(compounds_file=self.COMPOUNDS_ONE)
        etopic = find.explode_topic("search/1")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1")

    def test_explode_topic_base_without_info(self):
        find = finder(compounds_file=self.COMPOUNDS_ONE)
        etopic = find.explode_topic("end")
        self.assertEqual(etopic["base"], "end")
        self.assertEqual(etopic["info"], "")

    def test_explode_topic_base_with_complex_info(self):
        find = finder(compounds_file=self.COMPOUNDS_ONE)
        etopic = find.explode_topic("search/1/2")
        self.assertEqual(etopic["base"], "search")
        self.assertEqual(etopic["info"], "1/2")

    def test_search_components_compound_unexisting(self):
        find = finder(compounds_file=self.COMPOUNDS_ONE)
        result = find.search_components("2")
        self.assertEqual([], result)

    def test_search_components_compound_existing(self):
        find = finder(compounds_file=self.COMPOUNDS_ONE)
        result = find.search_components("1")
        self.assertEqual(["a", "b", "c"], result)
