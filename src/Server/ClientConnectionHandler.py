import multiprocessing
from threading import Thread

import src.Utilities.channel
from src.Utilities.constants import Orientation, OperationCodes
from src.Utilities.channel import DirectedChannel, UndirectedChannel
from src.Server.ClientConnection import ClientConnection


class ClientConnectionHandler(Thread):
    def __init__(self, output_queue: DirectedChannel, channel: UndirectedChannel,
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
            if self._output_queue.readable():
                orientation, code, data = self._output_queue.recv()
                self._address_list[orientation].send((code, data))

            for client in self._address_list.keys():
                if self._address_list[client] is not None:
                    if self._address_list[client].readable():
                        code, data = self._address_list[client].recv()
                        self._channel.send((client, code, data))
                        print(client, code, data)


    def add_client(self, client_socket, orientation):
        channel_keep, channel_send = src.Utilities.channel.create(directed=False)
        self._address_list[orientation] = channel_keep
        self._children[orientation] = ClientConnection(client_socket=client_socket, channel=channel_send)
        self._children[orientation].start()
