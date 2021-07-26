from message_model import MessageModel
from user_model import UserModel
from room_model import RoomModel
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from random_username.generate import generate_username
import uuid
import datetime

app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:8080")

# CORS(app, resources={'r/api/*': {'origins': '*'}})
CORS(app)

rooms = {}


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
        rooms[room.id] = room
        response_object['message'] = 'Room created'
        response_object['room'] = room.toJSON()
    else:
        roomId = request.args.get('roomId')
        tempRoom = rooms.get(roomId)
        if tempRoom is not None:
            response_object['room'] = tempRoom.toJSON()
        else:
            response_object['rooms'] = rooms

    return jsonify(response_object)


@socketio.on('connect')
def test_connect():
    emit('after connect', {'data': 'hello, world!'})


@socketio.on('join')
def on_join(data):
    user = rooms[data['roomId']].addUser(request.sid)
    message = rooms[data['roomId']].addMessage(
        user.username + ' has joined', user.identifier, True)
    join_room(data['roomId'])
    emit('join', message.toJSON(), to=data['roomId'])


@socketio.on('leave')
def on_leave(data):
    user = rooms[data['roomId']].removeUser(request.sid)
    leave_room(data['roomId'])
    emit('leave', user.username + ' has left', to=data['roomId'])


@socketio.on('messageSend')
def on_message(data):
    print(data)
    if rooms.get(data['roomId']) is not None:
        message = rooms[data['roomId']].addMessage(
            data['message'],
            request.sid)
        emit('messageSend', message.toJSON(), to=data['roomId'])


@socketio.on('play')
def play_video(roomId):
    if rooms.get(roomId) is not None:
        rooms[roomId].paused = False
        print(rooms[roomId].paused)
        emit('beginPlay', {'data': 'played'}, to=roomId, include_self=False)

        message = rooms[roomId].addMessage(
            'Resumed playback',
            request.sid, True)

        emit('messageSend', message.toJSON(), to=roomId)


@socketio.on('pause')
def pause_video(roomId):
    if rooms.get(roomId) is not None:
        rooms[roomId].paused = True
        emit('pausePlay', {'data': 'paused'}, to=roomId, include_self=False)

        message = rooms[roomId].addMessage(
            'Paused playback',
            request.sid, True)

        emit('messageSend', message.toJSON(), to=roomId)


@socketio.on('timestamp')
def update_time(data):
    if rooms.get(data['roomId']) is not None:
        rooms[data['roomId']].timestamp = data['timestamp']


@socketio.on('seeked')
def seeked(data):
    if rooms.get(data['roomId']) is not None:
        rooms[data['roomId']].timestamp = data['timestamp']
        emit('seek', {'time': data['timestamp']},
             to=data['roomId'], include_self=False)

        message = rooms[data['roomId']].addMessage(
            'Seeking to ' +
            str(datetime.timedelta(seconds=int(round(data['timestamp'])))),
            request.sid, True)

        emit('messageSend', message.toJSON(), to=data['roomId'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
