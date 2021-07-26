import json
from random_username.generate import generate_username
from py_avataaars import PyAvataaar


class UserModel:
    identifier = ''
    username = ''
    avatar = None

    def __init__(self, identifier, username=generate_username()[0]):
        self.identifier = identifier
        self.username = username
        # self.avatar = PyAvataaar

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)
