from flask import Flask, url_for, request, jsonify
from flask import make_response
from flask import abort, redirect
from room_matcher import RoomMatcher, User
import datetime

matcher = RoomMatcher()

def match_room():
    if request.method == 'GET':
        result = matcher.match()
        if not result:
            abort(404)
        else:
            return jsonify(result)

    if request.method == 'POST':
        param = request.get_json()

        try:
            id = int(param['id'])
            name = int(param['name'])
            user = User(id,datetime.datetime.now())
            matcher.enqueue(user)
            return user
        except (KeyError,TypeError, ValueError):
            return abort(500)
            # raise JsonError(description='Invalid value.')

    return abort(500)