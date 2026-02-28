import json
import os
import uuid
from datetime import datetime
from functools import wraps


# ==================== DECORATORS ====================

def ensure_data_dir(func):
    """Decorator to ensure data directory exists before file operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists("data"):
            os.makedirs("data")
        return func(*args, **kwargs)
    return wrapper


def handle_file_errors(func):
    """Decorator to handle file operation errors gracefully"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IOError, json.JSONDecodeError) as e:
            print(f"[ERROR] File operation failed: {e}")
            return None
    return wrapper


def validate_task_data(func):
    """Decorator to validate task data before operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict) and result is not None:
            required_fields = ['id', 'title', 'completed', 'created_at']
            if all(field in result for field in required_fields):
                return result
        return result
    return wrapper


# ==================== TASK CLASS ====================

class Task:
    """Represents a single task in the to-do list"""
    
    def __init__(self, title, description="", task_id=None, completed=False, 
                 created_at=None, user_id=None):
        """Initialize a Task instance"""
        self.id = task_id or self._generate_id()
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.user_id = user_id

    @staticmethod
    def _generate_id():
        """Generate a short ID (8 characters)"""
        return str(uuid.uuid4())[:8]

    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        return {
            "task_id": self.id,
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary"""
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            task_id=data.get("task_id") or data.get("id"),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            user_id=data.get("user_id")
        )

    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} (ID: {self.id})"


# ==================== TASK STORAGE CLASS ====================

class TaskStorage:
    """Handles all task persistence operations"""
    
    DATA_FILE = "data/tasks.json"

    @classmethod
    @ensure_data_dir
    @handle_file_errors
    @validate_task_data
    def load_all_tasks(cls):
        """Load all tasks from the file"""
        if not os.path.exists(cls.DATA_FILE):
            return []
        
        with open(cls.DATA_FILE, 'r') as file:
            data = json.load(file)
        return data if isinstance(data, list) else []

    @classmethod
    @ensure_data_dir
    @handle_file_errors
    def save_all_tasks(cls, all_tasks):
        """Save all tasks to the file"""
        with open(cls.DATA_FILE, 'w') as file:
            json.dump(all_tasks, file, indent=2)
        return True

    @classmethod
    def add_new_task(cls, task_title, user_id, description=""):
        """Add a new task and return the Task object"""
        all_tasks = cls.load_all_tasks()
        
        new_task = Task(
            title=task_title,
            description=description,
            user_id=user_id
        )
        
        all_tasks.append(new_task.to_dict())
        cls.save_all_tasks(all_tasks)
        
        return new_task

    @classmethod
    def get_user_tasks(cls, user_id):
        """Get all tasks for a specific user"""
        all_tasks = cls.load_all_tasks()
        user_tasks = [task for task in all_tasks if task.get("user_id") == user_id]
        return user_tasks

    @classmethod
    def get_all_tasks(cls):
        """Get all tasks (used by main.py)"""
        all_tasks = cls.load_all_tasks()
        return [Task.from_dict(task) for task in all_tasks]

    @classmethod
    def delete_one_task(cls, task_id, user_id=None):
        """Delete a task by ID"""
        all_tasks = cls.load_all_tasks()
        original_count = len(all_tasks)
        
        new_task_list = [
            task for task in all_tasks 
            if not (task.get("task_id") == task_id or task.get("id") == task_id)
        ]
        
        if len(new_task_list) < original_count:
            cls.save_all_tasks(new_task_list)
            return True
        
        return False

    @classmethod
    def mark_task_complete(cls, task_id, user_id=None):
        """Mark a task as complete"""
        all_tasks = cls.load_all_tasks()
        
        for task in all_tasks:
            if task.get("task_id") == task_id or task.get("id") == task_id:
                task["completed"] = True
                cls.save_all_tasks(all_tasks)
                return True
        
        return False

    @classmethod
    def mark_task_incomplete(cls, task_id, user_id=None):
        """Mark a task as incomplete"""
        all_tasks = cls.load_all_tasks()
        
        for task in all_tasks:
            if task.get("task_id") == task_id or task.get("id") == task_id:
                task["completed"] = False
                cls.save_all_tasks(all_tasks)
                return True
        
        return False

    @staticmethod
    def show_tasks(task_list):
        """Display tasks in a formatted table"""
        if not task_list:
            print("No tasks found.\n")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<10} {'Task':<40} {'Status':<15}")
        print("="*70)
        
        for one_task in task_list:
            task_id = one_task.get('task_id') or one_task.get('id', 'N/A')
            title = one_task.get('title', 'N/A')
            status = "✓ Completed" if one_task.get("completed") else "✗ Not Completed"
            print(f"{task_id:<10} {title:<40} {status:<15}")
        
        print("="*70 + "\n")


# ==================== CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY ====================

def load_all_tasks():
    """Load all tasks (backward compatibility)"""
    return TaskStorage.load_all_tasks()


def save_all_tasks(all_tasks):
    """Save all tasks (backward compatibility)"""
    return TaskStorage.save_all_tasks(all_tasks)


def add_new_task(task_title, user_id):
    """Add a new task (backward compatibility)"""
    task = TaskStorage.add_new_task(task_title, user_id)
    return task.to_dict()


def get_user_tasks(user_id):
    """Get user tasks (backward compatibility)"""
    return TaskStorage.get_user_tasks(user_id)


def delete_one_task(task_id, user_id):
    """Delete a task (backward compatibility)"""
    return TaskStorage.delete_one_task(task_id, user_id)


def mark_task_complete(task_id, user_id):
    """Mark task complete (backward compatibility)"""
    return TaskStorage.mark_task_complete(task_id, user_id)


def mark_task_incomplete(task_id, user_id):
    """Mark task incomplete (backward compatibility)"""
    return TaskStorage.mark_task_incomplete(task_id, user_id)


def show_tasks(task_list):
    """Show tasks (backward compatibility)"""
    return TaskStorage.show_tasks(task_list)