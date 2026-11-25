import datetime

from task import tasks
from accounts import accounts, find_account


# Print one task in a readable format.
def show_task(task):

    print("\n-----------------------------")
    print("Task ID:", task["ID"])
    print("Title:", task["Title"])
    print("Description:", task["Description"])
    print("Deadline:", task["Deadline"])
    print("Status:", task["Status"])

    employee = find_account(task["Assigned To"])

    if employee:
        print("Assigned To:", employee["Name"])
    else:
        print("Assigned To:", task["Assigned To"])

    if task["Blocker"] != "":
        print("Blocker:", task["Blocker"])

    if task["Review Note"] != "":
        print("Owner Feedback:", task["Review Note"])


# Owner sees tasks from the entire company.
def view_all_tasks():

    print("\n--- ALL TASKS ---")

    if len(tasks) == 0:
        print("No tasks available.")
        return

    for task in tasks:
        show_task(task)
        print("History:")

        for update in task["History"]:
            print(" -", update)


# Employee sees only tasks assigned to their own account.
def view_my_tasks(email):

    print("\n--- MY TASKS ---")
    found = False

    for task in tasks:
        if task["Assigned To"].lower() == email.lower():
            show_task(task)
            found = True

    if not found:
        print("No tasks assigned to you.")


# Owner can inspect all tasks for any one employee.
def view_employee_tasks():

    print("\n--- EMPLOYEE TASKS ---")
    email = input("Employee Email: ").strip().lower()
    account = find_account(email)

    if account is None or account["Role"] != "Employee":
        print("Employee not found.")
        return

    print("Employee:", account["Name"])
    view_my_tasks(email)
    show_progress(email)


# Display simple status counts for an employee or the whole team.
def show_progress(email=None):

    selected_tasks = []

    for task in tasks:
        if email is None or task["Assigned To"].lower() == email.lower():
            selected_tasks.append(task)

    print("\n--- TASK PROGRESS ---")
    print("Total Tasks:", len(selected_tasks))

    statuses = ["To Do", "In Progress", "Blocker", "Review", "Completed"]

    for status in statuses:
        count = 0

        for task in selected_tasks:
            if task["Status"] == status:
                count = count + 1

        print(status + ":", count)

    # Calculate completion using task counts.
    if len(selected_tasks) > 0:
        completed = 0

        for task in selected_tasks:
            if task["Status"] == "Completed":
                completed = completed + 1

        percentage = round(completed / len(selected_tasks) * 100)
        print("Completion:", str(percentage) + "%")


# Owner sees a basic overview for the company.
def team_overview():

    print("\n======== TEAM OVERVIEW ========")

    employee_count = 0

    for account in accounts:
        if account["Role"] == "Employee":
            employee_count = employee_count + 1

    print("Employees:", employee_count)
    show_progress()

    overdue = 0

    for task in tasks:
        if task["Status"] != "Completed":
            due_date = datetime.datetime.strptime(task["Deadline"], "%d-%m-%Y").date()

            if due_date < datetime.date.today():
                overdue = overdue + 1

    print("Overdue Tasks:", overdue)


# Owner sees tasks that are currently blocked.
def view_blockers():

    print("\n--- BLOCKED TASKS ---")
    found = False

    for task in tasks:
        if task["Status"] == "Blocker":
            show_task(task)
            found = True

    if not found:
        print("No blocked tasks.")
