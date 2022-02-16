from email.mime.application import MIMEApplication
import subprocess
from tabulate import tabulate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP, SMTPException
import os
from configparser import ConfigParser

# mail trigger and configuration function


def mail_notification(body):
    config = ConfigParser()
    config.read('.env')
    SMTP_PORT = config['mailconfig']['SMTP_PORT']
    SMTP_SENDER = config['mailconfig']['SMTP_SENDER']
    SMTP_PASSWORD = config['mailconfig']['SMTP_PASSWORD']
    SMTP_RECEIVERS = config['mailconfig']['SMTP_RECEIVERS']
    SMTP_HOST = config['mailconfig']['SMTP_HOST']
    SUBJECT = "Health Check for BMS Project"
    message = []
    # Setup the MIME
    msgData = MIMEMultipart()
    msgData['From'] = SMTP_SENDER
    msgData['To'] = SMTP_RECEIVERS
    msgData['Subject'] = SUBJECT  # The subject line

    for d in body:
        constainer_status = []
        logs = [subprocess.getoutput(
            f'docker logs --tail 100 {d["container_name"]}')]

        if (d != {} and d['statusCode'] != 200):
            constainer_status.append(subprocess.getoutput(
                'docker inspect -f "{0}" {1}'.format("{{ .State.Status }}", d["container_name"])))
            with open("logs.txt", "a") as f:
                f.writelines(logs)

            os.system(f'docker restart {d["container_name"]}')
            newData = {
                "Container Name": d["container_name"],
                "Service Name":  d["service_name"],
                "Response Code": d["statusCode"],
                "Container Status": constainer_status[0],
                "Message": f'Container {d["container_name"]} restarted successfully!',
            }
            message.append(newData)

        else:
            constainer_status.append(subprocess.getoutput(
                'docker inspect -f "{0}" {1}'.format("{{ .State.Status }}", d["container_name"])))
            newData = {
                "Container Name": d["container_name"],
                "Service Name":  d["service_name"],
                "Response Code": d["statusCode"],
                "Container Status": constainer_status[0],
                "Message": d['message']
            }
            message.append(newData)
    bodyData = tabulate(message, headers="keys", showindex="always")

    try:

        msgData.attach(MIMEText(bodyData, 'plain'))
        with open("logs.txt", "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name="logs.txt"
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="logs.txt"'
        msgData.attach(part)
        text = msgData.as_string()
        print('Mail trigger started...')
        with SMTP(SMTP_HOST, SMTP_PORT) as smtpObj:
            # smtpObj = SMTP(SMTP_HOST, SMTP_PORT)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            print('Mail server connected!')
            smtpObj.login(SMTP_SENDER, SMTP_PASSWORD)
            print('Login Successful')
            smtpObj.sendmail(SMTP_SENDER, SMTP_RECEIVERS, text)
            smtpObj.quit()
            print('Successfully sent email')
    except SMTPException as err:
        print('Error: unable to send email', err)
