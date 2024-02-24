import sys
from PyQt5 import QtWidgets
import design

import numexpr as ne


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn.clicked.connect(lambda: self.resultLabel.setText(f"Результат: {ne.evaluate(self.plane.toPlainText())}"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
