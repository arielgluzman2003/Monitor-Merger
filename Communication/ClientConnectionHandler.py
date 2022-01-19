from threading import Thread
from Constants import Orientation
import Constants
import pickle

class ClientConnectionHandler(Thread):
    def __init__(self, output_queue, client_information_channel, operation_code):
        super(ClientConnectionHandler, self).__init__()
        self._output_queue = output_queue
        self._channel = client_information_channel
        self._operation_code = operation_code
        self._address_list = {Orientation.LEFT: None, Orientation.RIGHT: None,
                              Orientation.TOP: None, Orientation.BOTTOM: None}

    def run(self) -> None:
        while self._operation_code.value != Constants.OPERATION_CODE_NOT_WORKING:
            for client in self._address_list.values():
                if client is not None:
                    if client.readable():
                        self._channel.send(client.recv())
            if self._output_queue.readable():
                orientation, point = pickle.loads(self._output_queue.recv())
                self._address_list[orientation].send(pickle.dumps(point))


    def add_client(self, client_socket, Orientation):
        pass
