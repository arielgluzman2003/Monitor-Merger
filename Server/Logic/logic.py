''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
    
'''''
from multiprocessing import Process, Value

import clipboard
from pynput.mouse import Controller as MouseController
from screeninfo.common import Monitor
from screeninfo import get_monitors
from Graphic.point import Point
from Graphic.window import Window
from Utilities.channel import DirectedChannel, UndirectedChannel
from Utilities.constants import Orientation, OperationCodes, ConnectionCodes, ActionCodes

SCREEN_MARGIN = 2


class Logic(Process):
    def __init__(self, input_queue: DirectedChannel, output_queue: DirectedChannel,
                 client_handle_channel: UndirectedChannel, operation_code: Value, passcode: str):
        super(Logic, self).__init__()
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._client_handle_channel = client_handle_channel
        self._operation_code = operation_code
        self._passcode = passcode
        self._current_display = Orientation.MAIN
        self._main_display: Monitor
        for monitor in get_monitors():
            if monitor.is_primary:
                self._main_display = monitor
        self._displays = dict.fromkeys([Orientation.LEFT, Orientation.RIGHT,
                                        Orientation.TOP, Orientation.BOTTOM], None)
        self.mouse_controller = MouseController()

    def run(self) -> None:
        transparent_window = Window(operation_code=self._operation_code)
        transparent_window.start()

        while self.working():
            if self._client_handle_channel.readable():
                orientation, code, data = self._client_handle_channel.recv()
                if code == ConnectionCodes.CLIENT_DETACHED:
                    self._displays[orientation] = None
                    if self._current_display == orientation:
                        self._current_display = Orientation.MAIN
                        transparent_window.destroy()
                    print("Client", orientation, "Detached At", data)

                elif code == ConnectionCodes.CONNECTION_ATTEMPT:
                    passcode, client_display = data
                    if passcode == self._passcode:
                        if self._displays[orientation] is None:
                            self._client_handle_channel.send(ConnectionCodes.CLIENT_APPROVED)  # Accept Client
                            self._displays[orientation] = client_display
                            print(self._displays[orientation].width, self._displays[orientation].height)
                        else:
                            self._client_handle_channel.send(
                                ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE)  # Reject Client Due to
                            # Orientation Unavailable
                    else:
                        self._client_handle_channel.send(
                            ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG)  # Reject Client Due to Passcode Wrong

                elif code == ActionCodes.CLIPBOARD_APPEND:
                    clipboard.copy(data)
                    if self._output_queue.writeable():
                        for client in self._displays.keys():
                            if client != orientation:
                                self._output_queue.send((client, ActionCodes.CLIPBOARD_APPEND, data))

            if self._input_queue.readable():
                code, data = self._input_queue.recv()
                # print(code, data)
                if code is ActionCodes.NEW_POSITION:
                    data: Point

                    # Check For Screen Changes
                    if self._current_display == Orientation.MAIN:
                        if data.x < SCREEN_MARGIN:
                            if self._displays[Orientation.LEFT] is not None:
                                self._current_display = Orientation.LEFT
                                transparent_window.wake()
                                self.mouse_controller.position = self._main_display.width - SCREEN_MARGIN, data.y
                        if data.x > self._main_display.width - SCREEN_MARGIN:
                            if self._displays[Orientation.RIGHT] is not None:
                                self._current_display = Orientation.RIGHT
                                self._input_queue.send((ActionCodes.NEW_POSITION, Point(x=SCREEN_MARGIN, y=data.y)))
                                self.mouse_controller.position = SCREEN_MARGIN, data.y
                                transparent_window.wake()
                        if data.y < SCREEN_MARGIN:
                            if self._displays[Orientation.TOP] is not None:
                                self._current_display = Orientation.TOP
                                self.mouse_controller.position = data.x, self._main_display.height - SCREEN_MARGIN
                                transparent_window.wake()
                        if data.y > self._main_display.height - SCREEN_MARGIN:
                            if self._displays[Orientation.BOTTOM] is not None:
                                self._current_display = Orientation.BOTTOM
                                self.mouse_controller.position = data.x, SCREEN_MARGIN
                                transparent_window.wake()
                    elif self._current_display == Orientation.RIGHT:
                        if data.x < SCREEN_MARGIN:
                            self._current_display = Orientation.MAIN
                            self.mouse_controller.position = self._main_display.width - SCREEN_MARGIN, data.y
                            transparent_window.destroy()
                    elif self._current_display == Orientation.LEFT:
                        if data.x > self._main_display.width - SCREEN_MARGIN:
                            transparent_window.destroy()
                            self._input_queue.clear()
                            self._current_display = Orientation.MAIN
                            self.mouse_controller.position = SCREEN_MARGIN, data.y
                    elif self._current_display == Orientation.TOP:
                        if data.y > self._main_display.height - SCREEN_MARGIN:
                            self._current_display = Orientation.MAIN
                            self.mouse_controller.position = data.x, SCREEN_MARGIN
                            transparent_window.destroy()
                    elif self._current_display == Orientation.BOTTOM:
                        if data.y < SCREEN_MARGIN:
                            self._current_display = Orientation.MAIN
                            self.mouse_controller.position = data.x, self._main_display.height - SCREEN_MARGIN
                            transparent_window.destroy()

                    if self._current_display != Orientation.MAIN:
                        data.set_relative(self._main_display, self._displays[self._current_display])

                if code is ActionCodes.CLIPBOARD_APPEND:
                    if self._current_display == Orientation.MAIN:
                        if self._output_queue.writeable():
                            for client in self._displays.keys():
                                self._output_queue.send((client, ActionCodes.CLIPBOARD_APPEND, data))

                if self._current_display != Orientation.MAIN:
                    if code in (ActionCodes.NEW_POSITION, ActionCodes.MOUSE_CLICK,
                                ActionCodes.SCROLL, ActionCodes.KEYBOARD_CLICK):
                        self._output_queue.send((self._current_display, code, data))

    def working(self):
        return self._operation_code.value != OperationCodes.NOT_WORKING
