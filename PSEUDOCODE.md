# TODO List CLI - Pseudocode

## Overview
This document explains how the TODO List CLI application works using pseudocode. The app allows users to register, login, and manage their tasks.

---

## 1. User Management (models/user.py)

### User Class
```
CLASS User:
    FUNCTION __init__(username, user_id=None, created_at=None):
        SET this._username = username
        SET this._user_id = user_id OR generate_new_id()
        SET this._created_at = created_at OR get_current_time()
    END FUNCTION
    
    PROPERTY username (getter):
        RETURN this._username
    END PROPERTY
    
    PROPERTY username (setter):
        IF username is empty THEN
            RAISE error "Username cannot be empty"
        END IF
        SET this._username = username
    END PROPERTY
    
    PROPERTY user_id (getter):
        RETURN this._user_id
    END PROPERTY
    
    PROPERTY created_at (getter):
        RETURN this._created_at
    END PROPERTY
    
    FUNCTION to_dict():
        RETURN dictionary with user_id, username, created_at
    END FUNCTION
    
    STATIC FUNCTION from_dict(data):
        CREATE new User from dictionary data
        RETURN the User object
    END FUNCTION
    
    FUNCTION __str__():
        RETURN formatted string like "User(alice, ID: abc123)"
    END FUNCTION
END CLASS
```

### UserManager Class
```
CLASS UserManager:
    CONSTANT USERS_FILE = "data/users.json"
    
    STATIC FUNCTION load_users():
        IF USERS_FILE does not exist THEN
            RETURN empty list
        END IF
        
        TRY:
            OPEN USERS_FILE for reading
            READ JSON data from file
            CLOSE file
            
            CREATE empty list of User objects
            FOR EACH user_data in JSON data DO
                CONVERT user_data to User object
                ADD User to list
            END FOR
            
            RETURN list of User objects
        CATCH error:
            RETURN empty list
        END TRY
    END FUNCTION
    
    STATIC FUNCTION save_users(users):
        IF "data" folder does not exist THEN
            CREATE "data" folder
        END IF
        
        TRY:
            CONVERT all User objects to dictionaries
            OPEN USERS_FILE for writing
            WRITE JSON data to file
            CLOSE file
            RETURN True
        CATCH error:
            RETURN False
        END TRY
    END FUNCTION
    
    STATIC FUNCTION username_exists(username_to_check):
        LOAD all users
        
        FOR EACH user in users DO
            IF user.username (lowercase) == username_to_check (lowercase) THEN
                RETURN True
            END IF
        END FOR
        
        RETURN False
    END FUNCTION
    
    STATIC FUNCTION find_user(username):
        LOAD all users
        
        FOR EACH user in users DO
            IF user.username (lowercase) == username (lowercase) THEN
                RETURN user
            END IF
        END FOR
        
        RETURN None (user not found)
    END FUNCTION
    
    STATIC FUNCTION create_user(username):
        IF username already exists THEN
            PRINT "User already exists!"
            RETURN None
        END IF
        
        CREATE new User object with username
        LOAD all existing users
        ADD new user to list
        SAVE all users to file
        PRINT "User created!"
        RETURN new user
    END FUNCTION
END CLASS
```

### Decorator
```
FUNCTION log_action(action_name):
    CREATE decorator function:
        FUNCTION decorator(func):
            CREATE wrapper function:
                FUNCTION wrapper(*args, **kwargs):
                    PRINT "[LOG] {action_name}..."
                    CALL original function
                    RETURN result
                END FUNCTION
            RETURN wrapper
        END FUNCTION
    RETURN decorator
END FUNCTION
```

---

## 2. Task Management (models/task.py)

