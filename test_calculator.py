"""Unit tests for add and subtract in calculator.py."""

import unittest

from calculator import add, subtract


class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)

    def test_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


class TestSubtract(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_negative_result(self):
        self.assertEqual(subtract(4, 10), -6)

    def test_floats(self):
        self.assertAlmostEqual(subtract(0.3, 0.1), 0.2)


if __name__ == "__main__":
    unittest.main()
