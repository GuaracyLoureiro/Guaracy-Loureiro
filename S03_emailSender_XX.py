#!/usr/bin/env python
# -----------------------------------------------------------------------------
#  Sending email using external emailing services
#    most of it is copied from Internet on various websites
# -----------------------------------------------------------------------------

import sys
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#MessageInfo
msg = MIMEMultipart()
msg['Subject'] = "[ALERT IN REARING UNITS] " + str(sys.argv[1]) + "°C " + str(sys.argv[2])
body = "ERROR : the average temperature over the last hour is of " + str(sys.argv[1]) + "°C for the rearing unit " + str(sys.argv[2])
msg.attach(MIMEText(body, 'plain'))
text = msg.as_string()

#ServerInfo
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("aaa@xxx.xxx", "password")

#Recipient(s)Info and send
toaddrlist=["xxx@xxx.xxx","yyy@xxx.xxx","zzz@xxx.xxx"]

for toaddr in toaddrlist:
	server.sendmail("aaa@xxx.xxx", toaddr, text)

server.quit()

#AlertFileWrite
with open('log_alert.txt', "a", newline = '') as myFile:
	myFile.write(str(datetime.datetime.now()) + ";" + str(sys.argv[1]) + ";" + str(sys.argv[2]) + "\n")
