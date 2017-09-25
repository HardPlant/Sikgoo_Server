from flask import Flask, url_for, request
from flask import make_response
from flask import render_template
from werkzeug import utils

from flask import abort, redirect
app = Flask(__name__)

@app.route('/')
def index(): # session recommended
    username = request.cookies.get('username')

    resp = make_response(render_template('index.html'))
    resp.set_cookie('username','the username')
    if 1==1:
        return resp
    if str() == 'redirect':
        return redirect(url_for('login'))
        abort(401)
        #no_excute()

@app.route('/login', method = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
    else:
        error = 'Invalid username/password'

    return render_template('login.html', error=error)
@app.route('/upload', method = ['GET', 'POST'])
def upload_file():
    if request.methd == 'POST':
        f = request.files['the_file']
        #f.save('/var/www/uploads/uploaded_file.txt')
        f.save('/var/www/uploads/' + utils.secure_filename(f.filename))

@app.route('/user/<username>')
def profile(username):
    pass

with app.test_request_context():
    print url_for('index') # func -> url
    print url_for('login')
    print url_for('login', next='/') # Get Params
    print url_for('profile', username = 'John doe')
    #print url_for('static', filename='style.css')

@app.route('/hello')
@app.route('/hello/<name<')
def hello(name=None):
    return render_template('hello.html',name=name)

with app.test_request_context('/hello', method='POST'): # context manager test
    assert request.path == '/hello'
    assert request.method == 'POST'

if __name__ == '__main__':
    app.run()