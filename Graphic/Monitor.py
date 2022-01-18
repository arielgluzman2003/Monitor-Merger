import ctypes

# Commonly Used Screen Aspect Ratios, see https://en.wikipedia.org/wiki/Display_aspect_ratio
ASPECT_RATIOS = [(16, 10), (16, 9), (4, 3), (21, 9)]


def current_monitor_dimensions():
    '''
    
    :return: Dimensions of Monitor: (WIDTH, HEIGHT) 
    
    # NOTE:
        This function is implemented using the Windows API, thus,
        it will not be usable in a different platform i.e Linux, MacOs
        
        '''''
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)


def calculate_aspect_ratio(width, height):
    for ratio in ASPECT_RATIOS:
        if width / ratio[0] == height / ratio[1]:
            return ratio


class Monitor:
    def __init__(self, width=None, height=None):
        '''
        
        optional :param width: Unsigned Integer Value for custom WIDTH of a monitor
        optional :param height: Unsigned Integer Value for custom HEIGHT of a monitor
        
        object can't receive a single argument!
        if no arguments are given height and width will be 
        retrieved through 'current_monitor_dimensions()'        
        
        '''''

        if (width is None and height is not None) or (width is not None and height is None):
            raise ValueError("Too Few Arguments Given!")
        elif width is None and height is None:
            width, height = current_monitor_dimensions()

        self.width = width
        self.height = height

        self.aspect_ratio = calculate_aspect_ratio(width, height)
        if self.aspect_ratio is None:
            raise ValueError("Screen Dimensions ({}, {}) Deviate Formal Aspect Ratios".format(width, height))

    def get_dimensions(self):
        return self.width, self.height
