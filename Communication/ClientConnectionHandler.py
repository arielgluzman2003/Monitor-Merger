from threading import Thread
from Constants import Orientation
import Constants
import pickle
from Utilities.channel import TwoWayChannel, OneWayChannel
from multiprocessing import Queue
from Communication.ClientConnection import ClientConnection

class ClientConnectionHandler(Thread):
    def __init__(self, output_queue, channel, operation_code):
        """
        :type output_queue: OneWayChannel
        :type client_information_channel: TwoWayChannel
        :type operation_code:

        """
        super(ClientConnectionHandler, self).__init__()
        self._output_queue = output_queue
        self._channel = channel
        self._operation_code = operation_code
        self._address_list = {Orientation.LEFT: None, Orientation.RIGHT: None,
                              Orientation.TOP: None, Orientation.BOTTOM: None}
        self._children = {Orientation.LEFT: None, Orientation.RIGHT: None,
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

    def add_client(self, client_socket, orientation):
        direction_a = OneWayChannel(queue=Queue())
        direction_b = OneWayChannel(queue=Queue())
        channel_keep = TwoWayChannel(in_queue=direction_a, out_queue=direction_b)
        channel_send = TwoWayChannel(in_queue=direction_b, out_queue=direction_a)
        self._address_list[orientation] = channel_keep
        self._children[orientation] = ClientConnection(client_socket=client_socket, channel=channel_send)
        self._children[orientation].start()
