''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''

import time
from multiprocessing import Process, Value
from Utilities.SecureSocket import SecureSocket
from Server.Communication.ClientConnectionHandler import ClientConnectionHandler
import pickle
from Utilities.constants import OperationCodes
from Utilities.constants import ConnectionCodes
from Utilities.channel import DirectedChannel, UndirectedChannel


IP = '0.0.0.0'
PORT = 1234
SERVER_INFO = (IP, PORT)
DEFAULT_LISTEN_QUEUE = 1


class Communication(Process):

    def __init__(self, output_queue: DirectedChannel, channel: UndirectedChannel, operation_code: Value):
        super(Communication, self).__init__()
        self._output_queue = output_queue
        self._channel = channel
        self._operation_code = operation_code
        self._server_socket = SecureSocket()
        self._server_socket.bind(SERVER_INFO)
        self._server_socket.listen(DEFAULT_LISTEN_QUEUE)

    def run(self) -> None:
        connections_handler = ClientConnectionHandler(output_queue=self._output_queue,
                                                      channel=self._channel,
                                                      operation_code=self._operation_code)

        connections_handler.start()
        while self._operation_code.value != OperationCodes.NOT_WORKING:
            client_socket, addr = self._server_socket.accept()
            client_approval_attempt = pickle.loads(client_socket.recv())
            self._channel.send(client_approval_attempt)
            reply = self._recvblocking(attempts=100)
            client_socket.send(str(reply.value).encode())
            if reply == ConnectionCodes.CLIENT_APPROVED:
                orientation, _, _ = client_approval_attempt
                connections_handler.add_client(client_socket=client_socket, orientation=orientation)
        self._server_socket.close()

    def _recvblocking(self, attempts, delay=0.01):
        attempt_counter = 0
        while attempt_counter <= attempts:
            if self._channel.readable():
                return self._channel.recv()
            time.sleep(delay)
        return b'Message Not Received'
