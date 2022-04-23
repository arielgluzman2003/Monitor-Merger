import ctypes
from platform import system

# Commonly Used Screen Aspect Ratios, see https://en.wikipedia.org/wiki/Display_aspect_ratio
ASPECT_RATIOS = [(16, 10), (16, 9), (4, 3), (21, 9)]


def _current_display_dimensions():
    '''
    
    :return: Dimensions of Display: (WIDTH, HEIGHT) 
    
    '''''

    if system() == 'Windows':
        return _windows_current_display_dimensions()
    if system() == 'Linux':
        return _linux_current_display_dimensions()


def _windows_current_display_dimensions():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)


def _linux_current_display_dimensions():
    raise NotImplementedError("Not Yet Set Implementation For Linux Machine")


def _calculate_aspect_ratio(width, height):
    for ratio in ASPECT_RATIOS:
        if width / ratio[0] == height / ratio[1]:
            return ratio
    return None


class Display:
    def __init__(self, width=None, height=None):
        '''
        
        optional :param width: Unsigned Integer Value for custom WIDTH of a display
        optional :param height: Unsigned Integer Value for custom HEIGHT of a display
        
        object can't receive a single argument!
        if no arguments are given height and width will be 
        retrieved through 'current_display_dimensions()'        
        
        '''''

        if (width is None and height is not None) or (width is not None and height is None):
            raise ValueError("Too Few Arguments Given!")
        elif width is None and height is None:
            width, height = _current_display_dimensions()

        self.width = width
        self.height = height

        self.aspect_ratio = _calculate_aspect_ratio(width, height)
        if self.aspect_ratio is None:
            raise ValueError("Screen Dimensions ({}, {}) Deviate Formal Aspect Ratios".format(width, height))

    def get_dimensions(self):
        return self.width, self.height
