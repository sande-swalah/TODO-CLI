import json

class Task:
    tasks_file = 'data/tasks.json'

    @classmethod
    def add_task(cls):
        title = input("Enter task title: ")
        task_data = {'title': title, 'status': 'pending'}
        cls.save_task(task_data)

    @classmethod
    def save_task(cls, task_data):
        try:
            with open(cls.tasks_file, 'r+') as file:
                tasks = json.load(file)
                tasks.append(task_data)
                file.seek(0)
                json.dump(tasks, file)
        except FileNotFoundError:
            with open(cls.tasks_file, 'w') as file:
                json.dump([task_data], file)

    @classmethod
    def list_tasks(cls):
        try:
            with open(cls.tasks_file, 'r') as file:
                tasks = json.load(file)
                for task in tasks:
                    print(f"{task['title']} - {task['status']}")
        except FileNotFoundError:
            print("No tasks available.")