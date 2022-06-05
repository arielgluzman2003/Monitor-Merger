import ctypes
import socket
from typing import Tuple
from screeninfo.common import Monitor
from screeninfo import get_monitors
import Graphic.display
import Utilities.SecureSocket
from Utilities.constants import Orientation, ActionCodes, ConnectionCodes
import pickle
from Graphic.point import Point
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

PORT = 1234
IP = "192.168.1.118"


def ip_finder():
    client_socket = Utilities.SecureSocket.SecureSocket()
    client_socket.settimeout(1)
    ip = '192.168.1.'
    for i in range(2, 256):
        ip_new = ip + str(i)
        try:
            client_socket.connect((ip_new, PORT))
            print(ip_new)
        except:
            print('ip ' + ip_new + " is not available.")


def main(passcode):
    client_socket = Utilities.SecureSocket.SecureSocket()
    try:
        client_socket.connect((IP, PORT))
        print("Connected")
    except:
        print("cant conect")
        exit(1)

    my_display: Monitor

    for m in get_monitors():
        if m.is_primary:
            my_display = m

    _mouse = MouseController()
    _keyboard = KeyboardController()

    client_socket.send(pickle.dumps((Orientation.LEFT, ConnectionCodes.CONNECTION_ATTEMPT, (passcode,my_display))))
    connection_code = client_socket.recv()

    if str(Utilities.constants.ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE) == connection_code or str(
            Utilities.constants.ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG) == connection_code:
        print("Cant Connect Something Went Wrong")
        exit(1)

    while True:
        action_code, data = pickle.loads(client_socket.recv())

        if action_code.value == ActionCodes.NEW_POSITION.value:
            # Data Is POINT
            data: Point
            x, y = data.x, data.y
            _mouse.position = x, y

        if action_code.value == ActionCodes.SCROLL.value:
            data: Tuple[int, int]
            dx, dy = data
            print(action_code, dx, dy)
            _mouse.scroll(dx, dy)

        elif action_code.value == ActionCodes.MOUSE_CLICK.value:
            button, pressed = data
            print(button, pressed)
            if pressed:
                _mouse.press(button)
            else:
                _mouse.release(button)

        elif action_code.value == ActionCodes.KEYBOARD_CLICK.value:
            key, pressed = data
            print(key, pressed)
            if pressed:
                _keyboard.press(key)
            else:
                _keyboard.release(key)
            #print(type(key))
            print(key)


if __name__ == '__main__':
    main("ABCDE")
