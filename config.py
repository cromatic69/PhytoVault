import os

class Config:

    SECRET_KEY = "PhytoVault2026"

    MYSQL_HOST = "localhost"

    MYSQL_USER = "root"

    MYSQL_PASSWORD = "iwantsomepeace@69" 

    MYSQL_DATABASE = "phytovault"

    SESSION_TYPE = "filesystem"

    SESSION_PERMANENT = False

    # -----------------------------
    # Email (used to send password-reset OTPs)
    # -----------------------------
    # For Gmail: enable 2-Step Verification on the account, then
    # generate an "App Password" and use that below instead of the
    # normal account password.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")

    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "ayushsenpai6969@gmail.com")

    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "jhsbrdrsxheqmjwi")

    MAIL_FROM = os.environ.get("MAIL_FROM", "PhytoVault <ayushsenpai6969@gmail.com>")