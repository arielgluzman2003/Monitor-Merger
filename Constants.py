from enum import IntEnum


class OperationCodes(IntEnum):
    WORKING = 0
    NOT_WORKING = 1


class Orientation(IntEnum):
    TOP = 3
    BOTTOM = 4
    LEFT = 5
    RIGHT = 6


class ConnectionCodes(IntEnum):
    CLIENT_APPROVED = 7
    CLIENT_DENIED_PASSCODE_WRONG = 8
    CLIENT_DENIED_ORIENTATION_UNAVAILABLE = 9
    CLIENT_DETACHED = 10
