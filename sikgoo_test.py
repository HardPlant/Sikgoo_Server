import unittest
from flask import jsonify
from flask_json import JsonTestResponse
import json
import sessionApp


class TestCase(unittest.TestCase):

    def setUp(self):
        sessionApp.app.config['TESTING'] = True
        sessionApp.app.response_class = JsonTestResponse
        self.app = sessionApp.app.test_client()

        sessionApp.init_db()

    def tearDown(self):
        pass

    def test_empty_db(self):
        rv = self.app.get('/')

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirect=True)

    def test_time(self):
        rv = self.app.get('/time')
        assert '"status": 200' in rv.data
        assert '"time": ' in rv.data

    def test_get_value(self):
        rv = self.app.get('/get_value')
        assert '"value": 12' in rv.data

    def test_invalid_data(self):
        return
        rv = self.app.post('/increment_value', data=dict(
            data='bla'
        ))

        assert '"status": 400' in rv.data
        assert '"description": "Not a JSON."' in rv.data

    def test_good_data(self):
        param = dict(
            value=10
        )
        rv = self.app.post('/increment_value', data=json.dumps(param))
        assert 'value' in rv.json
        assert rv.json['value'] == 11

    def test_json(self):
        rv = self.app.get('/get_value')

        assert 'value' in rv.json
        assert type(rv.json['value']) is int

    def test_match_enqueue(self):
        param = dict(
            value=10
        )
        rv = self.app.post('/match_room', data=
                           json.dumps(param))

        print rv.json


if __name__ == '__main__':
    unittest.main()