
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
