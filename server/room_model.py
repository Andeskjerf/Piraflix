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
        self.users = []
        self.messages = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)

    def addMessage(self, message, userId, isStatus=False):
        message = MessageModel(self.getUser(
            userId), message, len(self.messages), isStatus)
        self.messages.append(message)
        return message

    def addUser(self, userId, username, sessionId):
        user = UserModel(userId, username, sessionId)
        self.users.append(user)
        return user

    def removeUser(self, userId):
        index = 0
        found = False
        for elem in self.users:
            if userId == elem.identifier:
                found = True
            if found:
                break
            index += 1
        user = self.users[index]
        del self.users[index]
        print('New user count: ' + str(len(self.users)))
        return user

    def getUser(self, userId):
        for elem in self.users:
            if elem.identifier == userId:
                return elem

    def getUserIndex(self, userId):
        index = 0
        for elem in self.users:
            if elem.identifier == userId:
                return index
            index += 1

    def isAnyUserBuffering(self):
        for elem in self.users:
            if elem.buffering == True:
                return True

        return False

    def getBufferingUsers(self):
        users = []
        for elem in self.users:
            if elem.buffering == True:
                users.append(elem)

        print(len(users))
        return users

    def printUserDetails(self):
        index = 0
        print('User count: ' + str(len(self.users)))
        for elem in self.users:
            print('ID: ' + elem.identifier)
            print('Username: ' + elem.username)
            print('Index: ' + str(index))
            print('\n')
            index += 1
