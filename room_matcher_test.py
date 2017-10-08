import unittest
from room_matcher import RoomMatcher, User
from random import randrange, randint
from flask_json import JsonTestResponse
import json
import datetime
import room_match_request


class FuntionalTest(unittest.TestCase):
    def setUp(self):
        room_match_request.app.config['TESTING'] = True
        room_match_request.app.response_class = JsonTestResponse
        self.app = room_match_request.app.test_client()

    def tearDown(self):
        rv = self.app.post('/match_reset')

    def test_empty_queue(self):
        rv = self.app.get('/match_room')
        self.assertTrue('404' in rv.data)

    def test_post(self):
        rv = self.app.post('/match_room', data=json.dumps(dict(
            id=1
        )))
        self.assertTrue('1' in rv.data)

    def test_post_one(self):
        rv = self.app.post('/match_room', data=json.dumps(dict(
            id=1
        )))
        self.assertTrue('1' in rv.data)
        rv = self.app.get('/match_room')
        print(rv.data)
        self.assertTrue('404' in rv.data)


def random_date(start, l):
    current = start
    while l >= 0:
        curr = current + datetime.timedelta(minutes=randrange(60))
        yield curr
        l-=1


def getRandomUser(count):
    list = []
    timelist = []
    startDate = datetime.datetime(2013,9,20,13,00)

    for time in random_date(startDate, count):
        timelist.append(time)

    for turn in range(0,count):
        list.append(User(turn, timelist[turn]))

    return list


class UnitTest(unittest.TestCase):
    def setUp(self):
        self.matcher = RoomMatcher()
        print()
    def tearDown(self):
        self.matcher.clear()

    def empty(self):
        for i in range(0,2):
            with self.subTest(i=i):
                users = getRandomUser(i)
                for user in users:
                    self.matcher.enqueue(user)
                self.assertEqual(self.matcher.match(), [], 'Ghostly matched')

    def test_three(self):
        users = getRandomUser(3)
        for user in users:
            self.matcher.enqueue(user)
        self.assertNotEqual(self.matcher.match(), [], 'Match failed')

    def test_four(self):
        users = getRandomUser(4)
        for user in users:
            self.matcher.enqueue(user)

        self.assertNotEqual(self.matcher.match(), [], 'Match failed')
        self.assertNotEqual(self.matcher.match(), [], 'Match failed at two')
        self.assertEqual(self.matcher.match(), [], 'now it is empty')

    def test_odd(self):
        odd = 13
        users = getRandomUser(odd)
        self.assertEqual(self.matcher.queue,[])
        #print(users)
        for user in users:
            self.matcher.enqueue(user)
        #print("Odd: %d" % odd)
        #print("Enqueue Completed")
        count = 0
        for turn in range(0,odd):
            matched = self.matcher.match()
            if len(matched) == 0: break
            count = count + 1
            #print("matched %d :" % count)
            #print(matched)

        self.assertEqual(count, int(odd/2))

    def test_even(self):
        odd = 28
        users = getRandomUser(odd)
        self.assertEqual(self.matcher.queue,[])
        #print(users)
        for user in users:
            self.matcher.enqueue(user)
        #print("Odd: %d" % odd)
        #print("Enqueue Completed")
        count = 0
        for turn in range(0,odd):
            matched = self.matcher.match()
            if len(matched) == 0: break
            count = count + 1
            #print("matched %d :" % count)
            #print(matched)

        self.assertEqual(count, int(odd/2))


if __name__ == '__main__':
    unittest.main()