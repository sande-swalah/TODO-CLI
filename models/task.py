class Task:
    def __init__(self, title, status="pending", assigned_to=""):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value):
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_statuses = ["pending", "in_progress", "completed"]
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self._status = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        if not isinstance(value, str):
            raise ValueError("assigned_to must be a string")
        self._assigned_to = value

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }