
import argparse
import sys
from models.task import Task
from utils.auth import (
    add_task, get_all_tasks, delete_task, 
    complete_task, incomplete_task, load_tasks
)

def cmd_add(args):
    """Add a new task"""
    task = add_task(args.title, args.description or "")
    print(f"[SUCCESS] Task added: {task.title} (ID: {task.id})")

def cmd_list(args):
    """List all tasks"""
    tasks = get_all_tasks()
    if not tasks:
        print("No tasks yet.")
        return

  print("\nYour Tasks:")
    print("-" * 60)
    for i, task in enumerate(tasks, 1):
        status = "[DONE]" if task.completed else "[TODO]"
        print(f"{i}. [{status}] {task.title}")
        if task.description:
            print(f"   Description: {task.description}")
    print("-" * 60)

def cmd_delete(args):
    """Delete a task"""
    tasks = get_all_tasks()
    if args.index < 1 or args.index > len(tasks):
        print("[ERROR] Invalid task number")
        return
task = tasks[args.index - 1]
    delete_task(task.id)
    print(f"[DELETED] {task.title}")
def cmd_complete(args):
    """Mark a task as complete"""
    tasks = get_all_tasks()
    if args.index < 1 or args.index > len(tasks):
        print("[ERROR] Invalid task number")
        return

task = tasks[args.index - 1]
    complete_task(task.id)
    print(f"[COMPLETED] {task.title}")

def cmd_incomplete(args):
    """Mark a task as incomplete"""
    tasks = get_all_tasks()
    if args.index < 1 or args.index > len(tasks):
        print("[ERROR] Invalid task number")
        return

task = tasks[args.index - 1]
    incomplete_task(task.id)
    print(f"[TODO] Marked incomplete: {task.title}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Simple To-Do List CLI",
        prog="todo"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

 # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description")
    add_parser.set_defaults(func=cmd_add)
  )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description")
    add_parser.set_defaults(func=cmd_add)

 # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=cmd_list)
