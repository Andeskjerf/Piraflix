import json
from user_model import UserModel
from message_model import MessageModel


class RoomModel:
    id = ''
    paused = True
    timestamp = 0
    magnet = ''
    users = []
    messages = []
    owner = ''

    def __init__(self, id, paused, timestamp, magnet):
        self.id = id
        self.paused = paused
        self.timestamp = timestamp
        self.magnet = magnet

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)

    def addMessage(self, message, userId, isStatus=False):
        message = MessageModel(self.getUser(
            userId), message, len(self.messages), isStatus)
        self.messages.append(message)
        return message

    def addUser(self, userId):
        user = UserModel(userId)
        self.users.append(user)
        return user

    def getUser(self, userId):
        for elem in self.users:
            if elem.identifier == userId:
                return elem

    def removeUser(self, userId):
        index = 0
        found = False
        for elem in self.users:
            if userId == elem.identifier:
                found = True
            if found:
                break
            ++index
        user = self.users[index]
        del self.users[index]
        return user
