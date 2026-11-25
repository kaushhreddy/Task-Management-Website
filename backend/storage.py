import csv
import os


# Find our main project folder
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Find the storage folder
data_folder = os.path.join(project_folder, "storage")


# CSV file locations
task_file = os.path.join(data_folder, "tasks.csv")
account_file = os.path.join(data_folder, "employees.csv")


# Task CSV columns
task_columns = [
    "ID",
    "Title",
    "Description",
    "Deadline",
    "Assigned To",
    "Status",
    "Blocker",
    "Review Note",
    "History"
]


# Employee CSV columns
account_columns = [
    "Name",
    "Email",
    "Designation",
    "Role",
    "Salt",
    "Password Hash"
]


# Create CSV file if it does not exist
def create_file(filename, columns):

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(columns)


# Load all saved tasks
def load_tasks():

    create_file(task_file, task_columns)

    tasks = []

    with open(task_file, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for task in reader:

            task["ID"] = int(task["ID"])

            # Convert saved history into a list
            if task["History"]:

                task["History"] = task["History"].split("|")

            else:

                task["History"] = []

            tasks.append(task)

    return tasks


# Save all tasks permanently
def save_tasks(tasks):

    with open(task_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=task_columns)

        writer.writeheader()

        for task in tasks:

            saved_task = task.copy()

            saved_task["History"] = "|".join(task["History"])

            writer.writerow(saved_task)


# Load owner and employee accounts
def load_accounts():

    create_file(account_file, account_columns)

    accounts = []

    with open(account_file, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for account in reader:

            accounts.append(account)

    return accounts


# Save owner and employee accounts
def save_accounts(accounts):

    with open(account_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=account_columns)

        writer.writeheader()

        writer.writerows(accounts)