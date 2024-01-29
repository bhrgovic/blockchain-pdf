class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # In a real-world application, never store passwords in plain text
        self.email = email

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
        }