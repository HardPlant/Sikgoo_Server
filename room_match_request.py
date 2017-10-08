from flask import Flask, url_for, request, jsonify
from flask import make_response
from flask import abort, redirect
from flask_json import FlaskJSON, as_json
from room_matcher import RoomMatcher, User
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
import datetime

__all__ = ['make_json_app']


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

#app = make_json_app(__name__)
app = Flask(__name__)
json = FlaskJSON(app)
matcher = RoomMatcher()


@app.route('/match_room', methods = ['GET','POST'])
@as_json
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
            return jsonify(user)
        except (KeyError,TypeError, ValueError):
            return abort(500)
            # raise JsonError(description='Invalid value.')

    return abort(500)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404

if __name__ == '__main__':
    app.run()