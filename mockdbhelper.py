MOCK_USERS = [{'email': 'test@example.com',
               'salt': 'NRFU073fimsRVP72mmks',
               'hashed': 'd7ac9f5e44cb1b100fa9c5000850f02733ca3c2ccd6bfac13a8ccda05f70c35b45fdc92ef76e86e165f9fcc9c1915812ec56893564297d669f6e3fc26d8540a9'}]

class MockDBHelper:
    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({'email': email,
                           'salt': salt,
                           'hashed': hashed})