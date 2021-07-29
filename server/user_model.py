import json


class UserModel:
    identifier = ''
    username = ''
    buffering = False
    sessionId = ''

    def __init__(self, identifier, username, sessionId):
        self.identifier = identifier
        self.username = username
        self.sessionId = sessionId

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)
