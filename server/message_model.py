import json


class MessageModel:
    user = None
    message = None
    id = None
    isStatus = None

    def __init__(self, user, message, id, isStatus=False):
        self.user = user
        self.message = message
        self.id = id
        self.isStatus = isStatus

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)
