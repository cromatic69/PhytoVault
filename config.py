import os

class Config:

    # -----------------------------
    # Flask Configuration
    # -----------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "PhytoVault2026")

    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False

    # -----------------------------
    # MySQL Configuration
    # -----------------------------
    MYSQL_HOST = os.environ.get("MYSQLHOST", "localhost")

    MYSQL_PORT = int(os.environ.get("MYSQLPORT", 3306))

    MYSQL_USER = os.environ.get("MYSQLUSER", "root")

    MYSQL_PASSWORD = os.environ.get(
        "MYSQLPASSWORD",
        "iwantsomepeace@69"
    )

    MYSQL_DATABASE = os.environ.get(
        "MYSQLDATABASE",
        "phytovault"
    )

    # -----------------------------
    # Email Configuration
    # -----------------------------
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")

    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))

    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME",
        "ayushsenpai6969@gmail.com"
    )

    MAIL_PASSWORD = os.environ.get(
        "MAIL_PASSWORD",
        ""
    )

    MAIL_FROM = os.environ.get(
        "MAIL_FROM",
        "PhytoVault <ayushsenpai6969@gmail.com>"
    )