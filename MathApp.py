from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QLabel, QComboBox
from PyQt6 import uic
import sys


class MathApp(QMainWindow):
    def __init__(self):
        super(MathApp, self).__init__()

        uic.loadUi("MathApp.ui", self)

        self.mainWindowGrid = self.findChild(QGridLayout, "mainWindowGridLayout")
        self.mathAppGrid = self.findChild(QGridLayout, "gridLayout")

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

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MathApp()
    app.exec()
