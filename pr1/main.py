import sys
from email.message import EmailMessage

from PyQt5 import QtWidgets
import smtplib

import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, from_addr, password):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send_mail)
        self.from_addr, self.password = from_addr, password
        self.server = smtplib.SMTP_SSL(f"smtp.{from_addr.split('@')[1]}", 465)

    def send_mail(self):
        email, subject, text = self.email.text(), self.lineEdit.text(), self.mailText.toPlainText()
        msg = EmailMessage()
        msg['Subject'], msg['From'], msg['To'] = subject, self.from_addr, email.split("; ")
        msg.set_content(text)
        self.server.login(self.from_addr, self.password)
        self.server.send_message(msg)
        self.server.quit()


def main():
    args = sys.argv
    addr, password = args[args.index("-addr") + 1], args[args.index("-pass") + 1]
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp(addr, password)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
