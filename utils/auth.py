"""
Authentication - handle login/logout
"""

from models.user import find_user, add_new_user
from models.task import TaskStorage

# This variable stores the person who is logged in
# If nobody is logged in, it's None
logged_in_user = None


# Login a user
def login(username):
    global logged_in_user
    
    # Find the user in the file
    user = find_user(username)
    
    # If we didn't find the user
    if user is None:
        print(f"User '{username}' not found!")
        return False
    
    # Set the global variable to this user
    logged_in_user = user
    print(f"✓ Logged in as {username}!")
    return True


# Logout the current user
def logout():
    global logged_in_user
    
    # If someone is logged in
    if logged_in_user is not None:
        username = logged_in_user["username"]
        print(f"✓ {username} logged out")
        # Clear the logged in user
        logged_in_user = None
    else:
        print("No user logged in")


# Get the user who is currently logged in
def get_current_user():
    return logged_in_user


# Check if anyone is logged in
def is_logged_in():
    if logged_in_user is None:
        return False
    else:
        return True


# Register a new user
def register(username):
    # Try to create the user
    user = add_new_user(username)
    
    # If it worked
    if user:
        return True
    else:
        return False

# ==================== TASK MANAGEMENT FUNCTIONS ====================

def add_task(title, description=""):
    """Add a new task and return the Task object"""
    user = get_current_user()
    user_id = user.get("id") if user else None
    return TaskStorage.add_new_task(title, user_id, description)


def get_all_tasks():
    """Get all tasks as Task objects"""
    return TaskStorage.get_all_tasks()


def delete_task(task_id):
    """Delete a task by ID"""
    return TaskStorage.delete_one_task(task_id)


def complete_task(task_id):
    """Mark a task as complete"""
    return TaskStorage.mark_task_complete(task_id)


def incomplete_task(task_id):
    """Mark a task as incomplete"""
    return TaskStorage.mark_task_incomplete(task_id)


def load_tasks():
    """Load all tasks"""
    return TaskStorage.load_all_tasks()