```
FUNCTION load_all_tasks():
    IF tasks file does not exist THEN
        RETURN empty list
    END IF
    
    TRY:
        OPEN tasks file
        READ JSON data
        CLOSE file
        RETURN data
    CATCH error:
        RETURN empty list
    END TRY
END FUNCTION

FUNCTION save_all_tasks(all_tasks):
    IF "data" folder does not exist THEN
        CREATE "data" folder
    END IF
    
    TRY:
        OPEN tasks file for writing
        WRITE all_tasks as JSON
        CLOSE file
        RETURN True
    CATCH error:
        RETURN False
    END TRY
END FUNCTION

FUNCTION add_new_task(task_title, user_id):
    LOAD all tasks
    
    CREATE new task dictionary:
        task_id = generate_short_id()
        title = task_title
        user_id = user_id
        completed = False
        created_at = current_time
    
    ADD task to list
    SAVE all tasks
    RETURN new task
END FUNCTION

FUNCTION get_user_tasks(user_id):
    LOAD all tasks
    CREATE empty user_tasks list
    
    FOR EACH task in all tasks DO
        IF task.user_id == user_id THEN
            ADD task to user_tasks
        END IF
    END FOR
    
    RETURN user_tasks
END FUNCTION

FUNCTION mark_task_complete(task_id, user_id):
    LOAD all tasks
    
    FOR EACH task in all tasks DO
        IF task.task_id == task_id AND task.user_id == user_id THEN
            SET task.completed = True
            SAVE all tasks
            RETURN True
        END IF
    END FOR
    
    RETURN False (task not found)
END FUNCTION

FUNCTION mark_task_incomplete(task_id, user_id):
    LOAD all tasks
    
    FOR EACH task in all tasks DO
        IF task.task_id == task_id AND task.user_id == user_id THEN
            SET task.completed = False
            SAVE all tasks
            RETURN True
        END IF
    END FOR
    
    RETURN False (task not found)
END FUNCTION

FUNCTION delete_one_task(task_id, user_id):
    LOAD all tasks
    CREATE empty new_task_list
    SET task_found = False
    
    FOR EACH task in all tasks DO
        IF task.task_id == task_id AND task.user_id == user_id THEN
            SET task_found = True
            // Don't add to new list (delete it)
        ELSE
            ADD task to new_task_list
        END IF
    END FOR
    
    IF task_found THEN
        SAVE new_task_list
        RETURN True
    END IF
    
    RETURN False
END FUNCTION

FUNCTION show_tasks(task_list):
    IF task_list is empty THEN
        PRINT "No tasks found"
        RETURN
    END IF
    
    PRINT table header with ID, Task, Status
    
    FOR EACH task in task_list DO
        IF task.completed == True THEN
            SET status = "✓ Completed"
        ELSE
            SET status = "✗ Not Completed"
        END IF
        
        PRINT task with status
    END FOR
    
    PRINT table footer
END FUNCTION
```

---

## 3. Authentication (utils/auth.py)

```
GLOBAL logged_in_user = None

FUNCTION login(username):
    GLOBAL logged_in_user
    
    FIND user by username
    
    IF user not found THEN
        PRINT "User not found!"
        RETURN False
    END IF
    
    SET logged_in_user = user
    PRINT "Logged in!"
    RETURN True
END FUNCTION

FUNCTION logout():
    GLOBAL logged_in_user
    
    IF someone is logged in THEN
        PRINT "{username} logged out"
        SET logged_in_user = None
    ELSE
        PRINT "No user logged in"
    END IF
END FUNCTION

FUNCTION get_current_user():
    RETURN logged_in_user
END FUNCTION

FUNCTION is_logged_in():
    IF logged_in_user is None THEN
        RETURN False
    ELSE
        RETURN True
    END IF
END FUNCTION

FUNCTION register(username):
    TRY to CREATE new user
    
    IF user created successfully THEN
        RETURN True
    ELSE
        RETURN False
    END IF
END FUNCTION
```

---

## 4. Main Application (main.py)

```
FUNCTION show_menu():
    PRINT "TODO LIST APP"
    
    IF user is logged in THEN
        PRINT "Logged in as: {username}"
        PRINT menu options:
            1. Add Task
            2. View My Tasks
            3. Mark Task Complete
            4. Mark Task Incomplete
            5. Delete Task
            6. Logout
            7. Exit
    ELSE
        PRINT menu options:
            1. Login
            2. Create New User
            3. Exit
    END IF
END FUNCTION

FUNCTION add_task():
    GET current user
    ASK user for task title
    
    IF title is empty THEN
        PRINT "Task title cannot be empty"
        RETURN
    END IF
    
    CALL add_new_task(title, user.user_id)
    PRINT "Task added!"
END FUNCTION

FUNCTION view_tasks():
    GET current user
    GET all tasks for this user
    SHOW tasks in formatted table
END FUNCTION

FUNCTION mark_complete():
    GET current user
    GET all tasks for this user
    SHOW tasks
    ASK user which task ID to mark complete
    CALL mark_task_complete(task_id, user.user_id)
    
    IF successful THEN
        PRINT "Task marked as complete!"
    ELSE
        PRINT "Task not found"
    END IF
END FUNCTION

FUNCTION mark_incomplete():
    same as mark_complete but call mark_task_incomplete()
END FUNCTION

FUNCTION delete_task():
    GET current user
    GET all tasks for this user
    SHOW tasks
    ASK user which task ID to delete
    CALL delete_one_task(task_id, user.user_id)
    
    IF successful THEN
        PRINT "Task deleted!"
    ELSE
        PRINT "Task not found"
    END IF
END FUNCTION

FUNCTION login_user():
    ASK user for username
    CALL login(username)
END FUNCTION

FUNCTION create_user():
    ASK user for username
    
    IF username is empty THEN
        PRINT "Username cannot be empty"
        RETURN False
    END IF
    
    CALL register(username)
    AUTOMATICALLY login the new user
    RETURN True
END FUNCTION

FUNCTION main():
    PRINT "TODO List App Started"
    
    LOOP forever:
        SHOW menu
        GET user choice
        
        IF user is NOT logged in THEN
            IF choice == "1" THEN
                login_user()
            ELSE IF choice == "2" THEN
                create_user()
            ELSE IF choice == "3" THEN
                PRINT "Goodbye!"
                BREAK loop
            ELSE
                PRINT "Invalid option"
            END IF
        
        ELSE (user IS logged in):
            IF choice == "1" THEN
                add_task()
            ELSE IF choice == "2" THEN
                view_tasks()
            ELSE IF choice == "3" THEN
                mark_complete()
            ELSE IF choice == "4" THEN
                mark_incomplete()
            ELSE IF choice == "5" THEN
                delete_task()
            ELSE IF choice == "6" THEN
                logout()
            ELSE IF choice == "7" THEN
                PRINT "Goodbye!"
                BREAK loop
            ELSE
                PRINT "Invalid option"
            END IF
        END IF
    END LOOP
END FUNCTION

// Start the app
CALL main()
```

