from enum import IntEnum


class OperationCodes(IntEnum):
    WORKING = 0
    NOT_WORKING = 1


class Orientation(IntEnum):
    TOP = 3
    BOTTOM = 4
    LEFT = 5
    RIGHT = 6
    MAIN = 7


class ConnectionCodes(IntEnum):
    CLIENT_APPROVED = 8
    CLIENT_DENIED_PASSCODE_WRONG = 9
    CLIENT_DENIED_ORIENTATION_UNAVAILABLE = 10
    CLIENT_DETACHED = 11
    CONNECTION_ATTEMPT = 12


class ActionCodes(IntEnum):
    NEW_POSITION = 13
    MOUSE_CLICK = 14
    KEYBOARD_CLICK = 15
    SCROLL = 16
    DRAG = 17
    CLIPBOARD_APPEND = 18


class WindowCodes(IntEnum):
    RUNNING = 19
    NOT_RUNNING = 20
