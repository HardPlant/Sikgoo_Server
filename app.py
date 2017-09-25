from flask import Flask, url_for, request
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    pass

@app.route('/login', method = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login()
    else:
        form()

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