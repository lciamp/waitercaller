class User:
    def __init__(self, email):
        self.email = email

    # get_id is required to return a unique id
    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

