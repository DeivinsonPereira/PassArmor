import sqlite3
from passlib.hash import sha256_crypt
from email_validator import validate_email, EmailNotValidError
import secrets
import time
import re

MAX_LOGIN_ATTEMPTS = 3


def create_user_table():
    with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        conn = sqlite3.connect('user.db')

        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT UNIQUE,
                           password TEXT,
                           salt TEXT,
                           login_attempts INTEGER DEFAULT 0,
                           last_attempt_timestamp REAL DEFAULT 0,
                           locked INTEGER DEFAULT 0)''')

        conn.commit()
        conn.close()


# Generates a random salt
def generate_salt():
    return secrets.token_hex(16)


# Check the email format
def is_valid_email(username):
    try:
        validate_email(username)
        return True
    except EmailNotValidError:
        return False


# To validate the password strength
def is_strong_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not re.search(r'[!@#$%^&*.]', password):
        return False
    return True


def get_email_validation_message(username):
    if is_valid_email(username):
        return None
    return "Invalid email address."


def get_password_validation_message(password):
    if is_strong_password(password):
        return None
    return (
        "Password is not strong enough. Passwords must have at least 8 characters, "
        "including at least one uppercase letter, one lowercase letter, one digit, "
        "and one special character."
    )


def register_user():
    while True:
        username = input("Enter an email address: ")
        email_validation_message = get_email_validation_message(username)

        if email_validation_message is None:
            break
        else:
            print(email_validation_message)

    while True:
        password = input("Enter a password: ")
        password_validation_message = get_password_validation_message(password)

        if password_validation_message is None:
            break
        else:
            print(password_validation_message)

    salt = generate_salt()

    salted_password = salt + password

    # Encryption of the new password
    hashed_password = sha256_crypt.hash(salted_password)

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
                       (username, hashed_password, salt))
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username (email) already exists or is invalid. Please choose a different one.")

    conn.close()


def login():
    username = input("Enter the username: ")
    password = input("Enter a password: ")

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, password, salt, locked, login_attempts FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if row:
        user_id, stored_password, salt, locked, login_attempts = row

        if locked:
            print("Account is locked. Please contact the administrator.")
        elif sha256_crypt.verify(salt + password, stored_password):
            # Successful login, login attempts reset
            cursor.execute("UPDATE users SET login_attempts = 0 WHERE id=?", (user_id,))
            conn.commit()
            print("Successful login.")
        else:
            # Incorrect password, increase login attempts counter
            login_attempts += 1
            cursor.execute("UPDATE users SET login_attempts = ?, last_attempt_timestamp = ? WHERE id=?",
                           (login_attempts, time.time(), user_id))
            conn.commit()
            print("Incorrect password.")

            if login_attempts >= MAX_LOGIN_ATTEMPTS:
                # Locks the account after 3 unsuccessful login attempts
                cursor.execute("UPDATE users SET locked = 1 WHERE id=?", (user_id,))
                conn.commit()
                print("Account locked. Please contact the administrator.")

    else:
        print("Username not found.")

    conn.close()


# Função principal
def main():
    create_user_table()

    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Sign in")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
