import json


class RoomModel:
    id = ''
    paused = False
    timestamp = 0
    magnet = ''

    def __init__(self, id, paused, timestamp, magnet):
        self.id = id
        self.paused = paused
        self.timestamp = timestamp
        self.magnet = magnet

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self):
        return json.loads(self, object_hook=lambda o: o.__dict__, sort_keys=True, indent=4)
