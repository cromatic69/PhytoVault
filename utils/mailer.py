import requests

from config import Config


def send_email(to_email, subject, body):
    """
    Sends a plain-text email via the Resend HTTP API.

    Uses HTTPS (port 443) instead of raw SMTP, because many hosts
    (including Render's free tier) block outbound SMTP connections,
    which used to make this call hang until the request worker timed
    out. An HTTP API call fails fast and cleanly instead.

    Returns True on success, False on failure (failures are not raised
    so that a mail-server hiccup doesn't crash the request - callers
    should check the return value and respond accordingly).
    """

    try:

        response = requests.post(

            "https://api.resend.com/emails",

            headers={

                "Authorization": f"Bearer {Config.RESEND_API_KEY}",
                "Content-Type": "application/json"

            },

            json={

                "from": Config.MAIL_FROM,
                "to": [to_email],
                "subject": subject,
                "text": body

            },

            timeout=10

        )

        if response.status_code >= 400:

            print("Failed to send email:", response.status_code, response.text)
            return False

        return True

    except Exception as e:

        print("Failed to send email:", e)
        return False
