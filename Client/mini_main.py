import ctypes
import socket
from typing import Tuple
import Graphic.Display
import Utilities.SecureSocket
from Utilities.Constants import Orientation, ActionCodes
import pickle
import mouse
from Graphic.Point import Point
from pynput.mouse import Button

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
        print("aa")
    except:
        print("cant conect")
        exit(1)

    my_display = Graphic.Display.Display()

    client_socket.send(pickle.dumps((Orientation.TOP, passcode, my_display)))
    connection_code = client_socket.recv()

    if str(Utilities.Constants.ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE) == connection_code or str(
            Utilities.Constants.ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG) == connection_code:
        print("Cant Connect Something Went Wrong")
        exit(1)

    while True:
        action_code, data = pickle.loads(client_socket.recv())

        print(action_code, data)

        print(action_code, data)
        if action_code.value == ActionCodes.NEW_POSITION.value:
            # Data Is POINT
            data: Point
            x, y = data.x, data.y
            mouse.move(x, y, absolute=True)

        if action_code.value == ActionCodes.SCROLL.value:
            data: Tuple[int, int]
            dx, dy = data
            mouse.wheel(dy)

        elif action_code.value == ActionCodes.LEFT_CLICK.value:
            mouse.press('left')
        elif action_code.value == ActionCodes.LEFT_RELEASE.value:
            mouse.release('left')
        elif action_code.value == ActionCodes.RIGHT_CLICK.value:
            mouse.press('right')
        elif action_code.value == ActionCodes.RIGHT_RELEASE.value:
            mouse.release('right')
        elif action_code.value == ActionCodes.MIDDLE_CLICK.value:
            mouse.press('middle')
        elif action_code.value == ActionCodes.MIDDLE_RELEASE.value:
            mouse.release('middle')

if __name__ == '__main__':
    main("ABCDE")
