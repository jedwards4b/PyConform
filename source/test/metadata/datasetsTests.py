"""
Unit Tests for Dataset Metadata Objects

Copyright 2017-2018, University Corporation for Atmospheric Research
LICENSE: See the LICENSE.rst file for details
"""

import unittest

from pyconform.metadata.datasets import Dataset


class DatasetTests(unittest.TestCase):

    def setUp(self):
        self.ds = Dataset()

    def test_create(self):
        self.assertIsInstance(self.ds, Dataset)

    def test_default_dimensions_is_empty_tuple(self):
        self.assertEqual(self.ds.dimensions, ())

    def test_setting_dimensions_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.ds.dimensions = 3

    def test_default_variables_is_empty_tuple(self):
        self.assertEqual(self.ds.variables, ())

    def test_setting_variables_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.ds.variables = 3

    def test_default_files_is_empty_tuple(self):
        self.assertEqual(self.ds.files, ())

    def test_setting_files_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.ds.files = 3

    def test_new_dimension(self):
        d = self.ds.new_dimension('x')
        self.assertIn(d, self.ds)
        self.assertEqual(self.ds.dimensions, ('x',))

    def test_two_new_dimensions_with_same_name_raises_value_error(self):
        self.ds.new_dimension('x')
        with self.assertRaises(ValueError):
            self.ds.new_dimension('x')

    def test_new_dimension_sets_dimenion_dataset(self):
        d = self.ds.new_dimension('x')
        self.assertIs(d.dataset, self.ds)

    def test_new_variable(self):
        v = self.ds.new_variable('v')
        self.assertIn(v, self.ds)
        self.assertEqual(self.ds.variables, ('v',))

    def test_two_new_variables_with_same_name_raises_value_error(self):
        self.ds.new_variable('v')
        with self.assertRaises(ValueError):
            self.ds.new_variable('v')

    def test_new_variable_sets_variable_dataset(self):
        v = self.ds.new_dimension('v')
        self.assertIs(v.dataset, self.ds)

    def test_new_variable_without_dimensions_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.ds.new_variable('v', dimensions=('x',))

    def test_new_file(self):
        f = self.ds.new_file('test.nc')
        self.assertIn(f, self.ds)
        self.assertEqual(self.ds.files, ('test.nc',))

    def test_two_new_files_with_same_name_raises_value_error(self):
        self.ds.new_file('test.nc')
        with self.assertRaises(ValueError):
            self.ds.new_file('test.nc')

    def test_new_file_without_variables_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.ds.new_file('test.nc', variables=('v',))

    def test_new_file_sets_file_dataset(self):
        f = self.ds.new_file('test.nc')
        self.assertIs(f.dataset, self.ds)

    def test_get_dimension(self):
        x1 = self.ds.new_dimension('x', size=6)
        x2 = self.ds.get_dimension('x')
        self.assertIs(x1, x2)

    def test_get_dimension_not_found_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.ds.get_dimension('x')

    def test_get_variable(self):
        v1 = self.ds.new_variable('v')
        v2 = self.ds.get_variable('v')
        self.assertIs(v1, v2)

    def test_get_variable_not_found_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.ds.get_variable('v')

    def test_get_file(self):
        f1 = self.ds.new_file('test.nc')
        f2 = self.ds.get_file('test.nc')
        self.assertIs(f1, f2)

    def test_get_file_not_found_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.ds.get_file('test.nc')


if __name__ == '__main__':
    unittest.main()