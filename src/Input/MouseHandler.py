from src.Graphic.point import Point
import mouse


class MouseHandler:
    def __init__(self):
        pass

    def get_position(self):
        position = mouse.get_position()
        return Point(position[0], position[1])
