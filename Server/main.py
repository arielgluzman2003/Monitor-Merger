import multiprocessing
from multiprocessing import Value, Queue, Process
from threading import Thread

from typing import List

from Graphic.Display import Display
from tkinter import *
import string
import random

from Server.Communication.communication import Communication
from Server.Input.input import Input
from Server.Logic.logic import Logic
from Server.application import Mechanism
from Utilities.Constants import OperationCodes
from Utilities.channel import TwoWayChannel, OneWayChannel

TITLE = "Display Merger"
SIZE = 5  # the smaller size the larger window
START = "Start"
STOP = "Stop"


def generate_code(letters, length):
    return ''.join(random.choice(letters) for i in range(length))


def main(code):
    # Inter-Process Shared Resource with Form of Integer Value
    operation_code = Value('i', OperationCodes.NOT_WORKING)

    current_display = Display()

    input_queue = OneWayChannel(queue=Queue())  # Inter-Process Shared Resource with Form of Queue
    output_queue = OneWayChannel(queue=Queue())  # Inter-Process Shared Resource with Form of Queue

    direction_a = OneWayChannel(queue=Queue())
    direction_b = OneWayChannel(queue=Queue())
    logic_client_handle_channel = TwoWayChannel(in_channel=direction_a, out_channel=direction_b)
    communication_client_handle_channel = TwoWayChannel(in_channel=direction_b, out_channel=direction_a)

    logical_process = Logic(input_queue=input_queue,
                            output_queue=output_queue,
                            client_handle_channel=logic_client_handle_channel,
                            operation_code=operation_code)

    input_process = Input(input_queue=input_queue,
                          operation_code=operation_code)

    communication_process = Communication(output_queue=output_queue,
                                          channel=communication_client_handle_channel,
                                          operation_code=operation_code)

    operation_code.value = OperationCodes.WORKING
    logical_process.start()
    input_process.start()
    communication_process.start()

    logical_process.join()
    input_process.join()
    communication_process.join()

    # m = Mechanism(_operation_code)
    #
    # _dimensions = current_display.get_dimensions()
    # _size = str(int(_dimensions[0] / SIZE)) + 'x' + str(int(_dimensions[1] / SIZE))
    #
    # window = Tk()
    # window.title(TITLE)
    # window.geometry(_size)
    #
    # _label_code_font = ("Arial", int(400 / SIZE))
    # _button_operation_font = ("Arial", int(200 / SIZE))
    #
    # _label_code = Label(window, text=code, font=_label_code_font)
    # _button_operation = Button(window, text=START,
    #                            font=_button_operation_font,
    #                            command=lambda: m.operation())
    #
    # _label_code.pack()
    # _button_operation.pack()
    #
    # window.mainloop()
    #


if __name__ == '__main__':
    # code_length = 5
    # passcode = generate_code(string.ascii_uppercase, code_length)
    passcode = "ABCDE"
    #
    main(passcode)
