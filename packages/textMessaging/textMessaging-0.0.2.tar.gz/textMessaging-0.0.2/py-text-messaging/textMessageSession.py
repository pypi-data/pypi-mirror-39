import smtplib

class TextMessageSession:
    def __init__(self, smtpAddress, port, email, password):
        self.server = smtplib.SMTP(smtpAddress, port)
        self.server.starttls()
        self.server.login(email, password)
        self.email = email

    def sendText(self, carrierAddress, phoneNumber, message):
        self.server.sendmail(carrierAddress, phoneNumber + "@" + carrierAddress, message)

