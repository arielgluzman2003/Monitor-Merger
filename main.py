import sys
import pickle
import pynput
from Utilities.SecureSocket import SecureSocket
from Utilities.Constants import *
from Graphic import Point
from Graphic.Monitor import current_monitor_dimensions, Monitor
import mouse

def scan_local(start, end, port) -> SecureSocket:
    addresses = ('192.168.1.' + str(host) for host in range(start, end))
    sock = None

    for address in addresses:
        try:
            sock = SecureSocket()
            sock.connect((address, port), timeout=0.005)
            return sock
        except:
            print("Host '{}' Down, Trying Next Address..".format(address))


def main():
    # print("Enter Passcode: ", end='')
    # passcode = input()

    # print("Enter Orientation", end='')
    # orientation = input()

    passcode = 'ABCDE'
    orientation = 'LEFT'
    width, height = current_monitor_dimensions()
    monitor = Monitor(width=width, height=height)

    controller = pynput.mouse.Controller()

    if orientation.upper() == 'LEFT':
        orientation = Orientation.LEFT
    elif orientation.upper() == 'RIGHT':
        orientation = Orientation.RIGHT
    elif orientation.upper() == 'TOP':
        orientation = Orientation.TOP
    elif orientation.upper() == 'BOTTOM':
        orientation = Orientation.BOTTOM

    sock = scan_local(2, 254, 1234)
    sock.send(pickle.dumps((orientation, passcode, monitor)))
    code = ConnectionCodes(int(sock.recv().decode()))

    if code is ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG:
        print("You Entered The Wrong Passcode")
    elif code is ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE:
        print("Password is Correct, But Orientation is Unavailable")
    elif code is ConnectionCodes.CLIENT_APPROVED:
        print("You've Been Approved")

    while code is ConnectionCodes.CLIENT_APPROVED:
        action, data = pickle.loads(sock.recv())

        if action is ActionCodes.NEW_POSITION:
            x, y = data.get_position()
            print("(x:{}, y:{})".format(x, y))
            controller.position = (x,y)
        if action is ActionCodes.LEFT_CLICK:
            controller.click(button=pynput.mouse.Button.left)
        if action is ActionCodes.RIGHT_CLICK:
            controller.click(button=pynput.mouse.Button.right)
        if action is ActionCodes.MIDDLE_CLICK:
            controller.click(button=pynput.mouse.Button.middle)

        if action is ActionCodes.LEFT_CLICK:
            controller.release(button=pynput.mouse.Button.left)
        if action is ActionCodes.RIGHT_CLICK:
            controller.release(button=pynput.mouse.Button.right)
        if action is ActionCodes.MIDDLE_CLICK:
            controller.release(button=pynput.mouse.Button.middle)

if __name__ == '__main__':
    main()
