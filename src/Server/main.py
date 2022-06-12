import string
from threading import Thread

from src.Server.communication import Communication
from src.Server.input import Input
from src.Server.logic import Logic
from src.Utilities.constants import OperationCodes
from src.Utilities.channel import DirectedChannel, UndirectedChannel
from multiprocessing import Value, Process
import src.Utilities.channel
import random

TITLE = "Display Merger"
SIZE = 5  # the smaller size the larger window
START = "Start"
STOP = "Stop"


def generate_code(letters=string.digits + string.ascii_letters, length=5):
    return ''.join(random.choice(letters) for i in range(length))


class Server(Thread):

    def __init__(self, code: str, operation_code: Value):
        super(Server, self).__init__()
        operation_code: Value
        input_queue: DirectedChannel
        output_queue: DirectedChannel
        logic_client_handle_channel: UndirectedChannel
        communication_client_handle_channel: UndirectedChannel
        logical_process: Process
        input_process: Process
        communication_process: Process

        self.operation_code = operation_code
        self.code = code

    def run(self) -> None:
        input_queue = src.Utilities.channel.create(directed=True)
        output_queue = src.Utilities.channel.create(directed=True)

        logic_client_handle_channel, communication_client_handle_channel = src.Utilities.channel.create(directed=False)

        logical_process = Logic(input_queue=input_queue,
                                output_queue=output_queue,
                                client_handle_channel=logic_client_handle_channel,
                                operation_code=self.operation_code,
                                passcode=self.code)

        input_process = Input(input_queue=input_queue,
                              operation_code=self.operation_code)

        communication_process = Communication(output_queue=output_queue,
                                              channel=communication_client_handle_channel,
                                              operation_code=self.operation_code)

        self.operation_code.value = OperationCodes.WORKING
        logical_process.start()
        input_process.start()
        communication_process.start()

        logical_process.join()
        input_process.join()
        communication_process.join()
