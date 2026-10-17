import bcrypt
import random
import string
import datetime
from utils.db import get_db
from utils.mailer import send_email

OTP_EXPIRY_MINUTES = 10


def register_user(data):

    connection = get_db()
    cursor = connection.cursor(dictionary=True)

    # Check username
    cursor.execute(

"SELECT * FROM users WHERE USERNAME=%s",

(data["username"],)

)

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return {
            "success": False,
            "message": "Username already exists."
        }

    # Check email
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (data["email"],)
    )

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return {
            "success": False,
            "message": "Email already exists."
        }

    password_hash = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute("""

        INSERT INTO users
        (
            full_name,
            username,
            email,
            password_hash,
            institution,
            country,
            role
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s)

    """,

    (
        data["full_name"],
        data["username"],
        data["email"],
        password_hash,
        data["institution"],
        data["country"],
        "User"
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return {

        "success": True,

        "message": "Registration Successful."

    }

def login_user(data):

    connection = get_db()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(

        "SELECT * FROM users WHERE email=%s",

        (data["email"],)

    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user is None:

        return {

            "success": False,

            "message": "Email not found."

        }

    if not bcrypt.checkpw(

        data["password"].encode(),

        user["password_hash"].encode()

    ):

        return {

            "success": False,

            "message": "Incorrect password."

        }

    return {

        "success": True,

        "message": "Login Successful.",

        "user": {

            "id": user["user_id"],

            "name": user["full_name"],

            "role": user["role"]

        }

    }

def generate_otp():

    return "".join(
        random.SystemRandom().choice(string.digits)
        for _ in range(6)
    )


def request_password_reset(email):
    """
    Looks up the account by email and, if it exists, generates a 6
    digit OTP, stores its hash with a 10 minute expiry, and emails it
    to the user. Always returns a generic success message regardless
    of whether the email was found, so this endpoint can't be used to
    check which emails are registered.
    """

    connection = get_db()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    generic_response = {

        "success": True,

        "message": "If that email is registered, an OTP has been sent to it."

    }

    if user is None:

        cursor.close()
        connection.close()

        return generic_response

    otp = generate_otp()

    otp_hash = bcrypt.hashpw(
        otp.encode(),
        bcrypt.gensalt()
    ).decode()

    expires_at = datetime.datetime.now() + datetime.timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )

    cursor.execute(
        """

        INSERT INTO password_resets
        (user_id, otp_hash, expires_at)
        VALUES (%s, %s, %s)

        """,
        (user["user_id"], otp_hash, expires_at)
    )

    connection.commit()

    cursor.close()
    connection.close()

    send_email(
        to_email=user["email"],
        subject="Your PhytoVault Password Reset Code",
        body=(
            f"Hello {user['full_name']},\n\n"
            f"Your OTP to reset your PhytoVault password is: {otp}\n\n"
            f"This code will expire in {OTP_EXPIRY_MINUTES} minutes. "
            "If you didn't request this, you can safely ignore this email.\n\n"
            "- PhytoVault Team"
        )
    )

    return generic_response


def reset_password_with_otp(email, otp, new_password):

    connection = get_db()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    invalid_response = {

        "success": False,

        "message": "Invalid email or OTP."

    }

    if user is None:

        cursor.close()
        connection.close()

        return invalid_response

    cursor.execute(
        """

        SELECT * FROM password_resets
        WHERE user_id=%s AND used=FALSE
        ORDER BY reset_id DESC
        LIMIT 1

        """,
        (user["user_id"],)
    )

    reset_row = cursor.fetchone()

    if reset_row is None:

        cursor.close()
        connection.close()

        return invalid_response

    if reset_row["expires_at"] < datetime.datetime.now():

        cursor.close()
        connection.close()

        return {

            "success": False,

            "message": "This OTP has expired. Please request a new one."

        }

    if not bcrypt.checkpw(
        otp.encode(),
        reset_row["otp_hash"].encode()
    ):

        cursor.close()
        connection.close()

        return invalid_response

    new_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        "UPDATE users SET password_hash=%s WHERE user_id=%s",
        (new_hash, user["user_id"])
    )

    cursor.execute(
        "UPDATE password_resets SET used=TRUE WHERE reset_id=%s",
        (reset_row["reset_id"],)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {

        "success": True,

        "message": "Password reset successful. You can now log in."

    }
