''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''
import mouse
from pynput.mouse import Listener, Button
import pickle
from multiprocessing import Process
from Graphic.Point import Point
from Server.Input.MouseHandler import MouseHandler
from Utilities.Constants import OperationCodes
from Utilities.Constants import ActionCodes


class Input(Process):

    def __init__(self, input_queue, operation_code):
        super(Input, self).__init__()
        self._input_queue = input_queue
        self._operation_code = operation_code
        self.mouse = MouseHandler()
        self.last_position = self.mouse.get_position()

    def run(self) -> None:
        mouse_position = b''

        with Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll) as listener:
            listener.join()

    def _on_move(self, x, y):
        if self._operation_code.value != OperationCodes.NOT_WORKING and self._input_queue.writeable():
            # print(x, y)
            self._input_queue.send((ActionCodes.NEW_POSITION, Point(x=x, y=y)))

    def _on_click(self, x, y, button, pressed):
        if self._operation_code.value != OperationCodes.NOT_WORKING and self._input_queue.writeable():
            # print(x, y, button, pressed)
            if pressed:
                if button == Button.left:
                    self._input_queue.send((ActionCodes.LEFT_CLICK, ''))
                if button == Button.right:
                    self._input_queue.send((ActionCodes.RIGHT_CLICK, ''))
                if button == Button.middle:
                    self._input_queue.send((ActionCodes.MIDDLE_CLICK, ''))
            else:
                if button == Button.left:
                    self._input_queue.send((ActionCodes.LEFT_RELEASE, ''))
                if button == Button.right:
                    self._input_queue.send((ActionCodes.RIGHT_RELEASE, ''))
                if button == Button.middle:
                    self._input_queue.send((ActionCodes.MIDDLE_RELEASE, ''))

    def _on_scroll(self, x, y, dx, dy):
        if self._operation_code.value != OperationCodes.NOT_WORKING and self._input_queue.writeable():
            # print("{x}:{dx}, {y}:{dy}".format(x=x, dx=dx, y=y, dy=dy))
            self._input_queue.send((ActionCodes.SCROLL, (dx, dy)))
