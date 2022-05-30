import multiprocessing
from threading import Thread

from Utilities.constants import Orientation, OperationCodes
import pickle
import Utilities.channel
from Server.Communication.ClientConnection import ClientConnection


class ClientConnectionHandler(Thread):
    def __init__(self, output_queue: Utilities.channel.DirectedChannel, channel: Utilities.channel.UndirectedChannel,
                 operation_code: multiprocessing.Value):
        super(ClientConnectionHandler, self).__init__()
        self._output_queue = output_queue
        self._channel = channel
        self._operation_code = operation_code

        '''
        'address_list' is a dictionary that contains 'TwoWayChannel' objects used to
        communicate with child 'ClientConnection' Threads, which are in '_children'
        '''
        self._address_list = dict.fromkeys([Orientation.LEFT, Orientation.RIGHT,
                                            Orientation.TOP, Orientation.BOTTOM], None)

        '''
        '_children' contains child threads (ClientConnection)
        '''
        self._children = dict.fromkeys([Orientation.LEFT, Orientation.RIGHT,
                                        Orientation.TOP, Orientation.BOTTOM], None)

    def run(self) -> None:

        while self._operation_code.value != OperationCodes.NOT_WORKING:
            for display in self._address_list.keys():
                client = self._address_list[display]
                if client is not None:
                    if client.readable():
                        self._channel.send(pickle.dumps((display, client.recv(), '')))

            if self._output_queue.readable():
                orientation, code, data = self._output_queue.recv()
                self._address_list[orientation].send((code, data))

    def add_client(self, client_socket, orientation):
        channel_keep, channel_send = Utilities.channel.create(directed=False)
        self._address_list[orientation] = channel_keep
        self._children[orientation] = ClientConnection(client_socket=client_socket, channel=channel_send)
        self._children[orientation].start()
