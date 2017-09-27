import os
import tempfile
import unittest

from flask_json import JsonTestResponse

import sessionApp


class FlaskrTestCase(unittest.TestCase):

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



if __name__ == '__main__':
    unittest.main()