"""Vaayum Space web application."""

import csv
import hmac
import os
import sys

from datetime import date, datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)


# --------------------------------
# CONNECT EXISTING BACKEND
# --------------------------------

BASE = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(
    0,
    os.path.join(BASE, "backend")
)

from accounts import (
    accounts,
    find_account,
    protect_password,
    save_new_account
)

from storage import save_tasks

from task import (
    add_task,
    current_time,
    tasks
)

import sprint


# --------------------------------
# FLASK APPLICATION
# --------------------------------

app = Flask(__name__)

app.secret_key = os.environ.get(
    "VAAYUM_SECRET_KEY",
    "vaayum-local-demo-only-change-me"
)


STATUSES = [
    "To Do",
    "In Progress",
    "Blocker",
    "Review",
    "Completed"
]


# =================================
# CURRENT LOGGED-IN USER
# =================================

def signed_in_user():

    email = session.get("email", "")

    account = find_account(email)

    if account and account["Role"] == session.get("role"):

        return account

    return None


# =================================
# REDIRECT TO CORRECT DASHBOARD
# =================================

def send_home(account, section="overview"):

    if account["Role"] == "Owner":

        return redirect(
            url_for("owner", section=section)
        )

    return redirect(
        url_for("employee", section=section)
    )


# =================================
# FIND TASK
# =================================

def find_task(task_id):

    for item in tasks:

        if str(item["ID"]) == str(task_id):

            return item

    return None


# =================================
# FIND SPRINT
# =================================

def find_sprint(sprint_id):

    for item in sprint.sprints:

        if str(item["ID"]) == str(sprint_id):

            return item

    return None


# =================================
# FIND TASK'S SPRINT
# =================================

def sprint_name(task_id):

    for link in sprint.sprint_tasks:

        if str(link["Task ID"]) == str(task_id):

            item = find_sprint(
                link["Sprint ID"]
            )

            if item:
                return item["Name"]

    return ""


# =================================
# PREPARE TASK FOR DISPLAY
# =================================

def display_task(task):

    # Copy the task to avoid changing CSV columns.
    item = task.copy()

    member = find_account(
        task["Assigned To"]
    )

    if member:

        item["Person"] = member["Name"]

    else:

        item["Person"] = "Unassigned"

    item["Sprint"] = sprint_name(
        task["ID"]
    )

    # Check deadline.
    try:

        due = datetime.strptime(
            task["Deadline"],
            "%d-%m-%Y"
        ).date()

        item["Overdue"] = (
            due < date.today()
            and task["Status"] != "Completed"
        )

    except ValueError:

        item["Overdue"] = False

    return item


# =================================
# TASK STATISTICS
# =================================

def statistics(selected):

    counts = {}

    for status in STATUSES:

        counts[status] = 0

    for item in selected:

        if item["Status"] in counts:

            counts[item["Status"]] += 1

    total = len(selected)

    if total:

        percent = round(
            counts["Completed"] * 100 / total
        )

    else:

        percent = 0

    widths = {}

    for status in STATUSES:

        if total:

            widths[status] = round(
                counts[status] * 100 / total
            )

        else:

            widths[status] = 0

    return counts, percent, widths


# =================================
# MONTHLY COMPLETED TASKS
# =================================

def this_month(selected):

    count = 0

    for item in selected:

        if item["Status"] != "Completed":

            continue

        for entry in item["History"]:

            if "task approved and completed" in entry.lower():

                try:

                    finished = datetime.strptime(
                        entry[:16],
                        "%d-%m-%Y %H:%M"
                    ).date()

                    if (
                        finished.year == date.today().year
                        and finished.month == date.today().month
                    ):

                        count += 1

                except ValueError:

                    pass

                break

    return count


# =================================
# SPRINT DETAILS
# =================================

def sprint_cards(selected, hide_empty=False):

    result = []

    for source in sprint.sprints:

        card = source.copy()

        related_ids = set()

        for link in sprint.sprint_tasks:

            if str(link["Sprint ID"]) == str(source["ID"]):

                related_ids.add(
                    str(link["Task ID"])
                )

        matching = []

        for item in selected:

            if str(item["ID"]) in related_ids:

                matching.append(item)

        # Employees see only relevant sprints.
        if hide_empty and not matching:

            continue

        card["Active"] = []

        card["Completed"] = []

        for item in matching:

            if item["Status"] == "Completed":

                card["Completed"].append(item)

            else:

                card["Active"].append(item)

        if matching:

            card["Progress"] = round(
                len(card["Completed"]) * 100 / len(matching)
            )

        else:

            card["Progress"] = 0

        result.append(card)

    return result


# =================================
# SAVE TASK TO SPRINT
# =================================

