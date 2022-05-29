''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
    
'''''
from multiprocessing import Process
from Utilities.channel import *

import mouse

from Graphic.Display import Display
from Graphic.Point import Point
from Utilities.Constants import Orientation, OperationCodes, ConnectionCodes, ActionCodes, WindowCodes
from Graphic.window import Window

SCREEN_MARGIN = 2


class Logic(Process):
    def __init__(self, input_queue: OneWayChannel, output_queue: OneWayChannel, client_handle_channel: TwoWayChannel,
                 operation_code: multiprocessing.Value):
        super(Logic, self).__init__()
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._client_handle_channel = client_handle_channel
        self._operation_code = operation_code
        self._main_display = Display()
        self._displays = dict.fromkeys([Orientation.LEFT, Orientation.RIGHT,
                                        Orientation.TOP, Orientation.BOTTOM], None)
        self._passcode = 'ABCDE'
        self._current_display = Orientation.MAIN

    def run(self) -> None:
        transparent_window = Window(operation_code=self._operation_code)
        transparent_window.start()
        input_message = b''
        while self._operation_code.value != OperationCodes.NOT_WORKING:
            if self._client_handle_channel.readable():
                orientation, message, data = self._client_handle_channel.recv()
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
                if code is ActionCodes.NEW_POSITION:
                    data: Point

                    x, y = mouse.get_position()

                    # Check For Screen Changes
                    if self._current_display == Orientation.MAIN:
                        if data.x < SCREEN_MARGIN:
                            if self._displays[Orientation.LEFT] is not None:
                                self._current_display = Orientation.LEFT
                                transparent_window.wake()
                                mouse.move(self._main_display.width - SCREEN_MARGIN, y)
                        if data.x > self._main_display.width - SCREEN_MARGIN:
                            if self._displays[Orientation.RIGHT] is not None:
                                self._current_display = Orientation.RIGHT
                                self._input_queue.clear()
                                self._input_queue.send((ActionCodes.NEW_POSITION, Point(x=SCREEN_MARGIN, y=y)))
                                mouse.move(SCREEN_MARGIN, y)
                                transparent_window.wake()
                        if data.y < SCREEN_MARGIN:
                            if self._displays[Orientation.TOP] is not None:
                                self._current_display = Orientation.TOP
                                mouse.move(x, self._main_display.height - SCREEN_MARGIN)
                                transparent_window.wake()
                        if data.y > self._main_display.height - SCREEN_MARGIN:
                            if self._displays[Orientation.BOTTOM] is not None:
                                self._current_display = Orientation.BOTTOM
                                mouse.move(x, SCREEN_MARGIN)
                                transparent_window.wake()
                    elif self._current_display == Orientation.RIGHT:
                        if data.x < SCREEN_MARGIN:
                            self._current_display = Orientation.MAIN
                            mouse.move(self._main_display.width - SCREEN_MARGIN, y)
                            transparent_window.destroy()
                    elif self._current_display == Orientation.LEFT:
                        if data.x > self._main_display.width - SCREEN_MARGIN:
                            self._input_queue.clear()
                            self._current_display = Orientation.MAIN
                            transparent_window.destroy()
                            mouse.move(SCREEN_MARGIN, y)
                    elif self._current_display == Orientation.TOP:
                        if data.y > self._main_display.height - SCREEN_MARGIN:
                            self._current_display = Orientation.MAIN
                            mouse.move(x, SCREEN_MARGIN)
                            transparent_window.destroy()
                    elif self._current_display == Orientation.BOTTOM:
                        if data.y < SCREEN_MARGIN:
                            self._current_display = Orientation.MAIN
                            mouse.move(x, self._main_display.height - SCREEN_MARGIN)
                            transparent_window.destroy()

                    if self._current_display != Orientation.MAIN:
                        data.set_relative(self._main_display, self._displays[self._current_display])

                if self._current_display != Orientation.MAIN:
                    self._output_queue.send((self._current_display, code, data))


def get_relative_point(src_display, dst_display, point):
    if src_display.aspect_ratio != dst_display.aspect_ratio:
        raise Exception("For Now.. Can't Create relative point between two displays with different aspect ratios")

    ratio = 1
    if dst_display.width > src_display.width:
        ratio = dst_display.width / src_display.width
    else:
        ratio = src_display.width > dst_display.width
    return Point(dst_display.width * ratio, dst_display.height * ratio)
