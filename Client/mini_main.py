import ctypes
import socket
from typing import Tuple
from screeninfo.common import Monitor
from screeninfo import get_monitors
from Utilities.constants import Orientation, ActionCodes, ConnectionCodes
import pickle
from Graphic.point import Point
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from Utilities.SecureSocket import SecureSocket, SecureSocketException
from typing import List

PORT = 1234


def host_finder(subdomains: List[str], port=PORT):
    for subdomain in subdomains:
        if len(subdomain.split('.')) == 4:
            subdomain = '.'.join(subdomain.split('.')[:-1])  # Remove Last Octet
            subdomain += '.'
        for i in range(2, 256):
            client_socket = SecureSocket()
            default_timeout = client_socket.gettimeout()
            client_socket.settimeout(0.01)
            ip = subdomain + str(i)
            try:
                client_socket.connect((ip, PORT))
                client_socket.settimeout(default_timeout)
                return ip, client_socket
            except SecureSocketException:
                print(ip, '- Not A Host')
    return None, None


def main(passcode):
    subdomains = ['192.168.1.0', '10.0.2.0']
    address, client_socket = host_finder(subdomains)

    # client_socket = SecureSocket()
    # client_socket.connect((IP, PORT))

    if client_socket is None:
        print("Can't Connect")
        exit(1)

    my_display: Monitor

    for m in get_monitors():
        if m.is_primary:
            my_display = m

    _mouse = MouseController()
    _keyboard = KeyboardController()

    client_socket.send(pickle.dumps((Orientation.LEFT, ConnectionCodes.CONNECTION_ATTEMPT, (passcode, my_display))))
    connection_code = client_socket.recv()

    if str(ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE) == connection_code or str(
            ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG) == connection_code:
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
            # print(type(key))
            print(key)


if __name__ == '__main__':
    main("ABCDE")
