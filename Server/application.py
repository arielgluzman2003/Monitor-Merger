import random
import string
import threading
from tkinter import Tk, Button, Label
from tkinter.font import Font
from multiprocessing import Value
from typing import List
from Server.Communication.communication import Communication
from Server.Input.input import Input
from Server.Logic.logic import Logic
from Utilities.constants import OperationCodes
from Utilities.channel import create


def generate_code(length: int, charset: str):
    code: str = ''
    for _ in range(length):
        code += charset[random.randint(0, len(charset) - 1)]
    return code


def start(operation_code: Value, code):
    input_queue = create(directed=True)
    output_queue = create(directed=True)

    logic_client_handle_channel, communication_client_handle_channel = create(directed=False)

    logical_process = Logic(input_queue=input_queue,
                            output_queue=output_queue,
                            client_handle_channel=logic_client_handle_channel,
                            operation_code=operation_code,
                            passcode=code)

    input_process = Input(input_queue=input_queue,
                          operation_code=operation_code)

    communication_process = Communication(output_queue=output_queue,
                                          channel=communication_client_handle_channel,
                                          operation_code=operation_code)

    logical_process.start()
    input_process.start()
    communication_process.start()


def button_start_clicked(button: Button, operation_code: Value, code):
    if operation_code.value == OperationCodes.WORKING:
        button['text'] = 'START'
        operation_code.value = OperationCodes.NOT_WORKING
    else:
        button['text'] = 'STOP'
        operation_code.value = OperationCodes.WORKING
        start(operation_code, code)


def main(code):
    operation_code = Value('i', OperationCodes.NOT_WORKING)
    window = Tk()
    window.geometry('500x500')
    code_label = Label(window, text=code, font=Font(family="Helvetica", size=60, weight="bold"), pady=100)
    code_label.pack()
    operation_button = Button(window, text='START',
                              font=Font(family="Helvetica", size=36, weight="bold"), bd=7, activebackground="#A0A0A0",
                              command=lambda: threading.Thread(target=button_start_clicked,
                                                               args=(operation_button, operation_code, code,)).start())
    operation_button.pack()

    window.mainloop()
    operation_code.value = OperationCodes.NOT_WORKING
    exit(0)


if __name__ == '__main__':
    #passcode = generate_code(5, string.digits + string.ascii_letters)
    passcode = 'ABCDE'
    main(passcode)
