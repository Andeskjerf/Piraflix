from room_model import RoomModel
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import uuid
import json

app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:8080")

# CORS(app, resources={'r/api/*': {'origins': '*'}})
CORS(app)

rooms = []


@app.route('/api/rooms', methods=['GET', 'POST'])
def all_rooms():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        room = RoomModel(
            uuid.uuid4().hex[:6].upper(),
            False,
            0,
            post_data.get('magnet')
        )
        rooms.append(room.toJSON())
        response_object['message'] = 'Room created'
        response_object['room'] = room.toJSON()
    else:
        roomId = request.args.get('roomId')
        print(roomId)
        roomFound = False
        if roomId:
            for room in rooms:
                roomLoaded = json.loads(room)
                if roomLoaded['id'] == roomId:
                    response_object['room'] = room
                    roomFound = True
                    print("Found room")
                    break

        if (roomFound == False):
            response_object['rooms'] = rooms

    return jsonify(response_object)


if __name__ == '__main__':
    socketio.run(app)
