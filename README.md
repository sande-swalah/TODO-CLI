# TODO List App

A simple command-line task management application built with Python.

## Features

- **Create Users**: Simple user accounts (just username)
- **Add Tasks**: Create tasks to track
- **Mark Complete/Incomplete**: Show task completion status
- **View Tasks**: See all your tasks in a table
- **Delete Tasks**: Remove tasks you don't need

## Installation

### Requirements
- Python 3.10 or higher

### Setup

```bash
cd todo_cli
python3 main.py
```

No other dependencies needed! Uses only Python standard library.

## Usage

Run the app:
```bash
python3 main.py
```

### First Time
1. Select "Create New User"
2. Enter a username
3. Login with that username
4. Start adding tasks!

### Menu Options

**When Not Logged In:**
- 1: Login with existing username
- 2: Create new user account
- 3: Exit

**When Logged In:**
- 1: Add new task
- 2: View all your tasks
- 3: Mark a task as complete
- 4: Mark a task as incomplete
- 5: Delete a task
- 6: Logout
- 7: Exit

## Example

```
✓ TODO List App Started

==================================================
TODO LIST APP
==================================================

1. Login
2. Create New User
3. Exit
==================================================

Select option: 2

Enter username: alice

✓ User 'alice' created!

==================================================
TODO LIST APP
==================================================
Logged in as: alice

1. Add Task
2. View My Tasks
3. Mark Task Complete
4. Mark Task Incomplete
5. Delete Task
6. Logout
7. Exit
==================================================

Select option: 1

Enter task title: Learn Python

✓ Task added! (ID: a1b2c3d4)
```

## Data Storage

- Tasks stored in: `data/tasks.json`
- Users stored in: `data/users.json`
- Automatically created on first run

## Simple Design

- **Task**: title, completion status (yes/no)
- **User**: username only, no passwords
- **Storage**: JSON files, no database needed

## Code Structure

```
todo_cli/
├── main.py           # Interactive menu
├── models/
│   ├── task.py       # Task class
│   └── user.py       # User class
├── utils/
│   └── auth.py       # Login/logout
├── data/
│   ├── tasks.json    # Stored tasks
│   └── users.json    # Stored users
└── README.md         # This file
```

## How It Works

1. **Create a user** - Just enter a username
2. **Login** - Enter your username
3. **Add tasks** - Type task title
4. **Mark complete** - Enter task ID to mark done
5. **View tasks** - See all tasks with status
6. **Delete** - Remove tasks you don't need

## Beginner-Friendly

- No passwords to worry about
- Simple menu interface
- Clear status indicators (✓ Complete, ✗ Not Complete)
- Easy to understand code structure
