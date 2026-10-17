from flask import Blueprint, request, jsonify, session, redirect, flash, render_template
from services.auth_service import (
    register_user,
    login_user,
    request_password_reset,
    reset_password_with_otp
)
from utils.db import get_db
from flask import flash

# Create Blueprint FIRST
auth = Blueprint("auth", __name__)


# -----------------------------
# Register
# -----------------------------
@auth.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    result = register_user(data)

    return jsonify(result)


# -----------------------------
# Login
# -----------------------------
@auth.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    result = login_user(data)

    if result["success"]:
        session["user"] = result["user"]

    return jsonify(result)

@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# -----------------------------
# Forgot / Reset Password
# -----------------------------
@auth.route("/forgot-password")
def forgot_password_page():

    return render_template("forgot_password.html")


@auth.route("/api/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = (data.get("email") or "").strip()

    result = request_password_reset(email)

    return jsonify(result)


@auth.route("/reset-password")
def reset_password_page():

    email = request.args.get("email", "")

    return render_template("reset_password.html", email=email)


@auth.route("/api/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    result = reset_password_with_otp(
        (data.get("email") or "").strip(),
        (data.get("otp") or "").strip(),
        data.get("password") or ""
    )

    return jsonify(result)

@auth.route("/delete-account")
def delete_account():

    user = session.get("user")

    if not user:

        return redirect("/login")

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute(

        "DELETE FROM users WHERE user_id=%s",

        (user["id"],)

    )

    connection.commit()

    cursor.close()

    connection.close()

    session.clear()

    flash("Account deleted successfully.")

    return redirect("/")

@auth.route("/profile", methods=["GET", "POST"])
def profile():

    user = session.get("user")

    if not user:

        return redirect("/login")

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""

        UPDATE users

        SET

        full_name=%s,
        institution=%s,
        country=%s

        WHERE user_id=%s

        """,

        (

            request.form["full_name"],
            request.form["institution"],
            request.form["country"],
            user["id"]

        ))

        connection.commit()

        session["user"]["name"] = request.form["full_name"]

        flash("Profile Updated Successfully")

    cursor.execute(

        """

        SELECT

        *

        FROM users

        WHERE user_id=%s

        """,

        (user["id"],)

    )

    user_data = cursor.fetchone()

    cursor.close()

    connection.close()

    return render_template(

        "profile.html",

        user=user_data

    )