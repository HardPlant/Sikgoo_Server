from flask import Flask, session, redirect, url_for, escape, request, abort
from flask_json import FlaskJSON, json_response, JsonError, as_json
import database
import room_matcher
from datetime import datetime

'''
session implement cookie with encryption
import os
os.urandom(24) # makes 24 length hex key
'''
app = Flask(__name__)
json = FlaskJSON(app)
matcher = room_matcher.RoomMatcher()

def init_db():
    if app.config['TESTING']:
        global engine, db_session, Base
        engine, db_session, Base = database.test_init_db()
    else:
        return database.init_db()


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['useranme'])
    return 'Not loggend in'


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
    <form action "" method='post>
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    </form
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
app.secret_key = 'Something_Key_Do_Not_Hardcode'


@app.route('/time')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now)


@app.route('/increment_value', methods=['POST'])
def increment_value():
    data = request.get_json(force=True) # skim mimetype, have shorte curl command

    try:
        value = int(data['value'])
    except (KeyError,TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    return json_response(value=value+1)


@app.route('/get_value')
@as_json
def get_value():
    return dict(value=12)


@app.route('/match_room', methods=['GET','POST'])
def match_room():
    if request.method == 'GET':
        result = matcher.match()
        if not result:
            abort(404)
        else:
            return json_response(result)

    if request.method == 'POST':
        param = request.get_json()

        try:
            id = int(param['id'])
        except (KeyError,TypeError, ValueError):
            raise JsonError(description='Invalid value.')

        matcher.enqueue(id)
        return True


if __name__ == '__main__':
    app.run()