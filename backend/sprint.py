import csv
import os
from datetime import datetime

from task import tasks


# Find our main project folder
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Find the storage folder
data_folder = os.path.join(project_folder, "storage")


# CSV file locations
sprint_file = os.path.join(data_folder, "sprints.csv")
sprint_task_file = os.path.join(data_folder, "sprint_tasks.csv")


# Create sprint CSV file if it does not exist
if not os.path.exists(sprint_file) or os.path.getsize(sprint_file) == 0:

    with open(sprint_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["ID", "Name", "Start Date", "End Date"])


# Create sprint-task CSV file if it does not exist
if not os.path.exists(sprint_task_file) or os.path.getsize(sprint_task_file) == 0:

    with open(sprint_task_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Task ID", "Sprint ID"])


# Load previously saved sprints
sprints = []

with open(sprint_file, "r", newline="") as file:

    reader = csv.DictReader(file)

    for sprint in reader:

        sprints.append(sprint)


# Load previously saved sprint assignments
sprint_tasks = []

with open(sprint_task_file, "r", newline="") as file:

    reader = csv.DictReader(file)

    for item in reader:

        sprint_tasks.append(item)


# --------------------------------
# CREATE SPRINT
# --------------------------------

def create_sprint():

    print("\n--- CREATE SPRINT ---")

    name = input("Sprint Name: ").strip()
    start_date = input("Start Date (DD-MM-YYYY): ").strip()
    end_date = input("End Date (DD-MM-YYYY): ").strip()

    if name == "":

        print("Sprint name cannot be empty.")
        return

    # Check sprint dates
    try:

        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")

    except ValueError:

        print("Invalid date format.")
        return

    if end < start:

        print("End date cannot be before start date.")
        return

    # Check for duplicate sprint names
    for sprint in sprints:

        if sprint["Name"].lower() == name.lower():

            print("Sprint already exists.")
            return

    # Generate new Sprint ID
    sprint_id = 1

    for sprint in sprints:

        if int(sprint["ID"]) >= sprint_id:

            sprint_id = int(sprint["ID"]) + 1

    # Create sprint information
    new_sprint = {
        "ID": str(sprint_id),
        "Name": name,
        "Start Date": start_date,
        "End Date": end_date
    }

    # Add sprint to the list
    sprints.append(new_sprint)

    # Save sprint permanently
    with open(sprint_file, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            sprint_id,
            name,
            start_date,
            end_date
        ])

    print("\nSprint created successfully!")
    print("Sprint ID:", sprint_id)


# --------------------------------
# ASSIGN TASK TO SPRINT
# --------------------------------

def assign_task_to_sprint():

    print("\n--- ASSIGN TASK TO SPRINT ---")

    sprint_id = input("Enter Sprint ID: ").strip()
    task_id = input("Enter Task ID: ").strip()

    # Check whether sprint exists
    sprint_found = False

    for sprint in sprints:

        if sprint["ID"] == sprint_id:

            sprint_found = True
            break

    if not sprint_found:

        print("Sprint not found.")
        return

    # Check whether task exists
    task_found = False

    for task in tasks:

        if str(task["ID"]) == task_id:

            task_found = True
            break

    if not task_found:

        print("Task not found.")
        return

    # Check whether task already belongs to a sprint
    already_assigned = False

    for item in sprint_tasks:

        if item["Task ID"] == task_id:

            item["Sprint ID"] = sprint_id

            already_assigned = True
            break

    # Create a new sprint assignment
    if not already_assigned:

        sprint_tasks.append({
            "Task ID": task_id,
            "Sprint ID": sprint_id
        })

    # Save sprint assignments
    with open(sprint_task_file, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["Task ID", "Sprint ID"]
        )

        writer.writeheader()

        writer.writerows(sprint_tasks)

    print("\nTask assigned to sprint successfully!")


# --------------------------------
# VIEW SPRINTS AND TASKS
# --------------------------------

def view_sprints(employee_email=""):

    print("\n--- SPRINTS ---")

    if len(sprints) == 0:

        print("No sprints available.")
        return

    # Display all sprints
    for sprint in sprints:

        print("\n-----------------------------")

        print("Sprint ID:", sprint["ID"])
        print("Name:", sprint["Name"])
        print("Start Date:", sprint["Start Date"])
        print("End Date:", sprint["End Date"])

        print("\nTasks:")

        found = False

        # Find tasks belonging to this sprint
        for item in sprint_tasks:

            if item["Sprint ID"] == sprint["ID"]:

                for task in tasks:

                    if str(task["ID"]) == item["Task ID"]:

                        # Employees see only their own tasks
                        if employee_email != "":

                            if task["Assigned To"].lower() != employee_email.lower():

                                continue

                        print("\nTask ID:", task["ID"])
                        print("Title:", task["Title"])
                        print("Status:", task["Status"])

                        found = True

        if not found:

            print("No tasks available.")