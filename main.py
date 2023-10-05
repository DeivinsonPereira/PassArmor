import hashlib

# Dictionary to store passwords
passwords = {}


def hash_password(password):
    # Function to create a password hash

    salt = "s4lT"  # A fixed value to add to the password before hashing it
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash


def store_password():
    website = input("Enter the name of the website or service: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    # Encrypt the password
    hashed_password = hash_password(password)

    # Store the password in the dictionary
    passwords[website] = {
        'username': username,
        'password': hashed_password
    }
    print("Password stored successfully!")


def retrieve_password():
    website = input("Enter the name of the website or service: ")

    if website in passwords:
        username = passwords[website]['username']
        print(f"Username: {username}")
    else:
        print("Site not found in the password manager.")


def verify_password():
    print(passwords)
    # User data input for login
    website = input("Enter the name of the website or service: ")
    entered_username = input("Enter the username: ")
    entered_password = input("Enter the password: ")

    # Provided password passed through encryption
    entered_hashed_password = hash_password(entered_password)
    if website in passwords:
        if entered_hashed_password == passwords[website]['password']:
            print("Correct password! Login successful.")
        else:
            print("Incorrect username or password!")


def main():
    while True:
        print("\nOptions:")
        print("1. Store password")
        print("2. Recover password")
        print("3. Sign in")
        print("4. Sign out")

        choice = input("Choose an option: ")

        if choice == "1":
            store_password()
        elif choice == "2":
            retrieve_password()
        elif choice == "3":
            verify_password()
        elif choice == "4":
            print("Exiting the password manager.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

