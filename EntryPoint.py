from multiprocessing import Queue, Value
from Processes.logic import Logic
from Graphic.Monitor import Monitor
from Processes.input import Input
from Processes.communication import Communication

OPERATION_CODE_WORKING = 0
OPERATION_CODE_NOT_WORKING = 1


def main():
    current_monitor = Monitor()
    input_queue = Queue()  # Inter-Process Shared Resource with Form of Queue
    output_queue = Queue()  # Inter-Process Shared Resource with Form of Queue
    operation_code = Value('i', OPERATION_CODE_WORKING)  # Inter-Process Shared Resource with Form of Integer Value
    logical_process = Logic(input_queue=input_queue,
                            output_queue=output_queue,
                            operation_code=operation_code)

    input_process = Input(input_queue=input_queue,
                          operation_code=operation_code)

    communication_process = Communication(output_queue=output_queue,
                                          channel=None,
                                          operation_code=None)

    logical_process.start()
    input_process.start()
    communication_process.start()

    communication_process.start()
    input_process.join()
    logical_process.join()


if __name__ == '__main__':
    main()
