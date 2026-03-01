import hashlib

class User:
    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.role = role



