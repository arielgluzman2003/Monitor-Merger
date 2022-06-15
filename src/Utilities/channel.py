"""
Author: Ariel Gluzman
Date of creation: 2.1.2022
email: ariel.gluzman@gmail.com
"""

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
        while self.readable():
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
