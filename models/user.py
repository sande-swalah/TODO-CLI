import json
import os
from datetime import datetime




# A decorator to print messages when user is created or modified
def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[LOG] {action_name}...")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# User class - represents a single user
class User:
    # Initialize a new user
    def __init__(self, username, user_id,):
        self._username = username
        self._user_id = user_id 
        
    
    # Get the username property
    @property
    def username(self):
        return self._username
    
    # Set a new username
    @username.setter
    def username(self, new_username):
        if not new_username or len(new_username) == 0:
            raise ValueError("Username cannot be empty")
        self._username = new_username
    
    # Get the user ID property
    @property
    def user_id(self):
        return self._user_id
    
    # Get the created date property
    @property
    def created_at(self):
        return self._created_at
    
    # Convert user to a dictionary (for saving to JSON)
    def to_dict(self):
        return {
            "user_id": self._user_id,
            "username": self._username,
            "created_at": self._created_at
        }
    
    # Create a User object from a dictionary
    @staticmethod
    def from_dict(data):
        return User(
            username=data.get("username", ""),
            user_id=data.get("user_id"),
            created_at=data.get("created_at")
        )
    
    # Show user info as a string
    def __str__(self):
        return f"User({self._username}, ID: {self._user_id})"


# UserManager class - handles loading and saving users to file
class UserManager:
    USERS_FILE = "data/users.json"
    
    # Load all users from the file
    @staticmethod
    def load_users():
        # Check if file exists
        if not os.path.exists(UserManager.USERS_FILE):
            return []
        
        try:
            # Open and read the file
            file = open(UserManager.USERS_FILE, 'r')
            data = json.load(file)
            file.close()
            
            # Convert each dictionary to a User object
            users = []
            for user_data in data:
                users.append(User.from_dict(user_data))
            return users
        except:
            # If there's an error, return empty list
            return []
    
    # Save all users to the file
    @staticmethod
    def save_users(users):
        # Create data folder if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")
        
        try:
            # Convert all User objects to dictionaries
            user_list = [user.to_dict() for user in users]
            
            # Write to file
            file = open(UserManager.USERS_FILE, 'w')
            json.dump(user_list, file, indent=2)
            file.close()
            return True
        except:
            return False
    
    # Check if a username already exists
    @staticmethod
    def username_exists(username_to_check):
        # Load all users
        users = UserManager.load_users()
        
        # Go through each user
        for user in users:
            # Compare usernames (case-insensitive)
            if user.username.lower() == username_to_check.lower():
                return True
        
        # Not found
        return False
    
    # Find a user by username
    @staticmethod
    def find_user(username):
        # Load all users
        users = UserManager.load_users()
        
        # Go through each user
        for user in users:
            # Compare usernames (case-insensitive)
            if user.username.lower() == username.lower():
                return user
        
        # User not found
        return None
    
    # Create and save a new user
    @staticmethod
    @log_action("Creating new user")
    def create_user(username):
        # Check if username already exists
        if UserManager.username_exists(username):
            print(f"✗ User '{username}' already exists!")
            return None
        
        # Create new User object
        new_user = User(username)
        
        # Load existing users
        users = UserManager.load_users()
        
        # Add the new user
        users.append(new_user)
        
        # Save all users back to file
        UserManager.save_users(users)
        
        print(f"✓ User '{username}' created!")
        return new_user


# These functions are for compatibility with auth.py
# They wrap the UserManager and User classes

def find_user(username):
    """Find a user by username - returns a dictionary"""
    user = UserManager.find_user(username)
    if user:
        return user.to_dict()
    return None


def add_new_user(username):
    """Create a new user - returns a dictionary"""
    user = UserManager.create_user(username)
    if user:
        return user.to_dict()
    return None

    


    
    