def save_sprint_assignment(task_id, sprint_id):

    found = False

    for link in sprint.sprint_tasks:

        if str(link["Task ID"]) == str(task_id):

            link["Sprint ID"] = str(sprint_id)

            found = True
            break

    if not found:

        sprint.sprint_tasks.append({
            "Task ID": str(task_id),
            "Sprint ID": str(sprint_id)
        })

    with open(
        sprint.sprint_task_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["Task ID", "Sprint ID"]
        )

        writer.writeheader()

        writer.writerows(
            sprint.sprint_tasks
        )


# =================================
# LOGIN
# =================================

@app.route("/", methods=["GET", "POST"])
def login():

    user = signed_in_user()

    if user:

        return send_home(user)

    if request.method == "POST":

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        role = request.form.get(
            "role", ""
        )

        account = find_account(email)

        if account and account["Role"] == role:

            entered = protect_password(
                password,
                account["Salt"]
            )

            if hmac.compare_digest(
                entered,
                account["Password Hash"]
            ):

                session.clear()

                session["email"] = email

                session["role"] = role

                return send_home(account)

        flash(
            "Incorrect email, password, or account type.",
            "error"
        )

    return render_template(
        "login.html"
    )


# =================================
# LOGOUT
# =================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =================================
# OWNER DASHBOARD
# =================================

@app.route("/owner")
def owner():

    user = signed_in_user()

    if not user:

        return redirect(url_for("login"))

    if user["Role"] != "Owner":

        return send_home(user)

    section = request.args.get(
        "section",
        "overview"
    )

    allowed_sections = [
        "overview",
        "employees",
        "tasks",
        "reviews",
        "sprints",
        "history"
    ]

    if section not in allowed_sections:

        section = "overview"

    # All tasks.
    all_tasks = []

    for item in tasks:

        all_tasks.append(
            display_task(item)
        )

    # Employee task filtering.
    employee_filter = request.args.get(
        "person", ""
    ).strip().lower()

    shown_tasks = []

    for item in all_tasks:

        if (
            not employee_filter
            or item["Assigned To"].lower() == employee_filter
        ):

            shown_tasks.append(item)

    counts, progress, widths = statistics(
        all_tasks
    )

    shown_counts = statistics(
        shown_tasks
    )[0]

    # Employee information.
    employees = []

    for account in accounts:

        if account["Role"] != "Employee":

            continue

        member = account.copy()

        assigned = []

        for item in all_tasks:

            if item["Assigned To"].lower() == account["Email"].lower():

                assigned.append(item)

        member["Total"] = len(assigned)

        member["Completed"] = sum(
            item["Status"] == "Completed"
            for item in assigned
        )

        member["Progress"] = statistics(
            assigned
        )[1]

        member["Monthly"] = this_month(
            assigned
        )

        employees.append(member)

    # Reviews and blockers.
    reviews = []

    blockers = []

    for item in all_tasks:

        if item["Status"] == "Review":

            reviews.append(item)

        if item["Status"] == "Blocker":

            blockers.append(item)

    return render_template(
        "owner_dashboard.html",

        user=user,
        role="Owner",
        section=section,

        employees=employees,

        tasks=shown_tasks,
        all_tasks=all_tasks,

        counts=counts,
        shown_counts=shown_counts,

        widths=widths,
        progress=progress,

        statuses=STATUSES,

        reviews=reviews,
        blockers=blockers,

        sprints=sprint_cards(all_tasks),

        employee_filter=employee_filter,

        today=date.today().strftime("%d %b %Y"),
        month=date.today().strftime("%B %Y")
    )


# =================================
# EMPLOYEE DASHBOARD
# =================================

@app.route("/employee")
def employee():

    user = signed_in_user()

    if not user:

        return redirect(url_for("login"))

    if user["Role"] != "Employee":

        return send_home(user)

    section = request.args.get(
        "section",
        "overview"
    )

    if section not in [
        "overview",
        "tasks",
        "sprints"
    ]:

        section = "overview"

    # Board or List.
    view = request.args.get(
        "view",
        "board"
    )

    if view not in ["board", "list"]:

        view = "board"

    # Only tasks assigned to this employee.
    mine = []

    for item in tasks:

        if item["Assigned To"].lower() == user["Email"].lower():

            mine.append(
                display_task(item)
            )

    counts, progress, widths = statistics(
        mine
    )

    return render_template(
        "employee_dashboard.html",

        user=user,
        role="Employee",
        section=section,
        view=view,

        tasks=mine,

        counts=counts,
        progress=progress,
        widths=widths,

        statuses=STATUSES,

        sprints=sprint_cards(
            mine,
            hide_empty=True
        ),

        today=date.today().strftime("%d %b %Y")
    )


