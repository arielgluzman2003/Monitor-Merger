import multiprocessing
from threading import Thread
from typing import Tuple
from screeninfo.common import Monitor
from screeninfo import get_monitors
from src.Utilities.constants import Orientation, ActionCodes, ConnectionCodes, OperationCodes
import pickle
from src.Graphic.point import Point
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from src.Utilities.SecureSocket import SecureSocket, SecureSocketException
from typing import List


class Client(Thread):

    def __init__(self, client_socket: SecureSocket, operation_code: multiprocessing.Value):
        super().__init__()
        self.client_socket = client_socket
        self.operation_code = operation_code
        self._mouse = MouseController()
        self._keyboard = KeyboardController()

    def run(self) -> None:

        while self.running():
            action_code, data = pickle.loads(self.client_socket.recv())

            if action_code.value == ActionCodes.NEW_POSITION.value:
                # Data Is POINT
                data: Point
                x, y = data.x, data.y
                self._mouse.position = x, y

            if action_code.value == ActionCodes.SCROLL.value:
                data: Tuple[int, int]
                dx, dy = data
                print(action_code, dx, dy)
                self._mouse.scroll(dx, dy)

            elif action_code.value == ActionCodes.MOUSE_CLICK.value:
                button, pressed = data
                print(button, pressed)
                if pressed:
                    self._mouse.press(button)
                else:
                    self._mouse.release(button)

            elif action_code.value == ActionCodes.KEYBOARD_CLICK.value:
                key, pressed = data
                print(key, pressed)
                if pressed:
                    self._keyboard.press(key)
                else:
                    self._keyboard.release(key)
                print(key)

    def running(self):
        return self.operation_code.value != OperationCodes.NOT_WORKING.value
