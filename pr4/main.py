import sys
from PyQt5 import QtWidgets
import design
import requests

settings = {"yandex": {"host": "smtp.yandex.ru", "port": 465},
            "mail": {"host": "smtp.mail.ru", "port": 25},
            "gmail": {"host": "smtp.gmail.com", "port": 587}
            }


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send_mail)
        self.file_button.clicked.connect(self.browse_file)
        self.server_name = self.comboBox.currentText()
        self.filenames = []

    def send_mail(self):
        data = {
            "email": self.email.text(), "subject": self.subject.text(), "text": self.mailText.toPlainText(),
            "from_addr": self.from_addr.text(), "password": self.lineEdit.text(),
            "host": settings[self.server_name]["host"], "port": settings[self.server_name]["port"]
        }
        requests.post("http://localhost:5000/", data=data,
                      files=[("file", open(x, 'rb')) for x in self.filenames] if len(self.filenames) > 0 else None)
        self.filenames = []
        self.files_widjet.clear()

    def browse_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Открыть файл", r"C:\\", "AllFiles (*)"
        )
        for file in (filename[0]):
            self.files_widjet.addItem(file)
            self.filenames.append(file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
