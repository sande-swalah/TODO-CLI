import json
import os
import uuid
from datetime import datetime

import json
from datetime import datetime
from pathlib import Path

class Task:
    """Represents a single task"""
    
    def __init__(self, title, description="", completed=False, task_id=None, created_at=None):
        self.id = task_id or int(datetime.now().timestamp() * 1000)
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        return Task(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            task_id=data['id'],
            created_at=data['created_at']
        )
    
    def mark_complete(self):
        self.completed = True
    
    def mark_incomplete(self):
        self.completed = False