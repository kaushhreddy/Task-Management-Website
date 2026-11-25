# TASK MANAGEMENT WEBSITE

A web-based **Task Management System** developed using Python, Flask, HTML, CSS, and JavaScript. The application provides a centralized workspace for managing employees, assigning tasks, tracking work status, organizing sprints, and reviewing completed tasks.

The project features a professional dark-themed interface with separate dashboards for Owners and Employees.

## Project Overview

The Task Management System is designed to simplify task coordination and work tracking within a team.

Owners can create and assign tasks, manage employees, set deadlines, organize sprints, and review submitted work. Employees can view their assigned tasks, update their progress, report blockers, and submit tasks for approval.

The system maintains task records and activity history using CSV files for persistent storage.

## Key Features

### 1. Role-Based Authentication
- Separate login options for Owners and Employees.
- Email and password authentication.
- Passwords stored using secure hashing.
- Session-based login and logout.
- Role-based dashboard access.

### 2. Owner Dashboard
- Workspace overview with task and employee statistics.
- View registered employees and their designations.
- Create and assign tasks to employees.
- Set task descriptions and deadlines.
- Create and manage sprints.
- Monitor task statuses.
- Review employee submissions.
- Approve completed tasks or request changes.
- View reported blockers.
- Access task history and recent activity.

### 3. Employee Dashboard
- Personalized workspace for each employee.
- View individually assigned tasks.
- Track task deadlines and sprint assignments.
- Update task status.
- Drag and drop task cards between status columns.
- Report blockers with reasons.
- Submit completed work for owner review.
- View review feedback.
- Access task history.

### 4. Task Management

Tasks move through the following workflow:

**To Do → In Progress → Review → Completed**

Employees can also move a task into **Blocker** when they encounter an issue.

Only the Owner can approve tasks and mark them as Completed.

### 5. Sprint Management
- Create sprints with start and end dates.
- Assign tasks to sprints.
- View active sprint tasks.
- Track completed sprint tasks.
- Maintain completed task records.

### 6. Task History
- Records task creation and assignments.
- Tracks status changes.
- Maintains blocker information.
- Stores review feedback and approvals.
- Provides task-specific activity history.

### 7. User Interface
- Professional dark-themed design.
- Responsive dashboard layout.
- Clean navigation and readable typography.
- Task board and list views.
- Interactive task cards.
- Search and filtering options.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML5 | Webpage structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactions |
| CSV | Data storage |
| Git | Version control |
| GitHub | Source code hosting |

## Project Structure

```text
Vaayum_Space/
│
├── app.py
├── README.md
├── .gitignore
│
├── backend/
│   ├── accounts.py
│   ├── assign_task.py
│   ├── create_task.py
│   ├── main.py
│   ├── review_task.py
│   ├── sprint.py
│   ├── storage.py
│   ├── task.py
│   ├── update_task.py
│   └── view_tasks.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── owner_dashboard.html
│   ├── employee_dashboard.html
│   └── history_panel.html
│
├── static/
│   ├── style.css
│   ├── app.js
│   └── vaayum_logo_white.png
│
└── storage/
    └── .gitkeep
```

**Note:** Local CSV files containing employee accounts, task records, and sprint information are excluded from the public repository.

## Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/kaushhreddy/Task-Management-System.git
```

### Step 2: Open the project folder

```bash
cd Task-Management-System
```

### Step 3: Install Flask

```bash
pip install flask
```

### Step 4: Initialize local data

The application uses CSV files for storing employee accounts, tasks, and sprint information.

The required local CSV files are:

```text
storage/
├── employees.csv
├── tasks.csv
├── sprints.csv
└── sprint_tasks.csv
```

These files are not included in the public repository.

Use the backend's account and task management functions to initialize the required data and create login accounts before starting the website.

### Step 5: Run the application

```bash
python app.py
```

### Step 6: Open the website

Visit:

```text
http://127.0.0.1:5000
```

Sign in using a locally registered Owner or Employee account.

## Application Workflow

**Owner**

Login → Dashboard → Employees → Create Task → Assign Employee → Set Deadline / Sprint → Review Task → Approve Completion

**Employee**

Login → Dashboard → My Tasks → Update Status → Report Blocker (if required) → Submit for Review → View Feedback / Completion

## Data Storage

The project uses CSV-based storage to keep the implementation simple and beginner-friendly.

- `employees.csv` — Employee details and login credentials stored as password hashes.
- `tasks.csv` — Task details, assignments, statuses, blockers, and history.
- `sprints.csv` — Sprint information.
- `sprint_tasks.csv` — Task-to-sprint assignments.

Data remains available after the application is closed and restarted.

## Project Objectives

- Simplify task assignment and tracking.
- Provide separate workspaces for Owners and Employees.
- Improve visibility into task statuses and deadlines.
- Support sprint-based task organization.
- Maintain task history for reference.
- Build a functional web application using beginner-friendly technologies.

## Future Enhancements

Potential improvements include:

- Database integration using SQLite or MySQL.
- Individual password management.
- Email notifications for task assignments.
- File attachments for tasks.
- Task priorities and advanced filtering.
- Multiple projects and workspaces.
- Cloud deployment.
- Real-time collaboration features.

## Project Information

**Project Name:** Task Management System  
**Application Name:** Vaayum Space  
**Project Type:** Personal Demonstration Project  
**Backend:** Python, Flask  
**Frontend:** HTML, CSS, JavaScript  
**Storage:** CSV  

## Author

**Kaushik Reddy**

GitHub: [kaushhreddy](https://github.com/kaushhreddy)

---

*This project was developed for learning and demonstration purposes.*
