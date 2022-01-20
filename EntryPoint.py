import ctypes
from multiprocessing import Queue, Value
from Logic.logic import Logic
from Graphic.Monitor import Monitor
from Input.input import Input
from Communication.communication import Communication
from Utilities.channel import OneWayChannel, TwoWayChannel
from Constants import OperationCodes


def main():
    current_monitor = Monitor()

    input_queue = OneWayChannel(queue=Queue())  # Inter-Process Shared Resource with Form of Queue
    output_queue = OneWayChannel(queue=Queue())  # Inter-Process Shared Resource with Form of Queue

    direction_a = OneWayChannel(queue=Queue())
    direction_b = OneWayChannel(queue=Queue())
    logic_client_handle_channel = TwoWayChannel(in_queue=direction_a, out_queue=direction_b)
    communication_client_handle_channel = TwoWayChannel(in_queue=direction_b, out_queue=direction_a)

    operation_code = Value('i',
                           OperationCodes.WORKING)  # Inter-Process Shared Resource with Form of Integer Value

    logical_process = Logic(input_queue=input_queue,
                            output_queue=output_queue,
                            client_handle_channel=logic_client_handle_channel,
                            operation_code=operation_code)

    input_process = Input(input_queue=input_queue,
                          operation_code=operation_code)

    communication_process = Communication(output_queue=output_queue,
                                          channel=communication_client_handle_channel,
                                          operation_code=operation_code)

    logical_process.start()
    input_process.start()
    communication_process.start()

    communication_process.join()
    input_process.join()
    logical_process.join()


if __name__ == '__main__':
    main()
