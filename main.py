#!/usr/bin/env python3
"""
Simple TODO List App
A super simple app to manage your tasks
"""

from models.task import (
    add_new_task, 
    get_user_tasks, 
    show_tasks, 
    mark_task_complete, 
    mark_task_incomplete, 
    delete_one_task
)
from utils import auth


# Show the menu to the user
def show_menu():
    print("\n" + "="*50)
    print("TODO LIST APP")
    print("="*50)
    
    # Check if someone is logged in
    if auth.is_logged_in():
        # Get the logged in user
        user = auth.get_current_user()
        print(f"Logged in as: {user['username']}\n")
        
        # Show logged in menu
        print("1. Add Task")
        print("2. View My Tasks")
        print("3. Mark Task Complete")
        print("4. Mark Task Incomplete")
        print("5. Delete Task")
        print("6. Logout")
        print("7. Exit")
    else:
        # Show logged out menu
        print("\n1. Login")
        print("2. Create New User")
        print("3. Exit")
    
    print("="*50)


# Add a new task
def add_task():
    # Get the logged in user
    user = auth.get_current_user()
    
    # Ask for the task title
    title = input("\nEnter task title: ").strip()
    
    # Make sure they typed something
    if not title:
        print("✗ Task title cannot be empty")
        return
    
    # Add the task and get it back
    task = add_new_task(title, user["user_id"])
    
    # Show that it worked
    print(f"✓ Task added! (ID: {task['task_id']})")


# Show all tasks for this user
def view_tasks():
    # Get the logged in user
    user = auth.get_current_user()
    
    # Get all this user's tasks
    tasks = get_user_tasks(user["user_id"])
    
    # Show the tasks
    show_tasks(tasks)


# Mark a task as complete
def mark_complete():
    # Get the logged in user
    user = auth.get_current_user()
    
    # Get all this user's tasks
    tasks = get_user_tasks(user["user_id"])
    
    # If no tasks
    if len(tasks) == 0:
        print("\nNo tasks to complete!")
        return
    
    # Show the tasks
    show_tasks(tasks)
    
    # Ask which one to mark complete
    task_id = input("Enter task ID to mark complete: ").strip()
    
    # Try to mark it complete
    if mark_task_complete(task_id, user["user_id"]):
        print("✓ Task marked as complete!")
    else:
        print("✗ Task not found")


# Mark a task as incomplete
def mark_incomplete():
    # Get the logged in user
    user = auth.get_current_user()
    
    # Get all this user's tasks
    tasks = get_user_tasks(user["user_id"])
    
    # If no tasks
    if len(tasks) == 0:
        print("\nNo tasks to mark!")
        return
    
    # Show the tasks
    show_tasks(tasks)
    
    # Ask which one to mark incomplete
    task_id = input("Enter task ID to mark incomplete: ").strip()
    
    # Try to mark it incomplete
    if mark_task_incomplete(task_id, user["user_id"]):
        print("✓ Task marked as incomplete!")
    else:
        print("✗ Task not found")


# Delete a task
def delete_task():
    # Get the logged in user
    user = auth.get_current_user()
    
    # Get all this user's tasks
    tasks = get_user_tasks(user["user_id"])
    
    # If no tasks
    if len(tasks) == 0:
        print("\nNo tasks to delete!")
        return
    
    # Show the tasks
    show_tasks(tasks)
    
    # Ask which one to delete
    task_id = input("Enter task ID to delete: ").strip()
    
    # Try to delete it
    if delete_one_task(task_id, user["user_id"]):
        print("✓ Task deleted!")
    else:
        print("✗ Task not found")


# Login with a username
def login_user():
    # Ask for username
    username = input("\nEnter username: ").strip()
    
    # Try to login
    if auth.login(username):
        return True
    else:
        return False


# Create a new user
def create_user():
    # Ask for username
    username = input("\nEnter username: ").strip()
    
    # Make sure they typed something
    if not username:
        print("✗ Username cannot be empty")
        return False
    
    # Try to register
    if auth.register(username):
        # Automatically login after creating account
        auth.login(username)
        return True
    else:
        return False


# Main loop - keeps the app running
def main():
    print("\n✓ TODO List App Started\n")
    
    # Keep running forever until user exits
    while True:
        # Show the menu
        show_menu()
        
        # Ask user what they want to do
        choice = input("\nSelect option: ").strip()
        
        # If user is NOT logged in
        if not auth.is_logged_in():
            # Handle the login/not-logged-in menu options
            if choice == "1":
                # User chose to login
                login_user()
            elif choice == "2":
                # User chose to create new account
                create_user()
            elif choice == "3":
                # User chose to exit
                print("\n✓ Goodbye!")
                break
            else:
                # User typed something wrong
                print("✗ Invalid option")
        
        # If user IS logged in
        else:
            # Handle the logged in menu options
            if choice == "1":
                # User chose to add task
                add_task()
            elif choice == "2":
                # User chose to view tasks
                view_tasks()
            elif choice == "3":
                # User chose to mark task complete
                mark_complete()
            elif choice == "4":
                # User chose to mark task incomplete
                mark_incomplete()
            elif choice == "5":
                # User chose to delete task
                delete_task()
            elif choice == "6":
                # User chose to logout
                auth.logout()
            elif choice == "7":
                # User chose to exit
                print("\n✓ Goodbye!")
                break
            else:
                # User typed something wrong
                print("✗ Invalid option")


# Run the app
if __name__ == "__main__":
    main()

