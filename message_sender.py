import smtplib
import datetime
from email.mime.text import MIMEText

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


def message_sender(item, pattern, price, listing_id, inspect_link):
    datenow = datetime.datetime.now()
    email_data = ""
    with open("details.txt") as f:
        email_data = f.readlines()
    message = "Item found: "
    message += item["name"]
    message += "\n"
    message += "Date: "
    message += datenow.strftime("%Y-%m-%d %H:%M:%S")
    message += " "
    message += item["link"]
    message += "\npattern found: "
    message += pattern
    message += "\nprice: "
    message += price
    message += "\nadditional info: "
    message += listing_id
    message += "\ninspect link: "
    message += inspect_link
    title = "Item found " + item["name"] + " " + datenow.strftime("%Y-%m-%d %H:%M:%S")
    send_email(title, message, email_data[0], email_data[2].split(","), email_data[1])