import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password, attachment_path):
    # Create the email header
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )

        msg.attach(part)

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Email details from environment variables
subject = "Playwright Test Report"
body = "Please find the attached Playwright test report."
to_email = os.getenv('TO_EMAIL')
from_email = os.getenv('FROM_EMAIL')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
login = os.getenv('EMAIL_LOGIN')
password = os.getenv('EMAIL_PASSWORD')
attachment_path = os.getenv('ATTACHMENT_PATH')

# Send the email
send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password, attachment_path)
