''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
    
'''''

import pickle
from multiprocessing import Process
from Graphic.Display import Display
from Graphic.Point import Point
from Utilities.Constants import Orientation, OperationCodes, ConnectionCodes, ActionCodes


class Logic(Process):
    def __init__(self, input_queue, output_queue, client_handle_channel, operation_code):
        super(Logic, self).__init__()
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._client_handle_channel = client_handle_channel
        self._operation_code = operation_code
        self._main_display = Display()
        self._displays = dict.fromkeys([Orientation.LEFT, Orientation.RIGHT,
                                        Orientation.TOP, Orientation.BOTTOM], None)
        self._passcode = 'ABCDE'


    def run(self) -> None:
        input_message = b''
        while self._operation_code.value != OperationCodes.NOT_WORKING:
            if self._client_handle_channel.readable():
                orientation, message, data = pickle.loads(self._client_handle_channel.recv())
                if message in (ConnectionCodes.CLIENT_DETACHED, 1234):
                    if message == ConnectionCodes.CLIENT_DETACHED:
                        self._displays[orientation] = None
                        print("DETACHED CLIENT AT ", orientation)

                else:
                    if message == self._passcode:
                        if self._displays[orientation] is None:
                            self._client_handle_channel.send(ConnectionCodes.CLIENT_APPROVED)  # Accept Client
                            self._displays[orientation] = data
                            print(self._displays[orientation].get_dimensions())
                        else:
                            self._client_handle_channel.send(
                                ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE)  # Reject Client Due to
                            # Orientation Unavailable
                    else:
                        self._client_handle_channel.send(
                            ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG)  # Reject Client Due to Passcode Wrong
            if self._input_queue.readable():
                code, data = self._input_queue.recv()
                for display in self._displays.keys():
                    if self._displays[display] is not None:
                        if code is ActionCodes.NEW_POSITION:
                            data.set_relative(self._main_display, self._displays[display])
                        self._output_queue.send((display, code, data))


def get_relative_point(src_display, dst_display, point):
    if src_display.aspect_ratio != dst_display.aspect_ratio:
        raise Exception("For Now.. Can't Create relative point between two displays with different aspect ratios")

    ratio = 1
    if dst_display.width > src_display.width:
        ratio = dst_display.width / src_display.width
    else:
        ratio = src_display.width > dst_display.width
    return Point(dst_display.width * ratio, dst_display.height * ratio)
