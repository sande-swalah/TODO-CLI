class Users:
    def __init__(self):
        self.users = []

    def add_user(self, username):
        if username not in self.users:
            self.users.append(username)
            return True
        return False

    def remove_user(self, username):
        if username in self.users:
            self.users.remove(username)
            return True
        return False

    def list_users(self):
        return self.users
    