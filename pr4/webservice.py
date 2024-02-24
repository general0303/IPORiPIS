import mimetypes
import os
import shutil
import smtplib
from email import encoders
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from flask import Flask, request

app = Flask(__name__)


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


def create_attachment(msg, filenames):
    if filenames is None:
        return msg
    for filepath in filenames:
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


@app.route("/", methods=["POST"])
def send():
    os.mkdir("temp")
    filenames = []
    if "file" in request.files:
        print(request.files)
        for file in request.files.getlist('file'):
            if file.filename != "":
                file.save(os.path.join("temp", file.filename))
                filenames.append(os.path.join("temp", file.filename))
    server = smtplib.SMTP_SSL(request.form['host'], int(request.form['port']))
    email, subject, text = request.form['email'], request.form['subject'], request.form['text']
    from_addr, password = request.form['from_addr'], request.form['password']
    msg = EmailMessage()
    msg['Subject'], msg['From'], msg['To'] = subject, from_addr, email.split("; ")
    msg.set_content(text)
    if len(filenames) > 0:
        msg = create_attachment(msg, filenames)
    print(msg)
    server.login(from_addr, password)
    server.send_message(msg)
    server.quit()
    shutil.rmtree("temp")
    return "ok", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
