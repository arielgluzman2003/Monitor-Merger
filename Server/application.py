import multiprocessing
from multiprocessing import Queue
from threading import Thread

from Server.Communication.communication import Communication
from Server.Input.input import Input
from Server.Logic.logic import Logic
from Utilities.constants import OperationCodes
from Utilities.channel import DirectedChannel, UndirectedChannel
import Utilities.channel

# class Mechanism(Thread):
class Mechanism:

    def __init__(self, operation_code: multiprocessing.Value):
        # super(Mechanism, self).__init__()
        self._active = False
        self.operation_code = operation_code
        self.operation_code.value = OperationCodes.WORKING

        self.logical_process = None
        self.input_process = None
        self.communication_process = None
        self.set_processes()

    def operation(self):
        if self._active:
            self.stop()
            self._active = False

        else:
            self.start()
            self._active = True

        if self._active:
            print("Now Active")
        else:
            print("Now Not Active")

    def start(self):
        self.operation_code.value = OperationCodes.WORKING
        self.logical_process.start()
        self.input_process.start()
        self.communication_process.start()

        self.logical_process.join()
        self.input_process.join()
        self.communication_process.join()

    def stop(self):
        self.operation_code.value = OperationCodes.NOT_WORKING
        self.set_processes()

    def set_processes(self):
        input_queue = DirectedChannel()  # Inter-Process Shared Resource with Form of Queue
        output_queue = DirectedChannel()  # Inter-Process Shared Resource with Form of Queue

        logic_client_handle_channel: UndirectedChannel
        communication_client_handle_channel: UndirectedChannel
        logic_client_handle_channel, communication_client_handle_channel = Utilities.channel.create(directed=False)

        self.logical_process = Logic(input_queue=input_queue,
                                     output_queue=output_queue,
                                     client_handle_channel=logic_client_handle_channel,
                                     operation_code=self.operation_code,
                                     passcode="ABCDE")

        self.input_process = Input(input_queue=input_queue,
                                   operation_code=self.operation_code)

        self.communication_process = Communication(output_queue=output_queue,
                                                   channel=communication_client_handle_channel,
                                                   operation_code=self.operation_code)
