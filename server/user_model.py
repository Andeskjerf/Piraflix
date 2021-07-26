import json
from random_username.generate import generate_username


class UserModel:
    identifier = ''
    username = ''
    buffering = False

    def __init__(self, identifier):
        self.identifier = identifier
        self.username = generate_username()[0]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)
