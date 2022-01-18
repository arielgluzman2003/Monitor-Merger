class OneWayChannel:
    def __init__(self, queue):
        self.queue = queue
        self.messages = []

    def send(self, item_to_send):
        self.messages.append(item_to_send)
        for message in self.messages:
            if not self.queue.full():
                self.queue.put(item_to_send)
                self.messages.remove(self.messages[0])

    def recv(self):
        return self.queue.get_nowait()


class TwoWayChannel:
    def __init__(self, in_f, out_f):
        '''

        :param in_f: A Channel.Channel
        :param out_f: A Channel.Channel
        '''

        self.in_f = in_f
        self.out_f = out_f

    def send(self, item_to_send):
        self.out_f.send(item_to_send)

    def recv(self):
        return self.in_f.recv()
