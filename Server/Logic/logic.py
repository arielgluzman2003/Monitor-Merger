''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
    
'''''

import pickle
from multiprocessing import Process
from Graphic.Monitor import Monitor
from Graphic.Point import Point
from Utilities.Constants import Orientation
from Utilities.Constants import OperationCodes
from Utilities.Constants import ConnectionCodes


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
                orientation, message, data = pickle.loads(self._client_handle_channel.recv())
                if message in (ConnectionCodes.CLIENT_DETACHED, 1234):
                    if message == ConnectionCodes.CLIENT_DETACHED:
                        self.monitors[orientation] = None

                else:
                    if message == self._passcode:
                        if self.monitors[orientation] is None:
                            self._client_handle_channel.send(ConnectionCodes.CLIENT_APPROVED)  # Accept Client
                            self.monitors[orientation] = data
                            print(self.monitors[orientation].get_dimensions())
                        else:
                            self._client_handle_channel.send(
                                ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE)  # Reject Client Due to Orientation Unavailable
                    else:
                        self._client_handle_channel.send(
                            ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG)  # Reject Client Due to Passcode Wrong
            if self.input_queue.readable():
                received_point = self.input_queue.recv()
                for monitor in self.monitors.keys():
                    if self.monitors[monitor] is not None:
                        received_point = pickle.loads(received_point)
                        received_point.set_relative(self.main_monitor, self.monitors[monitor])
                        self.output_queue.send((monitor, received_point.get_position()))


def get_relative_point(src_monitor, dst_monitor, point):
    if src_monitor.aspect_ratio != dst_monitor.aspect_ratio:
        raise Exception("For Now.. Can't Create relative point between two monitors with different aspect ratios")

    ratio = 1
    if dst_monitor.width > src_monitor.width:
        ratio = dst_monitor.width / src_monitor.width
    else:
        ratio = src_monitor.width > dst_monitor.width
    return Point(dst_monitor.width * ratio, dst_monitor.height * ratio)
