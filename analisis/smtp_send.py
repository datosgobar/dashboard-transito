#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import config

def send_email_error(error_msg):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "update error: dashboardoperativo {0}".format(datetime.datetime.now())
    msg['From'] = config.email["user"]
    msg['To'] = config.email["to"]
    
    text = "API Sensores Error\nAlerta api sensores esta fallando\n"
    html2 = '<html><head></head><body><p>API Sensores Error<br><b>Alerta api sensores esta fallando {0}</b></p></body></html>'.format(error_msg)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html2, "html")
    msg.attach(part1)
    msg.attach(part2)
    s = smtplib.SMTP('smtp.buenosaires.gob.ar')

    if config.email['debug']:
        s.set_debuglevel(1)

    s.ehlo()
    s.starttls()
    s.ehlo

    s.login(config.email["user"], config.email["pwd"])
    s.sendmail(config.email["user"], config.email["to"], msg.as_string())
    s.quit()

if __name__ == '__main__':
    send_email_error()