import smtplib
from email.mime.text import MIMEText

from config import Config


def send_email(to_email, subject, body):
    """
    Sends a plain-text email using the Gmail SMTP settings in config.py.

    A short timeout is set on the connection so that if the host
    blocks outbound SMTP (as Render's free tier does), this fails
    quickly with a clear error instead of hanging until the whole
    request worker is killed.

    Returns True on success, False on failure (failures are not raised
    so that a mail-server hiccup doesn't crash the request - callers
    should check the return value and respond accordingly).
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_FROM
    msg["To"] = to_email

    try:

        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=10) as server:

            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.sendmail(Config.MAIL_FROM, [to_email], msg.as_string())

        return True

    except Exception as e:

        print("Failed to send email:", e)
        return False
