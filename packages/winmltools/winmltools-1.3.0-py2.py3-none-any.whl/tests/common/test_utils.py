import unittest
import numpy as np
from winmltools.convert.common import utils


class TestCommonConvertUtils(unittest.TestCase):

    def test_is_string_type(self):
        self.assertEqual(utils.is_string_type('foo'), True)
        self.assertEqual(utils.is_string_type(1), False)

        self.assertEqual(utils.is_string_type(['foo', 'bar']), True)
        self.assertEqual(utils.is_string_type([1, 2]), False)

        self.assertEqual(utils.is_string_type(['foo', 1]), False)
        self.assertEqual(utils.is_string_type([1, 'foo']), False)

        self.assertEqual(utils.is_string_type(np.array(['foo', 'bar'])), True)
        self.assertEqual(utils.is_string_type(np.array([1, 2])), False)


    def test_is_numeric_type(self):
        self.assertEqual(utils.is_numeric_type('foo'), False)
        self.assertEqual(utils.is_numeric_type(1), True)

        self.assertEqual(utils.is_numeric_type(['foo', 'bar']), False)
        self.assertEqual(utils.is_numeric_type([1, 2]), True)

        self.assertEqual(utils.is_numeric_type(['foo', 1]), False)
        self.assertEqual(utils.is_numeric_type([1, 'foo']), False)

        self.assertEqual(utils.is_numeric_type(np.array(['foo', 'bar'])), False)
        self.assertEqual(utils.is_numeric_type(np.array([1, 2])), True)

