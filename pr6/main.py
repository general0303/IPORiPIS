import sys

from PyQt5 import QtWidgets, QtGui

import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.saveButton.clicked.connect(self.save)
        self.openButton.clicked.connect(self.browse_file)
        self.setButton.clicked.connect(lambda:
                                       self.textEdit.setFont(QtGui.QFont(self.comboBox.currentText(),
                                                                         self.size.value())))
        self.filename = None

    def browse_file(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "Открыть файл", r"C:\\", "AllFiles (*)"
        )[0]
        with open(self.filename, "r") as f:
            self.textEdit.setText(f.read())

    def save(self):
        with open(self.filename, "w") as f:
            f.write(self.textEdit.toPlainText())
        self.filename = None
        self.textEdit.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
