import sqlite3
from passlib.hash import sha256_crypt
import secrets
import time

MAX_LOGIN_ATTEMPTS = 3


def create_user_table():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

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


def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

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
        print("Username already exists. Please choose a different one.")

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
