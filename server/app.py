from enum import unique
import json
from server.room_model import RoomModel
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from server.key import APP_SECRET_KEY, APP_REDIS_PASSWORD
from random_username.generate import generate_username
import uuid
import datetime
import redis
import os


scriptDir = os.path.dirname(__file__)
relativePath = '../config/hosts.json'
hostConfigPath = os.path.join(scriptDir, relativePath)

f = open(hostConfigPath)
hostsData = json.load(f)
hostIP = hostsData['ip']
frontendPort = hostsData['frontendPort']
redisPort = hostsData['redisPort']
httpType = hostsData['httpType']


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = APP_SECRET_KEY
app.config.update(SESSION_COOKIE_SAMESITE="Strict",
                  SESSION_COOKIE_SECURE=False)
socketio = SocketIO(app,
                    logger=True,
                    engineio_logger=True,
                    cors_allowed_origins=[httpType + "://" + hostIP + ":" + frontendPort])

# CORS(app, resources={'r/api/*': {'origins': '*'}})
CORS(app, supports_credentials=True)


redisPassword = APP_REDIS_PASSWORD
r = redis.StrictRedis(
    host=hostIP,
    port=redisPort,
    password=redisPassword,
    decode_responses=True)


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


@app.route('/cookie/', methods=['GET'])
def landing_page():
    cookie = request.cookies.get('identifier')
    print(cookie)
    if cookie is None:
        print('Visitor has no unique identifier cookie, setting one now')
        uniqueId = uuid.uuid4().hex + '-' + uuid.uuid4().hex
        cookie = make_response('Setting identifier cookie')
        cookie.set_cookie('identifier',
                          value=uniqueId,
                          domain=hostIP,
                          samesite='Strict')

        r.set(name=uniqueId, value=generate_username()[0])
        print(r.get(uniqueId))
    else:
        print('Visitor has unique identifier cookie')

    return cookie


def get_username():
    return r.get(request.cookies['identifier'])


@socketio.on('join')
def on_join(data):
    cookie = request.cookies['identifier']
    print(cookie)
    user = rooms[data['roomId']].addUser(
        cookie,
        get_username())

    message = rooms[data['roomId']].addMessage(
        'Connected',
        user.identifier,
        True)

    join_room(data['roomId'])

    emit('join', message.toJSON(), to=data['roomId'])
    emit('roomUserCount', json.dumps(
        [user.__dict__ for user in rooms[data['roomId']].users]), to=data['roomId'])


@socketio.on('disconnect')
@socketio.on('leave')
def on_leave():
    print('Disconnect triggered')
    user = None
    room = None
    cookie = request.cookies['identifier']
    for key, value in rooms.items():
        temp_user = value.getUser(cookie)
        if temp_user is not None:
            user = temp_user
            room = value

    if user is None and room is None:
        print('ERROR! No user or room?')
    else:
        print('User disconnected: ' + user.username)
        message = rooms[room.id].addMessage(
            'Disconnected', user.identifier, True)
        user = rooms[room.id].removeUser(user.identifier)
        leave_room(room.id)
        emit('leave', message.toJSON(), to=room.id)
        emit('roomUserCount', json.dumps(
            [user.__dict__ for user in rooms[room.id].users]), to=room.id)


@socketio.on('messageSend')
def on_message(data):
    if (not data['message'].isspace()):
        if rooms.get(data['roomId']) is not None:
            cookie = request.cookies['identifier']
            message = rooms[data['roomId']].addMessage(
                data['message'],
                cookie)
            emit('messageSend', message.toJSON(), to=data['roomId'])


@socketio.on('play')
def play_video(roomId):
    if rooms.get(roomId) is not None:
        rooms[roomId].paused = False
        print(rooms[roomId].paused)
        emit('beginPlay', {'data': 'played'}, to=roomId, include_self=False)

        cookie = request.cookies['identifier']

        message = rooms[roomId].addMessage(
            'Resumed playback',
            cookie,
            True)

        emit('messageSend', message.toJSON(), to=roomId)


@socketio.on('pause')
def pause_video(roomId):
    if rooms.get(roomId) is not None:
        rooms[roomId].paused = True
        emit('pausePlay', {'data': 'paused'}, to=roomId, include_self=False)
        cookie = request.cookies['identifier']

        message = rooms[roomId].addMessage(
            'Paused playback',
            cookie, True)

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

        cookie = request.cookies['identifier']
        message = rooms[data['roomId']].addMessage(
            'Seeking to ' +
            str(datetime.timedelta(seconds=int(round(data['timestamp'])))),
            cookie, True)

        emit('messageSend', message.toJSON(), to=data['roomId'])


@socketio.on('buffering')
def video_buffering(roomId):
    if rooms.get(roomId) is not None:
        cookie = request.cookies['identifier']
        userIndex = rooms[roomId].getUserIndex(cookie)
        rooms[roomId].users[userIndex].buffering = True
        users = rooms[roomId].getBufferingUsers()

        emit('buffering', json.dumps(
            [user.__dict__ for user in users]),
            to=roomId)


@socketio.on('bufferComplete')
def video_buffered(roomId):
    if rooms.get(roomId) is not None:
        cookie = request.cookies['identifier']
        userIndex = rooms[roomId].getUserIndex(cookie)
        rooms[roomId].users[userIndex].buffering = False
        users = rooms[roomId].getBufferingUsers()
        print('Total users: ' + str(len(rooms[roomId].users)))
        print('Buffering users: ' + str(len(users)))
        emit('buffering', json.dumps(
            [user.__dict__ for user in users]),
            to=roomId)


if __name__ == '__main__':
    socketio.run(app, debug=True)
