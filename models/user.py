import hashlib

class User:
    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.role = role

    def check_password(self, password):
        return self.password == hashlib.md5(password.encode()).hexdigest()

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
