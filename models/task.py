class Task:
    def __init__(self, title, status="pending", assigned_to=""):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }