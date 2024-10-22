import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to):
    """Send an email using Gmail SMTP server.

    Parameters:
    - subject (str): The subject of the email
    - body (str): The body of the email
    - to (str): The recipient's email address

    Returns:
    - None
    """
    # Set up the server
    # Please note that using environment variables for sensitive information
    # is recommended for production use.
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = os.getenv('SENDER_MAIL')
    password = os.getenv('SENDER_PASSWORD')

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server and send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.send_message(msg)

        print(f"Email sent successfully to {to}")

    except Exception as e:
        print(f"Failed to send email to {to}. Error: {e}")
