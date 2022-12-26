from unittest import TestCase

from core.logic import operation


class LogicTestCase(TestCase):

    def test_plus(self):
        result = operation(9, 5, '+')
        self.assertEqual(14, result)

    def test_minus(self):
        result = operation(8, 3, '-')
        self.assertEqual(5, result)

    def test_multiply(self):
        result = operation(8, 3, '*')
        self.assertEqual(24, result)
