from flask import Flask, session, redirect, url_for, escape, request
from flask_json import FlaskJSON, json_response
import database
from datetime import datetime

'''
session implement cookie with encryption
import os
os.urandom(24) # makes 24 length hex key
'''
app = Flask(__name__)
json = FlaskJSON(app)


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

if __name__ == '__main__':
    app.run()