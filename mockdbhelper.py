import datetime

MOCK_USERS = [{'email': 'test@example.com',
               'salt': 'NRFU073fimsRVP72mmks',
               'hashed': 'd7ac9f5e44cb1b100fa9c5000850f02733ca3c2ccd6bfac13a8ccda05f70c35b45fdc92ef76e86e165f9fcc9c1915812ec56893564297d669f6e3fc26d8540a9'}]

MOCK_TABLES = [{'_id': '1',
                'number': '1',
                'owner': 'test@example.com',
                'url': 'mockurl'}]

MOCK_REQUESTS = [{'_id': '1',
                 'table_id': '1',
                 'table_number': '1',
                 'time': datetime.datetime.now()}]


class MockDBHelper:

    ## DB - USER METHODS:
    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({'email': email,
                           'salt': salt,
                           'hashed': hashed})

    # DB - TABLE METHODS
    def add_table(self, number, owner):
        MOCK_TABLES.append({'_id': str(number),
                            'number': number,
                            'owner': owner})
        return number

    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table.get('_id') == _id:
                table["url"] = url
                break

    def get_tables(self, owner_id):
        return MOCK_TABLES

    def get_table(self, table_id):
        for table in MOCK_TABLES:
            if table.get("_id") == table_id:
                return table

    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table.get("_id") == table_id:
                del MOCK_TABLES[i]
                break    

    # DB - REQUEST METHODS
    def get_requests(self, owner_id):
        return MOCK_REQUESTS

    def delete_request(self, request_id):
        for i, request in enumerate(MOCK_REQUESTS):
            if request.get('_id') == request_id:
                del MOCK_REQUESTS[i]
                break

    def add_request(self, table_id, time):
        table = self.get_table(table_id)
        MOCK_REQUESTS.append({"_id": table_id, 
                              "owner": table["owner"], 
                              "table_number": table["number"], 
                              "table_id": table_id, 
                              "time": time})
        return True









