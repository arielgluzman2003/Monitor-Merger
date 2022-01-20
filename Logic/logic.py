''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
    
'''''

import pickle
from multiprocessing import Queue, Process, Pipe
from enum import Enum
from datetime import date
from Graphic.Monitor import Monitor
from Graphic.Point import Point
from Constants import Orientation
from Constants import OperationCodes
from Constants import ConnectionCodes

class Logic(Process):

    def __init__(self, input_queue, output_queue, client_handle_channel, operation_code):
        super(Logic, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self._client_handle_channel = client_handle_channel
        self.operation_code = operation_code
        self.main_monitor = Monitor()
        self.monitors = {Orientation.LEFT: None, Orientation.RIGHT: None,
                         Orientation.TOP: None, Orientation.BOTTOM: None}
        self._passcode = 'ABCDE'

    def run(self) -> None:
        input_message = b''
        while self.operation_code.value != OperationCodes.NOT_WORKING:
            if self._client_handle_channel.readable():
                orientation, message = pickle.loads(self._client_handle_channel.recv())
                if message.decode() in (ConnectionCodes.CLIENT_DETACHED):
                    if message.decode() == ConnectionCodes.CLIENT_DETACHED:
                        self.monitors[orientation] = None

                else:
                    if message == self._passcode:
                        if self.monitors[orientation] is not None:
                            pass  # Accept Client
                        else:
                            pass  # Reject Client Due to Orientation Unavailable
                    else:
                        pass  # Reject Client Due to Passcode Wrong
            if self.input_queue.readable():
                received_point = pickle.loads(self.input_queue.recv())
                print(received_point.get_position())


def get_relative_point(src_monitor, dst_monitor, point):
    if src_monitor.aspect_ratio != dst_monitor.aspect_ratio:
        raise Exception("For Now.. Can't Create relative point between two monitors with different aspect ratios")

    ratio = 1
    if dst_monitor.width > src_monitor.width:
        ratio = dst_monitor.width / src_monitor.width
    else:
        ratio = src_monitor.width > dst_monitor.width
    return Point(dst_monitor.width * ratio, dst_monitor.height * ratio)
