
import argparse

from models.user import User
from models.task import Task

def main():
    parser = argparse.ArgumentParser(description='CLI Todo List Application')
    subparsers = parser.add_subparsers(dest='command')

    # User commands
    user_parser = subparsers.add_parser('user')
    user_subparsers = user_parser.add_subparsers(dest='action')
    user_subparsers.add_parser('register')
    user_subparsers.add_parser('login')

    # Task commands
    task_parser = subparsers.add_parser('task')
    task_subparsers = task_parser.add_subparsers(dest='action')
    task_subparsers.add_parser('add')
    task_subparsers.add_parser('list')
    task_subparsers.add_parser('complete')

    args = parser.parse_args()

    if args.command == 'user':
        if args.action == 'register':
            User.register()
        elif args.action == 'login':
            User.login()
    
    elif args.command == 'task':
        if args.action == 'add':
            Task.add_task()
        elif args.action == 'list':
            Task.list_tasks()
        elif args.action == 'complete':
            Task.complete_task()

if __name__ == '__main__':
    main()