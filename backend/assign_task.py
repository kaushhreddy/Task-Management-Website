from task import tasks, current_time
from accounts import find_account
from storage import save_tasks


# Owner assigns a task to an employee's registered email.
def assign_task():

    print("\n--- ASSIGN TASK ---")

    try:
        entered_id = int(input("Task ID: "))
    except ValueError:
        print("Please enter a valid Task ID.")
        return

    email = input("Employee Email: ").strip().lower()
    employee = find_account(email)

    if employee is None or employee["Role"] != "Employee":
        print("Employee not found. Add the employee first.")
        return

    for task in tasks:
        if task["ID"] == entered_id:

            if task["Status"] == "Review" or task["Status"] == "Completed":
                print("You cannot reassign a task in Review or Completed.")
                return

            # Restart the assignment at To Do if the employee changes.
            if task["Assigned To"] != email:
                task["Status"] = "To Do"
                task["Blocker"] = ""
                task["Review Note"] = ""

            task["Assigned To"] = email
            task["History"].append(
                current_time() + " - Assigned to " + employee["Name"]
            )

            save_tasks(tasks)
            print("\nTask assigned to", employee["Name"])
            return

    print("\nTask ID not found.")