---

## 5. Data Flow Diagram

```
START APP
    ↓
SHOW MENU (not logged in)
    ↓
USER CHOOSES:
    ├─ 1. LOGIN
    │   ├─ ASK USERNAME
    │   ├─ FIND USER IN FILE
    │   ├─ SET logged_in_user
    │   └─ SHOW LOGGED IN MENU
    │
    ├─ 2. CREATE NEW USER
    │   ├─ ASK USERNAME
    │   ├─ CHECK IF EXISTS
    │   ├─ CREATE USER
    │   ├─ SAVE TO FILE
    │   ├─ AUTO LOGIN
    │   └─ SHOW LOGGED IN MENU
    │
    └─ 3. EXIT
        └─ END APP

LOGGED IN MENU:
    ├─ 1. ADD TASK
    │   ├─ ASK TITLE
    │   ├─ CREATE TASK
    │   ├─ SAVE TO FILE
    │   └─ SHOW SUCCESS
    │
    ├─ 2. VIEW TASKS
    │   ├─ LOAD ALL TASKS
    │   ├─ FILTER BY USER
    │   └─ DISPLAY TABLE
    │
    ├─ 3. MARK COMPLETE
    │   ├─ SHOW TASKS
    │   ├─ ASK TASK ID
    │   ├─ UPDATE TASK
    │   └─ SAVE TO FILE
    │
    ├─ 4. MARK INCOMPLETE
    │   └─ (Similar to #3)
    │
    ├─ 5. DELETE TASK
    │   ├─ SHOW TASKS
    │   ├─ ASK TASK ID
    │   ├─ REMOVE FROM LIST
    │   └─ SAVE TO FILE
    │
    ├─ 6. LOGOUT
    │   ├─ CLEAR logged_in_user
    │   └─ SHOW MAIN MENU
    │
    └─ 7. EXIT
        └─ END APP
```

---

## 6. File Structure

```
data/
├─ users.json    (stores all users: user_id, username, created_at)
└─ tasks.json    (stores all tasks: task_id, title, user_id, completed, created_at)

models/
├─ user.py       (User class, UserManager class, decorators)
└─ task.py       (task functions: add, delete, mark, view)

utils/
└─ auth.py       (login, logout, register, is_logged_in)

main.py          (main application loop and menu)
```

---

## 7. Key Concepts Used

### Classes
- **User**: Represents a single user with properties
- **UserManager**: Manages all user-related file operations

### Properties & Setters
- Used to validate data when setting username
- Private attributes (\_username, \_user_id, \_created_at)

### Decorators
- **@log_action()**: Prints action messages when functions are called
- **@property**: Allows accessing class attributes like normal variables
- **@staticmethod**: Methods that don't need access to instance data

### File Handling
- JSON files persist data between app sessions
- Load data into memory → modify → save back to file

### Session Management
- Global variable `logged_in_user` tracks who is currently logged in
- Used to filter tasks by user and validate operations

---

## 8. Example Flow: User Creates Task

```
1. User starts app
2. User selects "Create New User"
3. App calls create_user()
4. create_user() asks for username
5. create_user() calls register("alice")
6. register() calls UserManager.create_user("alice")
7. UserManager.create_user():
   - Checks if username exists
   - Creates User object
   - Loads current users from file
   - Adds new user to list
   - Saves all users to users.json
   - Returns new user
8. Auto-login calls login("alice")
9. login() finds user in file and sets logged_in_user
10. User sees logged-in menu
11. User selects "Add Task"
12. add_task() asks for title
13. add_task() calls add_new_task("Buy groceries", logged_in_user.user_id)
14. add_new_task():
    - Loads current tasks from file
    - Creates new task with ID, title, user_id, completed=False
    - Adds to list
    - Saves to tasks.json
    - Returns new task
15. App shows "Task added! (ID: xyz123)"
16. User selects "View My Tasks"
17. view_tasks() calls get_user_tasks(logged_in_user.user_id)
18. get_user_tasks():
    - Loads all tasks
    - Filters for tasks matching user_id
    - Returns filtered list
19. show_tasks() displays tasks in table format
20. User sees: "Buy groceries" with status "✗ Not Completed"
```

---

## Summary

The TODO CLI app uses:
- **OOP** with classes and properties
- **Decorators** for logging and validating properties
- **File persistence** with JSON
- **Session management** with global variables
- **Menu-driven interface** with infinite loop
- **User filtering** for tasks (each user only sees their own tasks)
