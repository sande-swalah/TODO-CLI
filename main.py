from models.user import User
from models.task import Task
from utils.auth import load_data, save_data, find_user

# who is logged in right now
logged_in_user = None

def register():
    print("\n-- Register --")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")

    users = load_data("data/users.json")

    if find_user(users, email):
        print("Email already exists!")
        return

    # first user is admin
    role = "admin" if len(users) == 0 else "user"

    new_user = User(name, email, password, role)
    users.append(new_user.to_dict())
    save_data("data/users.json", users)
    print(f"Account created! You are a {role}.")

def login():
    global logged_in_user
    print("\n-- Login --")
    email = input("Email: ")
    password = input("Password: ")

    users = load_data("data/users.json")
    user_data = find_user(users, email)

    if user_data is None:
        print("User not found.")
        return

    # check password using User class
    temp_user = User.__new__(User)
    temp_user.password = user_data["password"]
    temp_user.check_password = lambda p: __import__('hashlib').md5(p.encode()).hexdigest() == temp_user.password

    if temp_user.check_password(password):
        logged_in_user = user_data
        print(f"Welcome {user_data['name']}! Role: {user_data['role']}")
    else:
        print("Wrong password.")

def logout():
    global logged_in_user
    if logged_in_user:
        print(f"Bye {logged_in_user['name']}!")
        logged_in_user = None
    else:
        print("You are not logged in.")

def add_task():
    if not logged_in_user:
        print("Please login first.")
        return

    print("\n-- Add Task --")
    title = input("Task title: ")

    task = Task(title, assigned_to=logged_in_user["email"])
    tasks = load_data("data/tasks.json")
    tasks.append(task.to_dict())
    save_data("data/tasks.json", tasks)
    print("Task added!")

def view_tasks():
    if not logged_in_user:
        print("Please login first.")
        return

    tasks = load_data("data/tasks.json")

    # admins see all tasks, users see only theirs
    if logged_in_user["role"] == "admin":
        my_tasks = tasks
    else:
        my_tasks = [t for t in tasks if t["assigned_to"] == logged_in_user["email"]]

    if len(my_tasks) == 0:
        print("No tasks found.")
        return

    print("\n-- Tasks --")
    for i, task in enumerate(my_tasks):
        print(f"{i+1}. [{task['status']}] {task['title']} (assigned to: {task['assigned_to']})")

