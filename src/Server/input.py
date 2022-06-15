"""
author: Ariel Gluzman
date: 2022
email: ariel.gluzman@gmail.com
"""

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from multiprocessing import Process, Value
from src.Graphic.point import Point
from src.Utilities.constants import OperationCodes
from src.Utilities.constants import ActionCodes
from src.Utilities.channel import DirectedChannel


class Input(Process):

    def __init__(self, input_queue: DirectedChannel, operation_code: Value):
        super(Input, self).__init__()
        self._input_queue = input_queue
        self._operation_code = operation_code

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
            return False
            KeyboardListener.stop()

    # Keyboard Key-Release Event
    def _on_release(self, key):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.KEYBOARD_CLICK, (key, False)))
        else:
            return False
            KeyboardListener.stop()

    # Mouse-Move Event
    def _on_move(self, x, y):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.NEW_POSITION, Point(x=x, y=y)))
        else:
            return False
            MouseListener.stop()

    # Mouse-Click Event
    def _on_click(self, x, y, button, pressed):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.MOUSE_CLICK, (button, pressed)))
        else:
            return False
            MouseListener.stop()

    # Mouse Scroll Event
    def _on_scroll(self, x, y, dx, dy):
        if self.working():
            if self._input_queue.writeable():
                self._input_queue.send((ActionCodes.SCROLL, (dx, dy)))
        else:
            return False
            MouseListener.stop()

    def working(self):
        return self._operation_code.value != OperationCodes.NOT_WORKING
