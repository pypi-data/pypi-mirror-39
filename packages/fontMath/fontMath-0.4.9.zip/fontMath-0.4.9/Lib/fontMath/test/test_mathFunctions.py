import unittest
from fontMath.mathFunctions import (
    add, addPt, sub, subPt, mul, mulPt, div, divPt, factorAngle, _roundNumber
)


class MathFunctionsTest(unittest.TestCase):
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(3, -4), -1)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(6, 7), add(7, 6))

    def test_addPt(self):
        self.assertEqual(addPt((20, 230), (50, 40)), (70, 270))

    def test_sub(self):
        self.assertEqual(sub(10, 10), 0)
        self.assertEqual(sub(10, -10), 20)
        self.assertEqual(sub(-10, 10), -20)

    def test_subPt(self):
        self.assertEqual(subPt((20, 230), (50, 40)), (-30, 190))

    def test_mul(self):
        self.assertEqual(mul(1, 2), 2)
        self.assertEqual(mul(3, -4), -12)
        self.assertEqual(mul(10, 0), 0)
        self.assertEqual(mul(5, 6), mul(6, 5))

    def test_mulPt(self):
        self.assertEqual(mulPt((15, 25), (2, 3)), (30, 75))

    def test_div(self):
        self.assertEqual(div(1, 2), 0.5)
        with self.assertRaises(ZeroDivisionError):
            div(10, 0)
        self.assertEqual(div(12, -4), -3)

    def test_divPt(self):
        self.assertEqual(divPt((15, 75), (2, 3)), (7.5, 25.0))

    def test_factorAngle(self):
        f = factorAngle(5, (2, 1.5), mul)
        self.assertEqual(_roundNumber(f, 2), 3.75)

    def test_roundNumber(self):
        # round to integer:
        self.assertEqual(_roundNumber(0), 0)
        self.assertEqual(_roundNumber(0.1), 0)
        self.assertEqual(_roundNumber(0.99), 1)
        self.assertEqual(_roundNumber(0.499), 0)
        self.assertEqual(_roundNumber(0.5), 0)
        self.assertEqual(_roundNumber(-0.499), 0)
        self.assertEqual(_roundNumber(-0.5), 0)
        self.assertEqual(_roundNumber(1.5), 2)
        self.assertEqual(_roundNumber(-1.5), -2)

    def test_roundNumber_to_float(self):
        # round to float with specified decimals:
        self.assertEqual(_roundNumber(0.3333, None), 0)
        self.assertEqual(_roundNumber(0.3333, 0), 0.0)
        self.assertEqual(_roundNumber(0.3333, 1), 0.3)
        self.assertEqual(_roundNumber(0.3333, 2), 0.33)
        self.assertEqual(_roundNumber(0.3333, 3), 0.333)


if __name__ == "__main__":
    unittest.main()
