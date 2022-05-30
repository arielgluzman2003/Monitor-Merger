from Server.Communication.communication import Communication
from Server.Input.input import Input
from Server.Logic.logic import Logic
from Utilities.constants import OperationCodes
from Utilities.channel import DirectedChannel, UndirectedChannel
from multiprocessing import Value, Process
import Utilities.channel
import random

TITLE = "Display Merger"
SIZE = 5  # the smaller size the larger window
START = "Start"
STOP = "Stop"


def generate_code(letters, length):
    return ''.join(random.choice(letters) for i in range(length))


def main(code):
    operation_code: Value
    input_queue: DirectedChannel
    output_queue: DirectedChannel
    logic_client_handle_channel: UndirectedChannel
    communication_client_handle_channel: UndirectedChannel
    logical_process: Process
    input_process: Process
    communication_process: Process

    operation_code = Value('i', OperationCodes.NOT_WORKING)

    input_queue = DirectedChannel()
    output_queue = DirectedChannel()
    logic_client_handle_channel: UndirectedChannel
    communication_client_handle_channel: UndirectedChannel
    logic_client_handle_channel, communication_client_handle_channel = Utilities.channel.create(directed=False)

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

    operation_code.value = OperationCodes.WORKING
    logical_process.start()
    input_process.start()
    communication_process.start()

    logical_process.join()
    input_process.join()
    communication_process.join()


if __name__ == '__main__':
    # code_length = 5
    # passcode = generate_code(string.ascii_uppercase, code_length)
    passcode = "ABCDE"
    main(passcode)
