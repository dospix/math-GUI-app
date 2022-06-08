from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout, QLabel, QComboBox, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6 import uic
import sys
import sympy
import re
import traceback


class MathApp(QMainWindow):
    def __init__(self):
        super(MathApp, self).__init__()

        uic.loadUi("MathApp.ui", self)

        self.mainWindowGrid = self.findChild(QGridLayout, "mainWindowGridLayout")
        self.mathAppGrid = self.findChild(QGridLayout, "gridLayout")
        # these widgets will be hidden when the window changes
        self.displayed_widgets = []
        # these widgets will be destroyed when the window changes or when some buttons are pushed
        self.temporary_widgets = []

        self.currWindowLabel = self.findChild(QLabel, "currWindowLabel")
        self.nameOfCurrWindowLabel = self.findChild(QLabel, "nameOfCurrWindowLabel")
        self.algebraLabel = self.findChild(QLabel, "algebraLabel")
        self.algebraComboBox = self.findChild(QComboBox, "algebraComboBox")
        self.calculusLabel = self.findChild(QLabel, "calculusLabel")
        self.calculusComboBox = self.findChild(QComboBox, "calculusComboBox")
        self.probabilityAndCombinatoricsLabel = self.findChild(QLabel, "probabilityAndCombinatoricsLabel")
        self.probabilityAndCombinatoricsComboBox = self.findChild(QComboBox, "probabilityAndCombinatoricsComboBox")
        self.trigonometryLabel = self.findChild(QLabel, "trigonometryLabel")
        self.trigonometryComboBox = self.findChild(QComboBox, "trigonometryComboBox")

        self.main_font = QFont()
        self.main_font.setPointSize(11)

        self.disclaimer_font = QFont()
        self.disclaimer_font.setPointSize(10)
        self.disclaimer_font.setItalic(True)

        self.minimum_size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.create_algebra_widgets()
        self.create_calculus_widgets()

        self.show()

    def create_algebra_widgets(self):
        # Expression simplifier widgets
        self.expressionSimplifierEnterExpressionLabel = QLabel(self)
        self.expressionSimplifierEnterExpressionLabel.setText("Enter your expression here: (ex: (x+1)(x+3))")
        self.expressionSimplifierEnterExpressionLabel.setFont(self.main_font)
        self.expressionSimplifierEnterExpressionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.expressionSimplifierEnterExpressionLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.expressionSimplifierEnterExpressionLabel, 4, 1, 1, 3)
        # --------------------------------------------------
        self.expressionSimplifierExpressionInsertionLineEdit = QLineEdit(self)
        self.expressionSimplifierExpressionInsertionLineEdit.setFont(self.main_font)
        self.expressionSimplifierExpressionInsertionLineEdit.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.expressionSimplifierExpressionInsertionLineEdit, 5, 1, 1, 3)
        # --------------------------------------------------
        self.expressionSimplifierSimplifyExpressionButton = QPushButton(self)
        self.expressionSimplifierSimplifyExpressionButton.setText("Simplify expression")
        self.expressionSimplifierSimplifyExpressionButton.setSizePolicy(self.minimum_size_policy)
        self.expressionSimplifierSimplifyExpressionButton.clicked.connect(self.simplify_expression)
        self.mathAppGrid.addWidget(self.expressionSimplifierSimplifyExpressionButton, 7, 1, 1, 3)
        # --------------------------------------------------
        self.expression_simplifier_widgets = [self.expressionSimplifierEnterExpressionLabel,
                                              self.expressionSimplifierExpressionInsertionLineEdit,
                                              self.expressionSimplifierSimplifyExpressionButton]
        for widget in self.expression_simplifier_widgets:
            widget.hide()

        # Polynomial roots calculator widgets
        self.polynomialRootsEnterEquationLabel = QLabel(self)
        self.polynomialRootsEnterEquationLabel.setText("Enter your polynomial equation here: (ex: y = 2x^2 - 8x + 6)")
        self.polynomialRootsEnterEquationLabel.setFont(self.main_font)
        self.polynomialRootsEnterEquationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.polynomialRootsEnterEquationLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.polynomialRootsEnterEquationLabel, 4, 1, 1, 3)
        # --------------------------------------------------
        self.polynomialRootsEquationInsertionLineEdit = QLineEdit(self)
        self.polynomialRootsEquationInsertionLineEdit.setFont(self.main_font)
        self.polynomialRootsEquationInsertionLineEdit.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.polynomialRootsEquationInsertionLineEdit, 5, 1, 1, 3)
        # --------------------------------------------------
        self.polynomialRootsDisclaimerLabel = QLabel(self)
        self.polynomialRootsDisclaimerLabel.setText("*It can only solve quadratic or lower degree equations")
        self.polynomialRootsDisclaimerLabel.setFont(self.disclaimer_font)
        self.polynomialRootsDisclaimerLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.polynomialRootsDisclaimerLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.polynomialRootsDisclaimerLabel, 6, 1, 1, 3)
        # --------------------------------------------------
        self.polynomialRootsCalculateRootsButton = QPushButton(self)
        self.polynomialRootsCalculateRootsButton.setText("Calculate roots")
        self.polynomialRootsCalculateRootsButton.setSizePolicy(self.minimum_size_policy)
        self.polynomialRootsCalculateRootsButton.clicked.connect(self.calculate_roots_for_polynomial)
        self.mathAppGrid.addWidget(self.polynomialRootsCalculateRootsButton, 7, 1, 1, 3)
        # --------------------------------------------------
        self.polynomial_roots_calculator_widgets = [self.polynomialRootsEnterEquationLabel,
                                                    self.polynomialRootsEquationInsertionLineEdit,
                                                    self.polynomialRootsDisclaimerLabel,
                                                    self.polynomialRootsCalculateRootsButton]
        for widget in self.polynomial_roots_calculator_widgets:
            widget.hide()

        self.algebraComboBox.activated.connect(lambda: self.draw_window(self.algebraComboBox.currentText()))

    def create_calculus_widgets(self):
        # Derivative calculator widgets
        self.derivativeCalculatorEnterExpressionLabel = QLabel(self)
        self.derivativeCalculatorEnterExpressionLabel.setText("Enter your expression here: (ex: sin(x))")
        self.derivativeCalculatorEnterExpressionLabel.setFont(self.main_font)
        self.derivativeCalculatorEnterExpressionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.derivativeCalculatorEnterExpressionLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.derivativeCalculatorEnterExpressionLabel, 3, 1, 1, 3)
        # --------------------------------------------------
        self.derivativeCalculatorExpressionInsertionLineEdit = QLineEdit(self)
        self.derivativeCalculatorExpressionInsertionLineEdit.setFont(self.main_font)
        self.derivativeCalculatorExpressionInsertionLineEdit.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.derivativeCalculatorExpressionInsertionLineEdit, 4, 1, 1, 3)
        # --------------------------------------------------
        self.derivativeCalculatorEnterVariableLabel = QLabel(self)
        self.derivativeCalculatorEnterVariableLabel.setText("Enter the variable you're taking the derivative with "
                                                            "respect to here: (ex: x)")
        self.derivativeCalculatorEnterVariableLabel.setFont(self.main_font)
        self.derivativeCalculatorEnterVariableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.derivativeCalculatorEnterVariableLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.derivativeCalculatorEnterVariableLabel, 5, 1, 1, 3)
        # --------------------------------------------------
        self.derivativeCalculatorVariableInsertionLineEdit = QLineEdit(self)
        self.derivativeCalculatorVariableInsertionLineEdit.setFont(self.main_font)
        self.derivativeCalculatorVariableInsertionLineEdit.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.derivativeCalculatorVariableInsertionLineEdit, 6, 2, 1, 1)
        # --------------------------------------------------
        self.derivativeCalculatorCalculateDerivativeButton = QPushButton(self)
        self.derivativeCalculatorCalculateDerivativeButton.setText("Calculate derivative")
        self.derivativeCalculatorCalculateDerivativeButton.setSizePolicy(self.minimum_size_policy)
        self.derivativeCalculatorCalculateDerivativeButton.clicked.connect(self.calculate_derivative)
        self.mathAppGrid.addWidget(self.derivativeCalculatorCalculateDerivativeButton, 8, 1, 1, 3)
        # --------------------------------------------------
        self.derivative_calculator_widgets = [self.derivativeCalculatorEnterExpressionLabel,
                                              self.derivativeCalculatorExpressionInsertionLineEdit,
                                              self.derivativeCalculatorEnterVariableLabel,
                                              self.derivativeCalculatorVariableInsertionLineEdit,
                                              self.derivativeCalculatorCalculateDerivativeButton]
        for widget in self.derivative_calculator_widgets:
            widget.hide()

        # Integral calculator widgets
        self.integralCalculatorEnterExpressionLabel = QLabel(self)
        self.integralCalculatorEnterExpressionLabel.setText("Enter your expression here: (ex: cos(x))")
        self.integralCalculatorEnterExpressionLabel.setFont(self.main_font)
        self.integralCalculatorEnterExpressionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.integralCalculatorEnterExpressionLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.integralCalculatorEnterExpressionLabel, 3, 1, 1, 3)
        # --------------------------------------------------
        self.integralCalculatorExpressionInsertionLineEdit = QLineEdit(self)
        self.integralCalculatorExpressionInsertionLineEdit.setFont(self.main_font)
        self.integralCalculatorExpressionInsertionLineEdit.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.integralCalculatorExpressionInsertionLineEdit, 4, 1, 1, 3)
        # --------------------------------------------------
        self.integralCalculatorEnterVariableLabel = QLabel(self)
        self.integralCalculatorEnterVariableLabel.setText("Enter the variable you're taking the integral with respect "
                                                          "to here: (ex: x)")
        self.integralCalculatorEnterVariableLabel.setFont(self.main_font)
        self.integralCalculatorEnterVariableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.integralCalculatorEnterVariableLabel.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.integralCalculatorEnterVariableLabel, 5, 1, 1, 3)
        # --------------------------------------------------
        self.integralCalculatorVariableInsertionLineEdit = QLineEdit(self)
        self.integralCalculatorVariableInsertionLineEdit.setFont(self.main_font)
        self.integralCalculatorVariableInsertionLineEdit.setSizePolicy(self.minimum_size_policy)
        self.mathAppGrid.addWidget(self.integralCalculatorVariableInsertionLineEdit, 6, 2, 1, 1)
        # --------------------------------------------------
        self.integralCalculatorCalculateIntegralButton = QPushButton(self)
        self.integralCalculatorCalculateIntegralButton.setText("Calculate integral")
        self.integralCalculatorCalculateIntegralButton.setSizePolicy(self.minimum_size_policy)
        self.integralCalculatorCalculateIntegralButton.clicked.connect(self.calculate_integral)
        self.mathAppGrid.addWidget(self.integralCalculatorCalculateIntegralButton, 8, 1, 1, 3)
        # --------------------------------------------------
        self.integral_calculator_widgets = [self.integralCalculatorEnterExpressionLabel,
                                            self.integralCalculatorExpressionInsertionLineEdit,
                                            self.integralCalculatorEnterVariableLabel,
                                            self.integralCalculatorVariableInsertionLineEdit,
                                            self.integralCalculatorCalculateIntegralButton]
        for widget in self.integral_calculator_widgets:
            widget.hide()

        self.calculusComboBox.activated.connect(lambda: self.draw_window(self.calculusComboBox.currentText()))

    def clear_window(self):
        for widget in self.displayed_widgets:
            widget.hide()
        for widget in self.temporary_widgets:
            self.mathAppGrid.removeWidget(widget)
            widget.deleteLater()

        self.displayed_widgets = []
        self.temporary_widgets = []

    def clear_temporary_widgets(self):
        for widget in self.temporary_widgets:
            self.mathAppGrid.removeWidget(widget)
            widget.deleteLater()

        self.temporary_widgets = []

    def draw_window(self, window_name):
        self.clear_window()

        if window_name == "Polynomial roots calculator":
            self.nameOfCurrWindowLabel.setText("Polynomial roots calculator")

            for widget in self.polynomial_roots_calculator_widgets:
                self.displayed_widgets.append(widget)
                widget.show()

        elif window_name == "Expression simplifier":
            self.nameOfCurrWindowLabel.setText("Expression simplifier")

            for widget in self.expression_simplifier_widgets:
                self.displayed_widgets.append(widget)
                widget.show()

        elif window_name == "Derivative calculator":
            self.nameOfCurrWindowLabel.setText("Derivative calculator")

            for widget in self.derivative_calculator_widgets:
                self.displayed_widgets.append(widget)
                widget.show()

        elif window_name == "Integral calculator":
            self.nameOfCurrWindowLabel.setText("Integral calculator")

            for widget in self.integral_calculator_widgets:
                self.displayed_widgets.append(widget)
                widget.show()

    def simplify_expression(self):
        self.clear_temporary_widgets()

        expression = self.expressionSimplifierExpressionInsertionLineEdit.text()
        expression = expression.replace(" ", "")

        # This label will only be displayed if there is a warning
        warning_label = QLabel(self)
        warning_label.setStyleSheet("color: red;")
        warning_label.setFont(self.main_font)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(warning_label)

        warning = self.check_expression_mistakes(expression, non_x_or_y_variables=False, non_x_variables=True,
                                                 illegal_characters=True, improper_syntax=True,
                                                 incorrectly_placed_parentheses=True)
        if not warning == "expression is correct":
            if warning == "variables other than x in expression":
                warning_label.setText("Please only use lowercase x as the variable in your expression")
            elif warning == "illegal characters in expression":
                warning_label.setText("Illegal characters used. Please only use x, numbers with/without decimals, "
                                      "parentheses and the +, -, *, /, ^ operators")
            elif warning == "improper syntax":
                warning_label.setText("Improper syntax. Please check that you've written your expression correctly")
            elif warning == "closing parenthesis with no matching open parenthesis":
                warning_label.setText("You've used a closing parenthesis that doesn't have a matching open parenthesis")
            elif warning == "unclosed parentheses":
                warning_label.setText("You have unclosed parentheses")

            # the 'illegal characters in equation' warning is too big to fit 3 columns
            if warning != "illegal characters in expression":
                self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            else:
                self.mathAppGrid.addWidget(warning_label, 9, 0, 1, 5)

            return

        successful_expansion, expression = self.expand_expression(expression)

        if not successful_expansion:
            warning_label.setText("The expression could not be expanded")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return

        successful_simplification, expression = self.sympy_simplify_expression(expression)

        if not successful_simplification:
            warning_label.setText("The expression could not be simplified")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return

        simplified_equation_label = QLabel(self)
        simplified_equation_label.setText("The expression was simplified to: " + str(expression))
        simplified_equation_label.setFont(self.main_font)
        simplified_equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        simplified_equation_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(simplified_equation_label)
        self.mathAppGrid.addWidget(simplified_equation_label, 9, 1, 1, 3)

    def calculate_roots_for_polynomial(self):
        self.clear_temporary_widgets()

        equation = self.polynomialRootsEquationInsertionLineEdit.text()
        equation = equation.replace(" ", "")

        # This label will only be displayed if there is a warning
        warning_label = QLabel(self)
        warning_label.setStyleSheet("color: red;")
        warning_label.setFont(self.main_font)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(warning_label)

        warning = self.check_expression_mistakes(equation, is_equation=True, y_not_isolated=True,
                                                 non_x_or_y_variables=True, non_x_variables=False,
                                                 illegal_characters=True, improper_syntax=True,
                                                 incorrectly_placed_parentheses=True)
        if not warning == "equation is correct":
            if warning == "no 'y=' at beginning":
                warning_label.setText("Please enter equations in the form 'y=...'")
            elif warning == "no expression after equal sign":
                warning_label.setText("Please enter an expression to the right of the equal sign")
            elif warning == "y is not isolated on the left side":
                warning_label.setText("Please isolate the y variable on the left side of the equation")
            elif warning == "multiple equal signs":
                warning_label.setText("There are multiple equal signs in your equation")
            elif warning == "variables other than x and y in equation":
                warning_label.setText("Please only use lowercase x and y as variables in your equation, "
                                      "where x is the independent variable")
            elif warning == "illegal characters in equation":
                warning_label.setText("Illegal characters used. Please only use x, y, numbers with/without decimals, "
                                      "the equal sign, parentheses and the +, -, *, /, ^ operators")
            elif warning == "improper syntax":
                warning_label.setText("Improper syntax. Please check that you've written your equation correctly")
            elif warning == "closing parenthesis with no matching open parenthesis":
                warning_label.setText("You've used a closing parenthesis that doesn't have a matching open parenthesis")
            elif warning == "unclosed parentheses":
                warning_label.setText("You have unclosed parentheses")

            # the 'illegal characters in equation' warning is too big to fit 3 columns
            if warning != "illegal characters in equation":
                self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            else:
                self.mathAppGrid.addWidget(warning_label, 9, 0, 1, 5)

            return

        successful_expansion, expression = self.expand_expression(equation[2:])

        if not successful_expansion:
            warning_label.setText("The expression could not be expanded")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return

        expanded_equation_label = QLabel(self)
        expanded_equation_label.setText("The equation was expanded to: y=" + str(expression))
        expanded_equation_label.setFont(self.main_font)
        expanded_equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        expanded_equation_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(expanded_equation_label)
        self.mathAppGrid.addWidget(expanded_equation_label, 9, 1, 1, 3)

        if not self.is_quadratic(expression):
            warning_label.setText("This polynomial is not quadratic")
            self.mathAppGrid.addWidget(warning_label, 10, 1, 1, 3)
            return

        x_squared_coeff, x_coeff, constant_coeff = self.extract_coefficients_from_quadratic(expression)

        result = self.find_roots_of_quadratic(x_squared_coeff, x_coeff, constant_coeff)

        result_label = QLabel(self)
        if result is None:
            result_label.setText("This equation has no solutions!")
            result_label.setStyleSheet("color: red;")
        elif result == "infinite":
            result_label.setText("There are an infinite amount of roots!")
        elif x_squared_coeff == 0:
            result_label.setText("The root for this linear equation is x=" + str(result))
        elif not hasattr(result, '__iter__'):
            result_label.setText("This quadratic equation only has 1 root, which is x=" + str(result))
        else:
            result_label.setText("The roots for this quadratic equation are x1=" + str(result[0]) +
                                 " and x2=" + str(result[1]))
        result_label.setFont(self.main_font)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(result_label)
        self.mathAppGrid.addWidget(result_label, 10, 1, 1, 3)

    def calculate_derivative(self):
        self.clear_temporary_widgets()

        expression = self.derivativeCalculatorExpressionInsertionLineEdit.text()
        expression = expression.replace(" ", "")
        expression = self.add_multiplication_signs(expression, has_trigonometric_functions=True)

        # This label will only be displayed if there is a warning
        warning_label = QLabel(self)
        warning_label.setStyleSheet("color: red;")
        warning_label.setFont(self.main_font)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(warning_label)

        warning = self.check_expression_mistakes(expression, is_equation=False, y_not_isolated=False,
                                                 non_x_or_y_variables=False, non_x_variables=False,
                                                 illegal_characters=True, improper_syntax=True,
                                                 incorrectly_placed_parentheses=True)

        if not warning == "expression is correct":
            if warning == "illegal characters in expression":
                warning_label.setText("Illegal characters used. Please only use letters, numbers with/without decimals,"
                                      " parentheses and the +, -, *, /, ^ operators")
            elif warning == "improper syntax":
                warning_label.setText("Improper syntax. Please check that you've written your expression correctly")
            elif warning == "closing parenthesis with no matching open parenthesis":
                warning_label.setText("You've used a closing parenthesis that doesn't have a matching open parenthesis")
            elif warning == "unclosed parentheses":
                warning_label.setText("You have unclosed parentheses")

            # the 'illegal characters in equation' warning is too big to fit 3 columns
            if warning != "illegal characters in expression":
                self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            else:
                self.mathAppGrid.addWidget(warning_label, 9, 0, 1, 5)

            return

        variable = self.derivativeCalculatorVariableInsertionLineEdit.text().replace(" ", "")

        if len(variable) != 1:
            warning_label.setText("Please enter one variable")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return
        if not variable.isalpha():
            warning_label.setText("The variable has to be a letter")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return

        expression = expression.replace("^", "**")
        derivative = sympy.diff(expression, variable)
        derivative = str(derivative)
        derivative = derivative.replace("**", "^")

        result_label = QLabel(self)
        result_label.setText("The derivative of the equation above is: " + derivative)
        result_label.setFont(self.main_font)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(result_label)
        self.mathAppGrid.addWidget(result_label, 10, 1, 1, 3)

    def calculate_integral(self):
        self.clear_temporary_widgets()

        expression = self.integralCalculatorExpressionInsertionLineEdit.text()
        expression = expression.replace(" ", "")
        expression = self.add_multiplication_signs(expression, has_trigonometric_functions=True)

        # This label will only be displayed if there is a warning
        warning_label = QLabel(self)
        warning_label.setStyleSheet("color: red;")
        warning_label.setFont(self.main_font)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(warning_label)

        warning = self.check_expression_mistakes(expression, is_equation=False, y_not_isolated=False,
                                                 non_x_or_y_variables=False, non_x_variables=False,
                                                 illegal_characters=True, improper_syntax=True,
                                                 incorrectly_placed_parentheses=True)

        if not warning == "expression is correct":
            if warning == "illegal characters in expression":
                warning_label.setText("Illegal characters used. Please only use letters, numbers with/without decimals,"
                                      " parentheses and the +, -, *, /, ^ operators")
            elif warning == "improper syntax":
                warning_label.setText("Improper syntax. Please check that you've written your expression correctly")
            elif warning == "closing parenthesis with no matching open parenthesis":
                warning_label.setText("You've used a closing parenthesis that doesn't have a matching open parenthesis")
            elif warning == "unclosed parentheses":
                warning_label.setText("You have unclosed parentheses")

            # the 'illegal characters in equation' warning is too big to fit 3 columns
            if warning != "illegal characters in expression":
                self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            else:
                self.mathAppGrid.addWidget(warning_label, 9, 0, 1, 5)

            return

        variable = self.integralCalculatorVariableInsertionLineEdit.text().replace(" ", "")

        if len(variable) != 1:
            warning_label.setText("Please enter one variable")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return
        if not variable.isalpha():
            warning_label.setText("The variable has to be a letter")
            self.mathAppGrid.addWidget(warning_label, 9, 1, 1, 3)
            return

        expression = expression.replace("^", "**")
        x = sympy.Symbol(variable)
        try:
            integral = sympy.integrate(expression, x)
        except Exception:
            print(traceback.format_exc())
        integral = str(integral)
        integral = integral.replace("**", "^")

        result_label = QLabel(self)
        result_label.setText("The integral of the equation above is: " + integral + " + C")
        result_label.setFont(self.main_font)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setSizePolicy(self.minimum_size_policy)
        self.temporary_widgets.append(result_label)
        self.mathAppGrid.addWidget(result_label, 10, 1, 1, 3)

    @staticmethod
    def check_expression_mistakes(expression, is_equation=False, y_not_isolated=False, non_x_or_y_variables=False,
                                  non_x_variables=False, illegal_characters=False, improper_syntax=False,
                                  incorrectly_placed_parentheses=False,):
        """Checks if the expression/equation given has any mistakes and returns said mistake, otherwise it returns
        that it is correct. When calling the method it can be specified through its keyword arguments what constitutes
        as a mistake.
        Cases:
        *is_equation=True:
            'x^2+3x+4' -> 'no 'y=' at beginning'
            'y=' -> 'no expression after equal sign'
            *y_not_isolated=True:
                'y=x-y' -> 'y is not isolated on the left side'
            'y==' -> 'multiple equal signs'
            *non_x_or_y_variables=True:
                'y=a^2+3a+4' -> 'variables other than x and y in equation'
            *illegal_characters=True:
                'y=35%' -> 'illegal characters in equation'
            *improper_syntax=True:
                'y=35*)' -> 'improper syntax'
            *incorrectly_placed_parentheses=True:
                'y=35)+5' -> 'closing parenthesis with no matching open parenthesis'
                'y=(35+5' -> 'unclosed parentheses'

            No mistakes:
                'y=x^2+3x+4' -> 'equation is correct'

        *is_equation=False:
            *non_x_or_y_variables=True:
                'a^2+3a+4' -> 'variables other than x and y in expression'
            *non_x_variables=True:
                'a^2+3a+4' -> 'variables other than x in expression'
            *illegal_characters=True:
                '35%' -> 'illegal characters in expression'
            *improper_syntax=True:
                '35*)' -> 'improper syntax'
            *incorrectly_placed_parentheses=True:
                '35)+5' -> 'closing parenthesis with no matching open parenthesis'
                '(35+5' -> 'unclosed parentheses'

            No mistakes:
                'x^2+3x+4' -> 'expression is correct'"""

        if is_equation:
            equation = expression

            if equation[:2] != "y=":
                return "no 'y=' at beginning"

            if len(equation) == 2:
                return "no expression after equal sign"

            if y_not_isolated:
                if "y" in equation[2:]:
                    return "y is not isolated on the left side"

            if equation.count("=") > 1:
                return "multiple equal signs"

            if non_x_or_y_variables:
                for char in equation:
                    if char.isalpha() and char not in ["x", "y"]:
                        return "variables other than x and y in equation"

            if illegal_characters:
                for char in equation:
                    if char not in "xy0123456789.=()+-*/^":
                        return "illegal characters in equation"

        elif not is_equation:
            if non_x_or_y_variables:
                for char in expression:
                    if char.isalpha() and char not in "xy":
                        return "variables other than x and y in expression"

            if non_x_variables:
                for char in expression:
                    if char.isalpha() and char != "x":
                        return "variables other than x in expression"

            if illegal_characters:
                for char in expression:
                    if not char.isalpha() and char not in "0123456789.()+-*/^":
                        return "illegal characters in expression"

        if improper_syntax:
            improper_syntax_in_expression = False
            length_of_expression = len(expression)
            if not non_x_variables and not non_x_or_y_variables:
                variables_in_equation = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif non_x_or_y_variables:
                variables_in_equation = "xy"
            elif non_x_variables:
                variables_in_equation = "x"
            for i, char in enumerate(expression):
                if i < length_of_expression - 1:
                    if char in "+-*/^" and not (expression[i + 1].isdigit() or expression[i + 1] in "(+-" + variables_in_equation):
                        improper_syntax_in_expression = True
                        break
                    if char == "(" and not (expression[i + 1].isdigit() or expression[i + 1] in "(+-" + variables_in_equation):
                        improper_syntax_in_expression = True
                        break
                    if char in variables_in_equation and expression[i + 1] == ".":
                        improper_syntax_in_expression = True
                        break
                    if char == "." and not expression[i + 1].isdigit():
                        improper_syntax_in_expression = True
                        break

            if expression[length_of_expression - 1] in "+-*/^.":
                improper_syntax_in_expression = True

            if improper_syntax_in_expression:
                return "improper syntax"

        if incorrectly_placed_parentheses:
            open_parentheses_count = 0
            for char in expression:
                if char == "(":
                    open_parentheses_count += 1
                elif char == ")":
                    open_parentheses_count -= 1

                if open_parentheses_count < 0:
                    return "closing parenthesis with no matching open parenthesis"

            if open_parentheses_count > 0:
                return "unclosed parentheses"

        if is_equation:
            return "equation is correct"
        else:
            return "expression is correct"

    @staticmethod
    def sympy_simplify_expression(expression):
        """Returns a tuple containing whether the simplification was successful
        and in case it was the resulting simplified expression."""

        # using sympy on (x+1)(x-3) returns an error, but on (x+1)*(x-3) it doesn't
        i = 0
        length_of_expression = len(expression)
        while i < length_of_expression - 1:
            char = expression[i]
            if char.isdigit() and expression[i + 1] in "x(":
                expression = expression[:i + 1] + "*" + expression[i + 1:]
                length_of_expression += 1
            elif char in "x)" and (expression[i + 1].isdigit() or expression[i + 1] in "x("):
                expression = expression[:i + 1] + "*" + expression[i + 1:]
                length_of_expression += 1
            i += 1

        # sympy raises an exception if you use '^' as the exponentiation operator
        expression = expression.replace("^", "**")

        try:
            expression = sympy.parse_expr(expression)
            expression = sympy.simplify(expression)
        except Exception:
            print(traceback.format_exc())
            return False, ""

        expression = str(expression)
        expression = expression.replace(" ", "")
        expression = expression.replace("**", "^")

        return True, expression

    @staticmethod
    def expand_expression(expression):
        """Returns a tuple containing whether the expansion was successful
        and in case it was the resulting expression."""

        # using sympy on (x+1)(x-3) returns an error, but on (x+1)*(x-3) it doesn't
        i = 0
        length_of_expression = len(expression)
        while i < length_of_expression - 1:
            char = expression[i]
            if char.isdigit() and expression[i + 1] in "x(":
                expression = expression[:i + 1] + "*" + expression[i + 1:]
                length_of_expression += 1
            elif char in "x)" and (expression[i + 1].isdigit() or expression[i + 1] in "x("):
                expression = expression[:i + 1] + "*" + expression[i + 1:]
                length_of_expression += 1
            i += 1

        # sympy raises an exception if you use '^' as the exponentiation operator
        expression = expression.replace("^", "**")

        try:
            expression = sympy.parse_expr(expression)
            expression = sympy.expand(expression)
        except Exception:
            print(traceback.format_exc())
            return False, ""

        expression = str(expression)
        expression = expression.replace(" ", "")
        expression = expression.replace("**", "^")

        return True, expression

    @staticmethod
    def add_multiplication_signs(expression, has_trigonometric_functions=False):
        trig_identities = ["sin", "cos", "tan", "cot", "sec", "csc"]
        inverse_trig_identities = ["asin", "acos", "atan", "acot", "asec", "acsc"]

        len_expression = len(expression)
        i = 0
        while i < len_expression - 1:
            if expression[i].isalpha() and expression[i + 1] == "(":
                if has_trigonometric_functions:
                    if i >= 2 and expression[i-2:i+1] in trig_identities:
                        i += 1
                        continue
                    elif i >= 3 and expression[i-3:i+1] in inverse_trig_identities:
                        i += 1
                        continue
                    else:
                        expression = expression[:i + 1] + "*" + expression[i + 1:]
                        len_expression += 1
                else:
                    expression = expression[:i + 1] + "*" + expression[i + 1:]
                    len_expression += 1
            elif expression[i].isalpha() and expression[i + 1].isalpha():
                if has_trigonometric_functions:
                    """If we encounter 2 variables next to each other in the expression we need to make sure they
                    aren't part of a trig identity (ex: we don't want to transform sin(x) into s*i*n(x))
                    To do that we replace all trig identities with 0's and check that our current character is
                    still a letter
                    Note: We need to start with inverse trig identities first because otherwise asin(x) will be
                    converted to a000(x) which will become a*sin(x)"""
                    expression_copy = expression
                    for inverse_trig_identity in inverse_trig_identities:
                        index_of_inverse_trig_identity = expression_copy.find(inverse_trig_identity)
                        while index_of_inverse_trig_identity > -1:
                            expression_copy = expression_copy[:index_of_inverse_trig_identity] + "0000" + \
                                              expression_copy[index_of_inverse_trig_identity + 4:]
                            index_of_inverse_trig_identity = expression_copy.find(inverse_trig_identity)
                    for trig_identity in trig_identities:
                        index_of_trig_identity = expression_copy.find(trig_identity)
                        while index_of_trig_identity > -1:
                            expression_copy = expression_copy[:index_of_trig_identity] + "000" + \
                                              expression_copy[index_of_trig_identity + 3:]
                            index_of_trig_identity = expression_copy.find(trig_identity)

                    if expression_copy[i].isalpha():
                        expression = expression[:i + 1] + "*" + expression[i + 1:]
                        len_expression += 1
                else:
                    expression = expression[:i + 1] + "*" + expression[i + 1:]
                    len_expression += 1
            elif expression[i] == ")" and (expression[i+1].isdigit() or expression[i+1].isalpha() or
                                           expression[i+1] == "("):
                expression = expression[:i + 1] + "*" + expression[i + 1:]
                len_expression += 1
            elif expression[i].isdigit() and (expression[i + 1].isalpha() or expression[i + 1] == "("):
                expression = expression[:i + 1] + "*" + expression[i + 1:]
                len_expression += 1
            i += 1

        return expression

    @staticmethod
    def is_quadratic(expression):
        """Returns True or False depending on whether expression is quadratic or not.
        Expressions containing x^1 and/or constants are considered quadratic.
        Negative exponents are assumed to be written in this format: x^(-n).
        This function only works if expression has correct syntax, only contains the variable x and
        if '^' is the exponentiation sign."""

        length_expression = len(expression)
        for i in range(length_expression - 1):
            if expression[i] == "^":
                if expression[i + 1].isdigit():
                    if int(expression[i + 1]) > 2:
                        return False
                    elif i < length_expression - 2:
                        if expression[i + 2].isdigit():
                            return False
                        elif expression[i + 2] == ".":
                            return False
                elif expression[i + 1:i + 3] == "(-":
                    return False

        return True

    @staticmethod
    def extract_coefficients_from_quadratic(expression):
        x_squared_coeff_regex = re.compile("(-?\d*)\*?x\^2")
        x_coeff_regex = re.compile("(-?\d*)\*?x[^\^]|(-?\d*)\*?x$")
        constant_coeff_regex = re.compile("[^\^](-?\d+)$|^(-?\d+)$|^(\d+)-")

        regex_matches = x_squared_coeff_regex.findall(expression)
        if len(regex_matches) == 0:
            x_squared_coeff = 0
        else:
            if regex_matches[0] == "":
                x_squared_coeff = 1
            elif regex_matches[0] == "-":
                x_squared_coeff = -1
            else:
                x_squared_coeff = int(regex_matches[0])

        regex_matches = x_coeff_regex.findall(expression)
        if len(regex_matches) == 0:
            x_coeff = 0
        else:
            x_coeff = 1
            for group_matched in regex_matches[0]:
                if len(group_matched) > 0:
                    if group_matched != "-":
                        x_coeff = int(group_matched)
                    else:
                        x_coeff = -1

        regex_matches = constant_coeff_regex.findall(expression)
        if len(regex_matches) == 0:
            constant_coeff = 0
        else:
            for group_matched in regex_matches[0]:
                if len(group_matched) > 0:
                    constant_coeff = int(group_matched)

        return x_squared_coeff, x_coeff, constant_coeff

    @staticmethod
    def find_roots_of_quadratic(x_squared_coeff, x_coeff, constant_coeff):
        """Returns the roots of a polynomial(quadratic or lower degree), only using the coefficients of its terms.
        Examples:
        y=6(x_squared_coeff=0, x_coeff=0, constant_coeff=6) -> None (no values of x can make y=0)
        y=0(x_squared_coeff=0, x_coeff=0, constant_coeff=0) -> 'infinite' (all values of x can make y=0)
        y=-3x + 6(x_squared_coeff=0, x_coeff=-3, constant_coeff=6) -> 2 (only x=2 can make y=0)
        y=2x^2 - 8x + 6 (x_squared_coeff=2, x_coeff=-8, constant_coeff=6) -> (3, 1) (only x=3 and x=1 can make y=0)
        y=4x^2 - 12x + 9(x_squared_coeff=4, x_coeff=-12, constant_coeff=9) -> 1.5 (only x=1.5 can make y=0)"""
        if x_squared_coeff == 0 and x_coeff == 0:
            if constant_coeff != 0:
                return None
            else:
                return "infinite"

        elif x_squared_coeff == 0:
            result = -(constant_coeff / x_coeff)
            result = round(result, 4)
            if result == int(result):
                result = int(result)

            return result

        else:
            a = x_squared_coeff
            b = x_coeff
            c = constant_coeff

            delta = b ** 2 - 4 * a * c
            x1 = (-b + delta**0.5) / (2*a)
            x2 = (-b - delta**0.5) / (2*a)

            if x1.imag and x2.imag:
                x1 = complex(round(x1.real, 4), round(x1.imag, 4))
                x2 = complex(round(x2.real, 4), round(x2.imag, 4))
            else:
                x1 = round(x1, 4)
                x2 = round(x2, 4)

                if x1 == int(x1):
                    x1 = int(x1)
                if x2 == int(x2):
                    x2 = int(x2)

            if x1 != x2:
                return x1, x2
            else:
                return x1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MathApp()
    app.exec()
