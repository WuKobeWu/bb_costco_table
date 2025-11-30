import os
import sys
import unittest

import pandas as pd


def add_git_root_to_path(start_path=None):
    if start_path is None:
        start_path = os.path.abspath(os.getcwd())
    current = start_path
    while True:
        if os.path.isdir(os.path.join(current, ".git")):
            if current not in sys.path:
                sys.path.append(current)
            return current

        parent = os.path.dirname(current)
        if parent == current:
            print("⚠️ .git root not found.")
            return None
        current = parent

add_git_root_to_path()
from src.convert import Convert


class TestConvert(unittest.TestCase):
    def setUp(self):
        input_path = 'test/data/input.xlsx'
        output_path = 'test/data/output.xlsx'
        self.convert_instance = Convert(input_path, output_path)
        self.SHEET_NAME = "D13"
        self.input, self.output = self.convert_instance._read(self.SHEET_NAME)
    def test_read_type(self):
        self.assertIsInstance(self.input, pd.DataFrame)
        self.assertIsInstance(self.output, pd.DataFrame)
    
    def test_read_columns(self):
        self.assertIn("Dept", self.input.columns)
        self.assertIn("Dept", self.output.columns)
    
    def test_read_shape(self):
        self.assertEqual(self.input.shape[0], 20)
        self.assertEqual(self.input.shape[1], 14)
        self.assertEqual(self.output.shape[0], 29)
        self.assertEqual(self.output.shape[1], 22)
    
    def


if __name__ == '__main__':
    unittest.main()
    