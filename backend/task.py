import datetime

from storage import load_tasks, save_tasks

# Load all tasks when the program starts.
tasks = load_tasks()

# New task IDs start from 1001, just like Helpdesk ticket IDs.
task_id = 1001

for task in tasks:
    if task["ID"] >= task_id:
        task_id = task["ID"] + 1


# Return the current date and time as simple text.
def current_time():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M")


# Create and save a new task.
def add_task(title, description, deadline):

    global task_id

    task = {
        "ID": task_id,
        "Title": title,
        "Description": description,
        "Deadline": deadline,
        "Assigned To": "Unassigned",
        "Status": "To Do",
        "Blocker": "",
        "Review Note": "",
        "History": [current_time() + " - Task created"]
    }

    tasks.append(task)
    save_tasks(tasks)

    print("\nTask created successfully!")
    print("Task ID:", task_id)

    task_id = task_id + 1
