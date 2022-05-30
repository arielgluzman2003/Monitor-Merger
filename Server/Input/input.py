''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''
import mouse
from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Listener as KeyboardListener, Key
import pickle
from multiprocessing import Process, Value
from Graphic.point import Point
from Server.Input.MouseHandler import MouseHandler
from Utilities.constants import OperationCodes
from Utilities.constants import ActionCodes
from Utilities.channel import DirectedChannel


class Input(Process):

    def __init__(self, input_queue: DirectedChannel, operation_code: Value):
        super(Input, self).__init__()
        self._input_queue = input_queue
        self._operation_code = operation_code
        self.mouse = MouseHandler()
        self.last_position = self.mouse.get_position()

    def run(self) -> None:
        mouse_position = b''

        mouseListener = MouseListener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        keyboardListener = KeyboardListener(
            on_press=self._on_press,
            on_release=self._on_release
        )

        mouseListener.start()
        keyboardListener.start()
        mouseListener.join()
        keyboardListener.join()

    # Keyboard Key-Press Event
    def _on_press(self, key):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.KEYBOARD_CLICK, (key, True)))
        else:
            KeyboardListener.stop()

    # Keyboard Key-Release Event
    def _on_release(self, key):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.KEYBOARD_CLICK, (key, False)))
        else:
            KeyboardListener.stop()

    # Mouse-Move Event
    def _on_move(self, x, y):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.NEW_POSITION, Point(x=x, y=y)))
        else:
            MouseListener.stop()

    # Mouse-Click Event
    def _on_click(self, x, y, button, pressed):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.MOUSE_CLICK, (button, pressed)))
        else:
            MouseListener.stop()

    # Mouse Scroll Event
    def _on_scroll(self, x, y, dx, dy):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.SCROLL, (dx, dy)))
        else:
            MouseListener.stop()

    def working(self):
        return self._operation_code.value != OperationCodes.NOT_WORKING
