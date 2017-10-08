from flask import Flask, url_for, request, jsonify
from flask import make_response
from flask import render_template
from flask_json import FlaskJSON
from werkzeug import utils
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
import database
import models

from flask import abort, redirect

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

app = make_json_app(__name__)
json = FlaskJSON(app)

@app.route('/')
def index(): # session recommended
    username = request.cookies.get('username')

    resp = make_response(render_template('index.html'))
    resp.headers['HTTP-HEADER'] = 'Header!'
    resp.set_cookie('username','the username')
    if 1==1:
        return resp
    if str() == 'redirect':
        return redirect(url_for('login'))
        abort(401)
        #no_excute()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        pass
    else:
        error = 'Invalid username/password'

    return render_template('login.html', error=error)
@app.route('/upload', methods = ['GET', 'POST'])
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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404 # 404 means return code; default 200

if __name__ == '__main__':
    app.run()