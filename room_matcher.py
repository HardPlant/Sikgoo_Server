import json
import datetime
import requests

class RoomMatcher(object):

    def __init__(self):
        self.queue = []

    def enqueue(self, user):
        self.queue.append(user)

    def clear(self):
        self.queue = []

    def match(self, id):
        if len(self.queue) < 2:
            return []

        result = self.queue[:2]
        if id not in result:
            return []

        self.queue = self.queue[2:]
        send_notification(result[0], result[1])
        send_notification(result[1], result[0])

    def is_unmatchable(self):
        return len(self.queue) > 2

def send_notification(tokenfrom, tokento):
    sess = requests.Session()
    data = dict({
        "data": dict({
            "from": tokenfrom,
            "to": tokento
        }),
        "to" : tokento
    })
    JSON = json.dumps(data)

    req = requests.Request('POST', 'https://fcm.googleapis.com/fcm/send',json=JSON)
    prep = req.prepare()
    prep.headers['Authorization'] = 'key =' \
                                    + 'AAAA2RPB6OQ:APA91bHAIEOuFO0TzQqL6nAHjzEY3fAQv \
                                    AQdVvHsWFAurEYVCVqrBjOvfWiH4qW_NuWg4QfnIR0G \
                                    6NS0Z59qA9wGG_mflViQ3vfawsC90_TRRsFZyyEUuVNK \
                                    YNq2VV51O7tGtc3VcpRR'

    sess.send(prep)

class User(dict):
    def __init__(self, id, time = datetime.datetime.now()):
        dict.__init__(self, id=id, time=time)


