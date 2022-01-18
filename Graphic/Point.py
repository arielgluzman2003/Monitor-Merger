class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    # https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(
                "Error trying to compare values of different types - {type1} can't be compared with {type2}.".format(
                    type1=type(self), type2=type(other)))

    def __ne__(self, other):
        return not self.__eq__(other)
