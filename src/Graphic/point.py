'''
author: Ariel Gluzman
date: 2022
email: ariel.gluzman@gmail.com
'''

from screeninfo.common import Monitor


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(
                "Error trying to compare values of different types - {type1} can't be compared with {type2}.".format(
                    type1=type(self), type2=type(other)))

    def __ne__(self, other):
        return not self.__eq__(other)

    def set_relative(self, this: Monitor, other: Monitor):
        '''
        Given 'this' is monitor on which Point in native to,
        sets Point to its relative on monitor 'other'
        '''

        this_width, this_height = this.width, this.height
        other_width, other_height = other.width, other.height
        self.x = int((float(self.x) / this_width) * other_width)
        self.y = int((float(self.y) / this_height) * other_height)

    def get_relative(self, this: Monitor, other: Monitor):
        this_width, this_height = this.width, this.height
        other_width, other_height = other.width, other.height
        return Point(x=int((float(self.x) / this_width) * other_width),
                     y=int((float(self.y) / this_height) * other_height))

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)
