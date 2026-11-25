import hashlib
import os

from storage import load_accounts, save_accounts

# Keep all accounts in one list, just like tasks in our Helpdesk project.
accounts = load_accounts()


# Find an account using its email address.
def find_account(email):

    for account in accounts:
        if account["Email"].lower() == email.lower():
            return account

    return None


# Convert a password into a protected value before saving it.
# This uses Python's built-in libraries; no installation is needed.
def protect_password(password, salt):

    result = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"),
        bytes.fromhex(salt), 200000
    )

    return result.hex()


# Create an account and save it.
def save_new_account(name, email, designation, role, password):

    salt = os.urandom(16).hex()

    account = {
        "Name": name,
        "Email": email,
        "Designation": designation,
        "Role": role,
        "Salt": salt,
        "Password Hash": protect_password(password, salt)
    }

    accounts.append(account)
    save_accounts(accounts)


# The first time we run the program, create the owner account.
def setup_owner():

    for account in accounts:
        if account["Role"] == "Owner":
            return

    print("\n--- FIRST TIME SETUP: CREATE OWNER ACCOUNT ---")

    while True:
        name = input("Owner Name: ").strip()
        email = input("Owner Email: ").strip().lower()
        password = input("Choose a Password (at least 8 characters): ")

        if name == "" or "@" not in email or len(password) < 8:
            print("Enter a name, valid email and password of at least 8 characters.")
        elif find_account(email):
            print("This email is already registered.")
        else:
            break

    save_new_account(name, email, "Owner", "Owner", password)
    print("\nOwner account created! Please log in.\n")


# Login with the correct email, password and role.
def login(role):

    print("\n--- " + role.upper() + " LOGIN ---")

    email = input("Email: ").strip().lower()
    password = input("Password: ")

    account = find_account(email)

    if account is None or account["Role"] != role:
        print("Incorrect email, password or account type.")
        return None

    entered_hash = protect_password(password, account["Salt"])

    if entered_hash != account["Password Hash"]:
        print("Incorrect email, password or account type.")
        return None

    print("\nWelcome, " + account["Name"] + "!")
    return account


# Owner registers an employee with an individual login.
def add_employee():

    print("\n--- ADD EMPLOYEE ---")

    name = input("Employee Name: ").strip()
    email = input("Employee Email: ").strip().lower()
    designation = input("Designation: ").strip()
    password = input("Create Employee Password (at least 8 characters): ")

    if name == "" or "@" not in email or designation == "":
        print("Please enter a name, email and designation.")
        return

    if len(password) < 8:
        print("Password must have at least 8 characters.")
        return

    if find_account(email):
        print("This email is already registered.")
        return

    save_new_account(name, email, designation, "Employee", password)
    print("\nEmployee added successfully!")


# Owner views all employees and their details.
def view_employees():

    print("\n--- OUR TEAM ---")
    found = False

    for account in accounts:
        if account["Role"] == "Employee":
            print("\n-----------------------------")
            print("Name:", account["Name"])
            print("Email:", account["Email"])
            print("Designation:", account["Designation"])
            found = True

    if not found:
        print("No employees added yet.")
