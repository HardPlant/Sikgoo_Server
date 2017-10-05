class RoomMatcher(object):
    queue = []

    def __init__(self):
        pass

    def enqueue(self, user):
        self.queue.append(user)

    def match(self):
        if len(self.queue) < 2:
            return []

        result = self.queue[:1]
        self.queue = self.queue[2:]

        return result


