# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''
Programmer: Ariel Gluzman
Date of creation: 2.1.2022

'''''
import multiprocessing
from abc import ABC, abstractmethod
from multiprocessing import Queue


def create(directed: bool):
    if directed:
        return DirectedChannel()
    else:
        direction_a = DirectedChannel()
        direction_b = DirectedChannel()
        channel_a = UndirectedChannel(in_channel=direction_a, out_channel=direction_b)
        channel_b = UndirectedChannel(in_channel=direction_b, out_channel=direction_a)
        return channel_a, channel_b


class BaseChannel(ABC):
    @abstractmethod
    def send(self, item) -> None:
        """Sends Item Into Channel"""
        pass

    @abstractmethod
    def recv(self):
        """Gets Item From Channel"""
        pass

    @abstractmethod
    def writeable(self) -> bool:
        """True if a send() can be done, else False"""
        pass

    @abstractmethod
    def readable(self) -> bool:
        """True if a recv() can be done, else False"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clears Out All Messages In Channel"""
        pass


class DirectedChannel(BaseChannel):
    def __init__(self, queue=None):
        # region type validation
        if queue is not None:
            if type(queue) is multiprocessing.queues.Queue:
                self.queue: Queue
                self.queue = queue
            else:
                raise ValueError(
                    "Error. value used for parameter 'queue' is not multiprocessing.Queue but '{typeinserted}'".format(
                        typeinserted=type(queue)))
        # endregion
        elif queue is None:
            self.queue = Queue()

    def send(self, item) -> None:
        self.queue.put(item)

    def recv(self):
        return self.queue.get()

    def writeable(self) -> bool:
        return not self.queue.full()

    def readable(self) -> bool:
        return not self.queue.empty()

    def clear(self) -> None:
        while not self.readable():
            _ = self.recv()


class UndirectedChannel(BaseChannel):
    def __init__(self, in_channel: DirectedChannel, out_channel: DirectedChannel):
        # region different instances validation
        if id(in_channel) == id(out_channel):
            raise ValueError("'in_channel' and 'out_channel' must be two different instances.")
        # endregion
        else:
            self.in_channel = in_channel
            self.out_channel = out_channel

    def send(self, item) -> None:
        self.out_channel.send(item=item)

    def recv(self):
        return self.in_channel.recv()

    def writeable(self) -> bool:
        return self.out_channel.writeable()

    def readable(self) -> bool:
        return self.in_channel.readable()

    def clear(self) -> None:
        self.in_channel.clear()

#
# class OneWayChannel:
#     '''
#     One Way Channel
#     ---------------
#     based on one queue, one end shall only
#     send and the other shall only receive.
#     Utilizing the Queue data structure you can receive
#     in some later time after message has been placed on buffer
#     '''''
#
#     def __init__(self, queue=None):
#         # region type validation
#         if queue is not None:
#             if type(queue) is multiprocessing.queues.Queue:
#                 self.queue = queue
#             else:
#                 raise ValueError(
#                     "Error. value used for parameter 'queue' is not multiprocessing.Queue but '{typeinserted}'".format(
#                         typeinserted=type(queue)))
#         # endregion
#         elif queue is None:
#             self.queue = Queue()
#
#     # enqueues item_to_send
#     def send(self, item_to_send) -> None:
#         """
#         :param item_to_send: Any Object
#         """
#         self.queue.put(item_to_send)
#
#     # dequeues one item
#     def recv(self):
#         """
#         :return: any object, bytes, integer etc.
#         """
#         return self.queue.get()
#
#     # True if a send() can be done, else False
#     def writeable(self):
#         return not self.queue.full()
#
#     # True if a recv() can be done, else False
#     def readable(self):
#         return not self.queue.empty()
#
#     # Drops All Elements in Queue
#     def clear(self):
#         while not self.readable():
#             _ = self.recv()
#
#
# class TwoWayChannel:
#     '''
#     Two Way Channel
#     ---------------
#     Based on two queues,
#     which are encapsulated to One-Way-Channel (OWC).
#
#     The same OWC is the output channel of Party A and input channel of Party B,
#     and the other OWC is the input channel of Party A and the output channel of Party B.
#     '''''
#
#     def __init__(self, in_channel: OneWayChannel, out_channel: OneWayChannel):
#         '''
#         :param in_channel: used for reading data, in other end - used for writing.
#         :param out_channel: used for writing data, in other end - used for reading.
#
#         example:
#             from channel import OneWayChannel, TwoWayChannel
#
#             direction_a = OneWayChannel()
#             direction_b = OneWayChannel()
#
#             process_a_channel = TwoWayChannel(in_channel=direction_a, out_channel=direction_b)
#             process_b_channel = TwoWayChannel(in_channel=direction_b, out_channel=direction_a)
#
#             .....
#         '''
#         # region different instances validation
#         if id(in_channel) == id(out_channel):
#             raise ValueError(
#                 "Error. 'in_channel' and 'out_channel' mustn't be the same instance of 'OneWayChannel', this will cause "
#                 "conflictions in use of TwoWayChannel")
#         # endregion
#         else:
#             self.in_channel = in_channel
#             self.out_channel = out_channel
#
#     # enqueues item_to_send into out_channel
#     def send(self, item_to_send):
#         """
#         :param item_to_send: Any Object
#         """
#         self.out_channel.send(item_to_send=item_to_send)
#
#     # dequeues item from in_channel
#     def recv(self):
#         """
#         :return: any object, bytes, integer etc.
#         """
#         return self.in_channel.recv()
#
#     # True if a send() can be done, else False
#     def writeable(self):
#         return self.out_channel.writeable()
#
#     # True if a recv() can be done, else False
#     def readable(self):
#         return self.in_channel.readable()
