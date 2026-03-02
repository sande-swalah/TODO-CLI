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
def update_task():
    if not logged_in_user:
        print("Please login first.")
        return

    view_tasks()

    tasks = load_data("data/tasks.json")

    if logged_in_user["role"] == "admin":
        my_tasks = tasks
    else:
        my_tasks = [t for t in tasks if t["assigned_to"] == logged_in_user["email"]]

    if len(my_tasks) == 0:
        return

    try:
        choice = int(input("Pick task number to update: ")) - 1
        task = my_tasks[choice]
    except:
        print("Invalid choice.")
        return

    print("New status: 1) pending  2) in-progress  3) done")
    status_choice = input("Choose: ")

    if status_choice == "1":
        task["status"] = "pending"
    elif status_choice == "2":
        task["status"] = "in-progress"
    elif status_choice == "3":
        task["status"] = "done"
    else:
        print("Invalid.")
        return

    # save back - find and update in full list
    for t in tasks:
        if t["title"] == task["title"] and t["assigned_to"] == task["assigned_to"]:
            t["status"] = task["status"]

    save_data("data/tasks.json", tasks)
    print("Task updated!")

def delete_task():
    if not logged_in_user:
        print("Please login first.")
        return

    view_tasks()

    tasks = load_data("data/tasks.json")

    if logged_in_user["role"] == "admin":
        my_tasks = tasks
    else:
        my_tasks = [t for t in tasks if t["assigned_to"] == logged_in_user["email"]]

    if len(my_tasks) == 0:
        return

    try:
        choice = int(input("Pick task number to delete: ")) - 1
        task_to_delete = my_tasks[choice]
    except:
        print("Invalid choice.")
        return

    tasks.remove(task_to_delete)
    save_data("data/tasks.json", tasks)
    print("Task deleted!")

def main():
    print("Welcome to the TODO CLI!")

    while True:
        print("\n====== MENU ======")
        if logged_in_user is None:
            print("1. Register")
            print("2. Login")
        else:
            print(f"Logged in as: {logged_in_user['name']} ({logged_in_user['role']})")
            print("3. View Tasks")
            print("4. Add Task")
            print("5. Update Task")
            print("6. Delete Task")
            print("7. Logout")
        print("0. Exit")
        print("==================")

        choice = input("Choose: ")

        if choice == "1" and logged_in_user is None:
            register()
        elif choice == "2" and logged_in_user is None:
            login()
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            add_task()
        elif choice == "5":
            update_task()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            logout()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
