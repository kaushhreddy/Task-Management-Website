from accounts import setup_owner, login, add_employee, view_employees

from create_task import create_task
from assign_task import assign_task

from view_tasks import (
    view_all_tasks,
    view_my_tasks,
    view_employee_tasks,
    show_progress,
    team_overview,
    view_blockers
)

from update_task import update_task
from review_task import review_task

from sprint import create_sprint, assign_task_to_sprint, view_sprints


# Create owner account during first-time setup
setup_owner()


# Main Application Menu
while True:

    print("\n================================")
    print("           VAAYUM SPACE")
    print("================================")

    print("1. Owner Login")
    print("2. Employee Login")
    print("3. Exit")

    role = input("\nEnter Choice: ")


    # OWNER LOGIN
    if role == "1":

        owner = login("Owner")

        if owner is None:
            continue

        while True:

            print("\n----------- OWNER MENU -----------")

            print("1. Team Progress")
            print("2. Add Employee")
            print("3. View Employees")
            print("4. Create Task")
            print("5. Assign Task")
            print("6. View All Tasks")
            print("7. View Employee Tasks")
            print("8. View Blockers")
            print("9. Review Tasks") 
            print("10. Create Sprint")
            print("11. Assign Task to Spri" \
            "nt")
            print("12. View Sprints")
            print("13. Logout")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                team_overview()

            elif choice == "2":
                add_employee()

            elif choice == "3":
                view_employees()

            elif choice == "4":
                create_task()

            elif choice == "5":
                assign_task()

            elif choice == "6":
                view_all_tasks()

            elif choice == "7":
                view_employee_tasks()

            elif choice == "8":
                view_blockers()

            elif choice == "9":
                review_task()

            elif choice == "10":
                create_sprint()

            elif choice == "11":
                assign_task_to_sprint()

            elif choice == "12":
                view_sprints()

            elif choice == "13":
                print("Owner logged out.")
                break

            else:
                print("Invalid choice.")


    # EMPLOYEE LOGIN
    elif role == "2":

        employee = login("Employee")

        if employee is None:
            continue

        while True:

            print("\n---------- EMPLOYEE MENU ----------")

            print("1. My Progress")
            print("2. View My Tasks")
            print("3. Update Task Status")
            print("4. My Sprint Tasks")
            print("5. Logout")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                show_progress(employee["Email"])

            elif choice == "2":
                view_my_tasks(employee["Email"])

            elif choice == "3":
                update_task(employee["Email"])

            elif choice == "4":
                view_sprints(employee["Email"])

            elif choice == "5":
                print("Employee logged out.")
                break

            else:
                print("Invalid choice.")


    # EXIT APPLICATION
    elif role == "3":

        print("\nThank you for using Vaayum Space!")
        break

    else:
        print("Invalid choice.")