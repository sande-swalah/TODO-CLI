import hashlib

class User:
    def __init__(self, name, email, password, role="user"):
        # assign via property setters so validation is centralized
        self.name = name
        self.email = email
        self.password = password      # setter will hash and validate
        self.role = role
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # ensure we have a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str) or "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Password must be a string")
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        self._password = hashlib.md5(value.encode()).hexdigest()
    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        valid_roles = ["user", "admin", "moderator"]
        if value not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        self._role = value


    def check_password(self, password):
        return self.password == hashlib.md5(password.encode()).hexdigest()

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
