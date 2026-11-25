from task import tasks, current_time
from storage import save_tasks


# Employee updates the status of a task assigned to their email.
def update_task(email):

    print("\n--- UPDATE MY TASK ---")

    try:
        entered_id = int(input("Task ID: "))
    except ValueError:
        print("Please enter a valid Task ID.")
        return

    for task in tasks:
        if task["ID"] == entered_id and task["Assigned To"].lower() == email.lower():

            if task["Status"] == "Completed":
                print("This task is already completed.")
                return

            if task["Status"] == "Review":
                print("This task is waiting for the owner's review.")
                return

            print("\n1. To Do")
            print("2. In Progress")
            print("3. Blocker")
            print("4. Review")

            choice = input("Choose Status: ")

            if choice == "1":
                status = "To Do"
            elif choice == "2":
                status = "In Progress"
            elif choice == "3":
                status = "Blocker"
            elif choice == "4":
                status = "Review"
            else:
                print("Invalid choice.")
                return

            if status == "Review" and task["Status"] != "In Progress":
                print("Start the task before submitting it for review.")
                return

            if status == "Blocker":
                reason = input("What is blocking your work? ").strip()

                if reason == "":
                    print("Please explain the blocker.")
                    return

                task["Blocker"] = reason
                task["History"].append(
                    current_time() + " - Blocker reported: " + reason
                )
            else:
                if task["Status"] == "Blocker":
                    task["History"].append(current_time() + " - Blocker cleared")

                task["Blocker"] = ""

            task["Status"] = status

            if status == "Review":
                task["Review Note"] = ""

            task["History"].append(
                current_time() + " - Status changed to " + status
            )

            save_tasks(tasks)
            print("\nTask status updated to:", status)
            return

    print("\nTask not found or not assigned to you.")
