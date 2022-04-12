import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import datetime
import traceback
from os import remove, path
from auth_data import sender, password, recip


def send_email_log_error():
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg['Subject'] = 'Crew_Bot Error' + str(datetime.datetime.now())
        msg.attach(MIMEText('Crew_Bot Error'))

        with open('logs/log_error.txt', 'r', encoding='utf-8') as f:
            file = MIMEText(f.read())
        file.add_header('content-disposition', 'attachment', filename='logs/log_error.txt')
        msg.attach(file)

        server.sendmail(sender, 'fakir_x@mail.ru', msg.as_string())
        # remove('log.txt')
    except:
        with open('logs/log_email.txt', 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.now()) + ': ' + str(traceback.format_exc()) + '______\n')
        return 'log error is NOT send'
    return 'log error is send'

def send_email_log_message():
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg['Subject'] = 'Crew_Bot_message_log' + str(datetime.datetime.now())
        msg.attach(MIMEText('Crew_Bot_message_log'))

        with open('data/text_log.txt', 'r', encoding='utf-8') as f:
            file = MIMEText(f.read())
        file.add_header('content-disposition', 'attachment', filename='text_log.txt')
        msg.attach(file)

        server.sendmail(sender, recip, msg.as_string())
        #remove('data/text_log.txt')
    except:
        with open('logs/log_email.txt', 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.now()) + ': ' + str(traceback.format_exc()) + '______\n')
        if path.getsize('logs/log_error.txt') == 1048576:
            remove('logs/log_error.txt')
        time.sleep(5)
        return 'log message is NOT send'
    return 'log message is send'


def main():
    send_email_log_error()
    send_email_log_message()


if __name__ == '__main__':
    main()
