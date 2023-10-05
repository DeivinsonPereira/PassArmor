import sqlite3
from passlib.hash import sha256_crypt


# Function to create the user table in the SQLite database
def create_user_table():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT UNIQUE,
                       password TEXT)''')

    conn.commit()
    conn.close()


# Function to register a new user
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Criptografa a senha
    hashed_password = sha256_crypt.hash(password)

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hashed_password))
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different one.")

    conn.close()


# Function to log in
def login():
    username = input("Enter the username: ")
    password = input("Enter a password: ")

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if row:
        stored_password = row[0]
        if sha256_crypt.verify(password, stored_password):
            print("Successful login.")
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")

    conn.close()


# Main function
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
