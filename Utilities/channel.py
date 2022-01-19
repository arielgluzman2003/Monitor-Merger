# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''
Programmer: Ariel Gluzman
Date of creation: 2.1.2022

'''''

import time

class OneWayChannel:
    '''
    One Way Channel
    ---------------
    based on one queue, one end shall only
    send and the other shall only receive.
    Utilizing the Queue data structure you can receive
    in some later time after message has been placed on buffer
    '''''

    def __init__(self, queue):
        self.queue = queue

    # enqueues item_to_send
    def send(self, item_to_send):
        self.queue.put(item_to_send)

    # dequeues one item
    def recv(self):
        return self.queue.get()

    # True if a send() can be done, else False
    def writeable(self):
        return not self.queue.full()

    # True if a recv() can be done, else False
    def readable(self):
        return not self.queue.empty()


class TwoWayChannel:
    '''
    Two Way Channel
    ---------------
    Based on two queues,
    which are encapsulated to One-Way-Channel (OWC).

    The same OWC is the output channel of Party A and input channel of Party B,
    and the other OWC is the input channel of Party A and the output channel of Party B.
    '''''

    def __init__(self, in_queue, out_queue):
        '''

        :param in_queue: A Channel.Channel
        :param out_queue: A Channel.Channel
        '''

        self.in_queue = in_queue
        self.out_queue = out_queue

    # enqueues item_to_send into OUT_QUEUE
    def send(self, item_to_send):
        self.out_queue.send(item_to_send=item_to_send)

    # dequeues item from IN_QUEUE
    def recv(self):
        return self.in_queue.recv()

    # True if a send() can be done, else False
    def writeable(self):
        return self.out_queue.writeable()

    # True if a recv() can be done, else False
    def readable(self):
        return self.in_queue.readable()

