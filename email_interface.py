import yagmail
import imaplib
import email
import traceback
import re
import platform
from credential import Credential

class EmailInterface:
    def __init__(self):
        self.credential = Credential()
        print('Email interface initialized')

    # return validation code
    def get_validation_code(self) -> str:
        return self.extract_validation_code(self.get_validation_email_content())

    # retrieve the most recent validation email content in raw string format
    def get_validation_email_content(self) -> str:
        try:
            # login
            con = imaplib.IMAP4_SSL('imap.gmail.com')
            con.login(
                self.credential.validation_email_account() + '@gmail.com',
                self.credential.validation_email_password()
            )
            # select inbox
            con.select('INBOX')
            # search inbox emails for amazon validation emails
            data = con.search(None, 'FROM', 'no-reply@amazon.work')
            # get most recent email's id
            id = int(data[1][0].split()[-1])
            # get first instance of valid email body
            data = con.fetch(str(id), '(RFC822)')
            for response in data:
                arr = response[0]
                if isinstance(arr, tuple):
                    message = email.message_from_string(str(arr[1], 'utf-8'))
                    body = message.get_payload(decode = True)
                    break
            # terminate connection
            con.close()
            con.logout()
            # return message content
            return body
        except:
            traceback.print_exc()

    # parse and extract validation code from email content string
    def extract_validation_code(self, input: str) -> str:
        return re.findall('[0-9]{6,6}', str(input))[0]

    def status_report(self, status: bool, message: str):
        yag = yagmail.SMTP(self.credential.report_email_account(), self.credential.report_email_password())
        email_title = str(platform.node()) + ': '
        if status:
            email_title += 'AtoZ Successful'
        else:
            email_title += 'AtoZ Failed'
        yag.send(self.credential.report_receiver_email(), email_title, message)
        print('email report sent')

    def password_reminder(self):
        yag = yagmail.SMTP(self.credential.validation_email_account(), self.credential.validation_email_password())
        message = 'Your AtoZ password is expiring on {}. Please update it.'.format(self.credential.password_expiration_date())
        yag.send(self.credential.report_receiver_email(), 'Password Expiring Soon', message)