# =================================
# OWNER - ADD EMPLOYEE
# =================================

@app.route("/employees/add", methods=["POST"])
def add_employee():

    user = signed_in_user()

    if not user or user["Role"] != "Owner":

        return redirect(url_for("login"))

    name = request.form.get(
        "name", ""
    ).strip()

    email = request.form.get(
        "email", ""
    ).strip().lower()

    designation = request.form.get(
        "designation", ""
    ).strip()

    password = request.form.get(
        "password", ""
    )

    if (
        not name
        or "@" not in email
        or not designation
        or len(password) < 8
    ):

        flash(
            "Enter a name, valid email, designation and 8-character password.",
            "error"
        )

    elif find_account(email):

        flash(
            "This email is already registered.",
            "error"
        )

    else:

        save_new_account(
            name,
            email,
            designation,
            "Employee",
            password
        )

        flash(
            "Employee added successfully.",
            "success"
        )

    return send_home(
        user,
        "employees"
    )


# =================================
# OWNER - CREATE TASK
# =================================

@app.route("/tasks/create", methods=["POST"])
def create_task():

    user = signed_in_user()

    if not user or user["Role"] != "Owner":

        return redirect(url_for("login"))

    title = request.form.get(
        "title", ""
    ).strip()

    description = request.form.get(
        "description", ""
    ).strip()

    email = request.form.get(
        "employee", ""
    ).strip().lower()

    sprint_id = request.form.get(
        "sprint_id", ""
    )

    try:

        due = datetime.strptime(
            request.form.get("deadline", ""),
            "%Y-%m-%d"
        ).date()

    except ValueError:

        flash(
            "Select a valid deadline.",
            "error"
        )

        return send_home(
            user,
            "tasks"
        )

    member = find_account(email) if email else None

    if (
        not title
        or not description
        or due < date.today()
    ):

        flash(
            "Add a title, description and valid deadline.",
            "error"
        )

    elif email and (
        not member
        or member["Role"] != "Employee"
    ):

        flash(
            "Select a registered employee.",
            "error"
        )

    elif sprint_id and not find_sprint(sprint_id):

        flash(
            "Select a valid sprint.",
            "error"
        )

    else:

        add_task(
            title,
            description,
            due.strftime("%d-%m-%Y")
        )

        new_task = tasks[-1]

        if member:

            new_task["Assigned To"] = email

            new_task["History"].append(
                current_time()
                + " - Assigned to "
                + member["Name"]
            )

            save_tasks(tasks)

        if sprint_id:

            save_sprint_assignment(
                new_task["ID"],
                sprint_id
            )

        flash(
            "Task created successfully.",
            "success"
        )

    return send_home(
        user,
        "tasks"
    )


# =================================
# OWNER - ASSIGN TASK
# =================================

@app.route("/tasks/assign", methods=["POST"])
def assign_task():

    user = signed_in_user()

    if not user or user["Role"] != "Owner":

        return redirect(url_for("login"))

    item = find_task(
        request.form.get("task_id", "")
    )

    email = request.form.get(
        "employee", ""
    ).strip().lower()

    member = find_account(email)

    if (
        not item
        or not member
        or member["Role"] != "Employee"
    ):

        flash(
            "Select a task and registered employee.",
            "error"
        )

    elif item["Status"] in [
        "Review",
        "Completed"
    ]:

        flash(
            "Tasks in Review or Completed cannot be reassigned.",
            "error"
        )

    else:

        if item["Assigned To"].lower() != email:

            item["Status"] = "To Do"

            item["Blocker"] = ""

            item["Review Note"] = ""

        item["Assigned To"] = email

        item["History"].append(
            current_time()
            + " - Assigned to "
            + member["Name"]
        )

        save_tasks(tasks)

        flash(
            "Task assigned.",
            "success"
        )

    return send_home(
        user,
        "tasks"
    )


# =================================
# OWNER - REVIEW TASK
# =================================

@app.route("/tasks/review", methods=["POST"])
def review_task():

    user = signed_in_user()

    if not user or user["Role"] != "Owner":

        return redirect(url_for("login"))

    item = find_task(
        request.form.get("task_id", "")
    )

    action = request.form.get(
        "action", ""
    )

    feedback = request.form.get(
        "feedback", ""
    ).strip()

    if not item or item["Status"] != "Review":

        flash(
            "Task is not awaiting review.",
            "error"
        )

    elif action == "approve":

        item["Status"] = "Completed"

        item["Review Note"] = "Approved"

        item["History"].append(
            current_time()
            + " - Task approved and completed"
        )

        save_tasks(tasks)

        flash(
            "Task approved and moved to completed history.",
            "success"
        )

    elif action == "changes" and feedback:

        item["Status"] = "In Progress"

        item["Review Note"] = feedback

        item["History"].append(
            current_time()
            + " - Changes requested: "
            + feedback
        )

        save_tasks(tasks)

        flash(
            "Feedback sent to employee.",
            "success"
        )

    else:

        flash(
            "Enter feedback to request changes.",
            "error"
        )

    return send_home(
        user,
        "reviews"
    )


