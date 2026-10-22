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
    # Email Configuration (Resend HTTP API)
    # -----------------------------
    RESEND_API_KEY = os.environ.get(
        "RESEND_API_KEY",
        ""
    )

    MAIL_FROM = os.environ.get(
        "MAIL_FROM",
        "PhytoVault <onboarding@resend.dev>"
    )
