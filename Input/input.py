''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''

import pickle
from multiprocessing import Process
from Input.MouseHandler import MouseHandler

OPERATION_CODE_WORKING = 0
OPERATION_CODE_NOT_WORKING = 1


class Input(Process):

    def __init__(self, input_queue, operation_code):
        super(Input, self).__init__()
        self.input_queue = input_queue
        self.operation_code = operation_code
        self.mouse = MouseHandler()
        self.last_position = self.mouse.get_position()

    def run(self) -> None:
        mouse_position = b''
        while self.operation_code != OPERATION_CODE_NOT_WORKING:
            if not self.input_queue.full():
                mouse_position = self.mouse.get_position()
                if self.last_position != mouse_position:
                    self.input_queue.put(pickle.dumps(mouse_position))
                    self.last_position = mouse_position

