# VAAYUM SPACE — Simple Python Backend

This is the **backend-only**, beginner-friendly version of Vaayum Space. It follows the same modular Python style as the Helpdesk Ticket Management System.

## Run

1. Open the `Vaayum_Space` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Run `python main.py` (or `py main.py` on Windows if needed).
4. On the first run, enter the owner's name, email and a password of at least 8 characters.
5. Choose **Owner Login** and enter those same credentials.
6. As the owner, add your employees, then create and assign tasks.
7. Choose **Logout**, then **Employee Login** with an employee's email/password to work on their tasks.

No `pip install` is necessary: this project uses Python's built-in modules only.

## Workflow

- **Owner**: log in → add employees → create tasks with deadlines → assign tasks to registered employees → monitor progress and blockers → approve or request changes.
- **Employee**: log in → view only assigned tasks → change status between To Do, In Progress, Blocker and Review → see feedback → wait for owner approval before Completed.

`tasks.csv` saves task records; `employees.csv` saves owner and employee accounts. These files are created automatically if missing.

## Structure

```
Vaayum_Space/
├── main.py         # Start program, owner menu, employee menu
├── accounts.py     # Create owner account, employee accounts, logins
├── task.py         # Task list and new task IDs
├── storage.py      # Read/write two CSV files
├── create_task.py  # Create tasks and deadlines
├── assign_task.py  # Assign tasks by registered employee email
├── view_tasks.py   # Lists, blockers, team/employee progress
├── update_task.py # Employee changes task status
├── review_task.py # Owner approves or requests changes
├── tasks.csv       # Stored tasks, initially empty
└── employees.csv   # Stored accounts, initially empty
```

## Task statuses

`To Do → In Progress → Review → Completed`

An employee can choose `Blocker` when stuck, provide a reason, and move back to `In Progress` when work resumes. An owner can send a reviewed task back to `In Progress` with feedback.

## Important notes

- This is a **local, single-computer learning application**, not a production web service. It uses password hashes instead of plain-text passwords, but CSV files do not provide production-grade access controls, auditing or concurrent editing.
- **Sprints, graphs, and the browser interface are intentionally not included** because the current step is backend only.
- This version assigns work by **employee email address** instead of just a name. If you already have an older `tasks.csv`, back it up; old name-based assignments may need to be reassigned through the owner menu.
- Keep `employees.csv` private. It contains hashed passwords and account information.
- The program expects to be run from inside the `Vaayum_Space` folder.
