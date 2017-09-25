from flask import Flask, session, redirect, url_for, escape, request
'''
session implement cookie with encryption
'''
app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['useranme'])
    return 'Not loggend in'

@app.route('/login', method = ['GET','POST'])
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
import os
os.urandom(24) # makes 24 length hex key
app.secret_key = 'Something_Key_Do_Not_Hardcode'

if __name__ == '__main__':
    app.run()