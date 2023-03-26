import smtplib
from email.mime.text import MIMEText


def send_email(gmail_user, gmail_password, to, subject, body):
    """
    Sends an email using Gmail.

    Args:
        gmail_user (str): The Gmail account email address.
        gmail_password (str): The Gmail account password.
        to (str): The recipient email address.
        subject (str): The email subject.
        body (str): The email body.
    """
    # Create a MIMEText object to represent the email message
    msg = MIMEText(body)
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    # Send the email using the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, msg.as_string())

    print('Email sent successfully')
