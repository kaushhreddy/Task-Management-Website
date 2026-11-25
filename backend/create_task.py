import datetime

from task import add_task


# Owner enters task details and a deadline.
def create_task():

    print("\n--- CREATE TASK ---")

    title = input("Task Title: ").strip()
    description = input("Description: ").strip()
    deadline = input("Deadline (DD-MM-YYYY): ").strip()

    if title == "" or description == "":
        print("Title and description cannot be empty.")
        return

    # Check that the entered date is a real date.
    try:
        due_date = datetime.datetime.strptime(deadline, "%d-%m-%Y").date()
    except ValueError:
        print("Invalid date. Use DD-MM-YYYY.")
        return

    if due_date < datetime.date.today():
        print("The deadline cannot be in the past.")
        return

    add_task(title, description, deadline)
