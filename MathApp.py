from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout, QLabel, QComboBox, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6 import uic
import sys


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

        self.show()

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

    def calculate_roots_for_polynomial(self):
        self.clear_temporary_widgets()

        equation = self.polynomialRootsEquationInsertionLineEdit.text()
        equation.replace(" ", "")

        for char in equation:
            if char.isalpha() and char not in ["x", "y"]:
                warning = QLabel(self)
                warning.setText("Please only use lowercase x and y as variables in your equation, "
                                "where x is the independent variable!")
                warning.setStyleSheet("color: red;")
                warning.setFont(self.main_font)
                warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
                warning.setSizePolicy(self.minimum_size_policy)
                self.temporary_widgets.append(warning)
                self.mathAppGrid.addWidget(warning, 9, 1, 1, 3)
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MathApp()
    app.exec()
