import json
import os

USERS_FILE = "data/users.json"
TASKS_FILE = "data/tasks.json"

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def find_user(users, email):
    for u in users:
        if u["email"] == email:
            return u
    return None
