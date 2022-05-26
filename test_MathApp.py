import unittest
import MathApp
import sys


class TestMathApp(unittest.TestCase):
    def setUp(self):
        # testing PyQt applications doesn't work without this line of code
        qapp = MathApp.QApplication(sys.argv)
        self.app = MathApp.MathApp()

    def test_check_equation_mistakes(self):
        inputs_to_outputs = {
            "x^2+3x+4": "no 'y=' at beginning",
            "y=": "no expression after equal sign",
            "y=x-y": "y is not isolated on the left side",
            "y==": "multiple equal signs",
            "y=a^2+3a+4": "variables other than x and y in equation",
            "y=35%": "illegal characters in equation",
            "y=35*)": "improper syntax",
            "y=35)+5": "closing parenthesis with no matching open parenthesis",
            "y=(35+5": "unclosed parentheses",
            "y=x^2+3x+4": "equation is correct"
        }
        # input is a built-in function
        for input_, output in inputs_to_outputs.items():
            self.assertEqual(self.app.check_equation_mistakes(input_), output)

    def test_expand_expression(self):
        inputs_to_outputs = {
            "2x^2 - 8x + 6": (True, "2*x^2-8*x+6"),
            "-x+6": (True, "6-x"),
            "6 - 8x + 2x^2": (True, "2*x^2-8*x+6"),
        }
        # input is a built-in function
        for input_, output in inputs_to_outputs.items():
            self.assertEqual(self.app.expand_expression(input_), output)

    def test_is_quadratic(self):
        inputs_to_outputs = {
            "x^2 - 6x + 6": True,
            "x^1 + 3": True,
            "6-x": True,
            "3": True,
            "x^0": True,
            "x^3 + 3": False,
            "x^2 - 6x + 6 + x^4": False,
            "x^(-1) + x - 3": False,
            "x^0.5 + 3x + 3": False
        }
        # input is a built-in function
        for input_, output in inputs_to_outputs.items():
            self.assertEqual(self.app.is_quadratic(input_), output)

    def test_extract_coefficients_from_quadratic(self):
        inputs_to_outputs = {
            "3x^2+6x+3": (3, 6, 3),
            "x^2+6x+3": (1, 6, 3),
            "6x+3": (0, 6, 3),
            "3": (0, 0, 3),
            "0": (0, 0, 0),
            "x^2+6x": (1, 6, 0),
            "x^2+3": (1, 0, 3),
            "2x^2-8x+6": (2, -8, 6),
            "-x^2-2x-9": (-1, -2, -9),
            "-2x^2-x-1": (-2, -1, -1),
            "-3x^2": (-3, 0, 0),
            "-x^2": (-1, 0, 0)
        }
        # input is a built-in function
        for input_, output in inputs_to_outputs.items():
            self.assertEqual(self.app.extract_coefficients_from_quadratic(input_), output)

    def test_find_roots_of_quadratic(self):
        inputs_to_outputs = {
            (0, 0, 6): None,
            (0, 0, 0): "infinite",
            (0, -3, 6): 2,
            (2, -8, 6): (3, 1),
            (4, -12, 9): 1.5
        }
        # input is a built-in function
        for input_, output in inputs_to_outputs.items():
            self.assertEqual(self.app.find_roots_of_quadratic(*input_), output)


if __name__ == "__main__":
    unittest.main()
