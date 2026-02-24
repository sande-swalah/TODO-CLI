


import json
import hashlib

class User:
    users_file = 'data/users.json'

    @classmethod
    def register(cls):
        name = input("Enter name: ")
        email = input("Enter email: ")
        
        if not email:
            print("Email cannot be empty.")
            return
        
        password = input("Enter password: ")
        
        if not password:
            print("Password cannot be empty.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = {'name': name, 'email': email, 'password': hashed_password}

        if cls.save_user(user_data):
            print("User registered successfully.")
        else:
            print("User already exists.")

    @classmethod
    def save_user(cls, user_data):
        try:
            with open(cls.users_file, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []
        except json.JSONDecodeError:
            print("Error: users.json is malformed. Resetting.")
            users = []

        for user in users:
            if user['email'] == user_data['email']:
                return False

        users.append(user_data)
        with open(cls.users_file, 'w') as file:
            json.dump(users, file)
        return True

    @classmethod
    def login(cls):
        email = input("Enter email: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            with open(cls.users_file, 'r') as file:
                users = json.load(file)
                for user in users:
                    if user['email'] == email and user['password'] == hashed_password:
                        print("Login successful.")
                        return
        except FileNotFoundError:
            print("No users registered.")
            return
        except json.JSONDecodeError:
            print("Error: users.json is malformed.")
            return

        print("Invalid email or password.")