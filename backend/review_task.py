from task import tasks, current_time
from storage import save_tasks


# Owner approves a submitted task or sends it back for changes.
def review_task():

    print("\n--- REVIEW SUBMITTED TASKS ---")

    submitted = 0

    for task in tasks:
        if task["Status"] == "Review":
            print("Task", task["ID"], "-", task["Title"])
            submitted = submitted + 1

    if submitted == 0:
        print("No tasks waiting for review.")
        return

    try:
        entered_id = int(input("\nEnter Task ID to Review: "))
    except ValueError:
        print("Please enter a valid Task ID.")
        return

    for task in tasks:
        if task["ID"] == entered_id:

            if task["Status"] != "Review":
                print("This task is not submitted for review.")
                return

            print("\nTask:", task["Title"])
            print("1. Approve Task")
            print("2. Request Changes")

            choice = input("Enter Choice: ")

            if choice == "1":
                task["Status"] = "Completed"
                task["Review Note"] = "Approved"
                message = "Task approved and completed"

            elif choice == "2":
                feedback = input("Enter Feedback: ").strip()

                if feedback == "":
                    print("Please enter feedback for the employee.")
                    return

                task["Status"] = "In Progress"
                task["Review Note"] = feedback
                message = "Changes requested: " + feedback

            else:
                print("Invalid choice.")
                return

            task["History"].append(current_time() + " - " + message)
            save_tasks(tasks)

            print("\n" + message)
            return

    print("\nTask ID not found.")
