import logging
import traceback

from flask import Flask, render_template, session, redirect, request, jsonify
from flask_session import Session

from config import Config

from routes.auth import auth
from routes.plants import plants
from routes.admin import admin
from routes.search import search

app = Flask(__name__)

app.config.from_object(Config)

Session(app)

app.register_blueprint(auth)
app.register_blueprint(plants)
app.register_blueprint(admin)
app.register_blueprint(search)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("phytovault")


@app.route("/")
def home():

    return render_template(

        "index.html",

        user=session.get("user")

    )


@app.route("/admin-home")
def admin_home():

    user = session.get("user")

    if not user:

        return redirect("/login")

    if user["role"] != "Admin":

        return redirect("/")

    return render_template(

        "admin_home.html",

        user=user

    )


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/register")
def register():

    return render_template("register.html")


@app.errorhandler(404)
def not_found(error):

    return render_template("404.html"),404


@app.errorhandler(500)
def server_error(error):

    return render_template("500.html"),500


@app.errorhandler(Exception)
def handle_unexpected_error(error):

    # Let normal HTTP errors (404, the 500 above, etc.) go through
    # their own handlers instead of being swallowed here.
    from werkzeug.exceptions import HTTPException

    if isinstance(error, HTTPException):

        return error

    # Always log the full traceback server-side so it shows up in
    # Render's logs, even though the client only gets a safe message.
    logger.error(
        "Unhandled exception on %s %s:\n%s",
        request.method,
        request.path,
        traceback.format_exc()
    )

    if request.path.startswith("/api/"):

        return jsonify({

            "success": False,
            "message": "Server error. Please try again in a moment."

        }), 500

    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)