# =================================
# OWNER - CREATE SPRINT
# =================================

@app.route("/sprints/create", methods=["POST"])
def create_sprint():

    user = signed_in_user()

    if not user or user["Role"] != "Owner":

        return redirect(url_for("login"))

    name = request.form.get(
        "name", ""
    ).strip()

    try:

        start = datetime.strptime(
            request.form.get("start", ""),
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            request.form.get("end", ""),
            "%Y-%m-%d"
        ).date()

    except ValueError:

        flash(
            "Select valid start and end dates.",
            "error"
        )

        return send_home(
            user,
            "sprints"
        )

    if not name or end < start:

        flash(
            "Enter a sprint name and valid date range.",
            "error"
        )

    elif any(
        item["Name"].lower() == name.lower()
        for item in sprint.sprints
    ):

        flash(
            "This sprint already exists.",
            "error"
        )

    else:

        next_id = max(
            [int(item["ID"]) for item in sprint.sprints]
            + [0]
        ) + 1

        new_sprint = {
            "ID": str(next_id),
            "Name": name,
            "Start Date": start.strftime("%d-%m-%Y"),
            "End Date": end.strftime("%d-%m-%Y")
        }

        with open(
            sprint.sprint_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                list(new_sprint.values())
            )

        sprint.sprints.append(
            new_sprint
        )

        flash(
            "Sprint created.",
            "success"
        )

    return send_home(
        user,
        "sprints"
    )


# =================================
# OWNER - ADD TASK TO SPRINT
# =================================

@app.route("/sprints/assign", methods=["POST"])
def assign_sprint():

    user = signed_in_user()

    if not user or user["Role"] != "Owner":

        return redirect(url_for("login"))

    task_id = request.form.get(
        "task_id", ""
    )

    sprint_id = request.form.get(
        "sprint_id", ""
    )

    item = find_task(task_id)

    if not item or not find_sprint(sprint_id):

        flash(
            "Select a valid task and sprint.",
            "error"
        )

    elif item["Status"] == "Completed":

        flash(
            "Completed tasks remain in their existing history.",
            "error"
        )

    else:

        save_sprint_assignment(
            task_id,
            sprint_id
        )

        flash(
            "Task added to sprint.",
            "success"
        )

    return send_home(
        user,
        "sprints"
    )


# =================================
# EMPLOYEE - UPDATE STATUS
# =================================

@app.route("/tasks/status", methods=["POST"])
def update_status():

    user = signed_in_user()

    if not user or user["Role"] != "Employee":

        return redirect(url_for("login"))

    item = find_task(
        request.form.get("task_id", "")
    )

    new_status = request.form.get(
        "status", ""
    )

    blocker = request.form.get(
        "blocker", ""
    ).strip()

    # Employee can only update assigned tasks.
    if (
        not item
        or item["Assigned To"].lower() != user["Email"].lower()
    ):

        flash(
            "This task is not assigned to you.",
            "error"
        )

    elif item["Status"] in [
        "Review",
        "Completed"
    ]:

        flash(
            "This task is locked until owner review.",
            "error"
        )

    elif new_status not in [
        "To Do",
        "In Progress",
        "Blocker",
        "Review"
    ]:

        flash(
            "Select a valid status.",
            "error"
        )

    elif (
        new_status == "Review"
        and item["Status"] != "In Progress"
    ):

        flash(
            "Move the task to In Progress before Review.",
            "error"
        )

    elif new_status == "Blocker" and not blocker:

        flash(
            "Enter a blocker reason.",
            "error"
        )

    else:

        if new_status == "Blocker":

            item["Blocker"] = blocker

            item["History"].append(
                current_time()
                + " - Blocker reported: "
                + blocker
            )

        else:

            if item["Status"] == "Blocker":

                item["History"].append(
                    current_time()
                    + " - Blocker cleared"
                )

            item["Blocker"] = ""

        item["Status"] = new_status

        if new_status == "Review":

            item["Review Note"] = ""

        item["History"].append(
            current_time()
            + " - Status changed to "
            + new_status 
        )

        save_tasks(tasks)

        flash(
            "Task moved to " + new_status + ".",
            "success"
        )

    return send_home(
        user,
        "tasks"
    )


# =================================
# START WEBSITE
# =================================

if __name__ == "__main__":

    app.run(debug=True)