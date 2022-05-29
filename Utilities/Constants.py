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


class ActionCodes(IntEnum):
    NEW_POSITION = 12
    LEFT_CLICK = 13
    MIDDLE_CLICK = 14
    RIGHT_CLICK = 15
    LEFT_RELEASE = 16
    MIDDLE_RELEASE = 17
    RIGHT_RELEASE = 18
    SCROLL = 19
    DRAG = 20

class WindowCodes(IntEnum):
    RUNNING = 21
    NOT_RUNNING = 22