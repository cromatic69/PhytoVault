/*=========================================================
    MIGRATION: Add OTP-based password reset support
    Run this against an EXISTING phytovault database
    (do not use this on a fresh install - phytovault.sql
    already includes this table).
=========================================================*/

USE phytovault;

CREATE TABLE IF NOT EXISTS password_resets (

    reset_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    otp_hash VARCHAR(255) NOT NULL,

    expires_at DATETIME NOT NULL,

    used BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE

);
