import mimetypes
import sys
from email import encoders
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from PyQt5 import QtWidgets
import smtplib

import design

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
        server_name = self.comboBox.currentText()
        self.server = smtplib.SMTP_SSL(settings[server_name]["host"], settings[server_name]["port"])
        self.filenames = []

    def send_mail(self):
        email, subject, text = self.email.text(), self.subject.text(), self.mailText.toPlainText()
        from_addr, password = self.from_addr.text(), self.lineEdit.text()
        msg = EmailMessage()
        msg['Subject'], msg['From'], msg['To'] = subject, from_addr, email.split("; ")
        msg.set_content(text)
        msg = self.create_attachment(msg)
        print(msg)
        self.server.login(from_addr, password)
        self.server.send_message(msg)
        self.server.quit()
        self.filenames = []

    def browse_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Открыть файл", r"C:\\", "AllFiles (*)"
        )
        for file in (filename[0]):
            self.files_widjet.addItem(file)
            self.filenames.append(file)

    def create_attachment(self, msg):
        for filepath in self.filenames:
            ctype, encoding = mimetypes.guess_type(filepath)
            if ctype is None or encoding is None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(filepath) as fp:
                    file = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
            elif maintype == 'image':
                with open(filepath, 'rb') as fp:
                    file = MIMEImage(fp.read(), _subtype=subtype)
                    fp.close()
            elif maintype == 'audio':
                with open(filepath, 'rb') as fp:
                    file = MIMEAudio(fp.read(), _subtype=subtype)
                    fp.close()
            else:
                with open(filepath, 'rb') as fp:
                    file = MIMEBase(maintype, subtype)
                    file.set_payload(fp.read())
                    fp.close()
                    encoders.encode_base64(file)
            file.add_header('Content-Disposition', 'attachment', filename=filepath.split("/")[-1])
            msg.add_attachment(file)
        return msg


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
