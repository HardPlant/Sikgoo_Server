import json
import datetime

class RoomMatcher(object):

    def __init__(self):
        self.queue = []

    def enqueue(self, user):
        self.queue.append(user)

    def clear(self):
        self.queue = []

    def match(self):
        if len(self.queue) < 2:
            return []

        result = self.queue[:2]
        self.queue = self.queue[2:]

        return result

    def is_unmatchable(self):
        return len(self.queue) > 2


class User(object):
    def __init__(self, id, time = datetime.datetime.now()):
        self.id = id
        self.time = time


