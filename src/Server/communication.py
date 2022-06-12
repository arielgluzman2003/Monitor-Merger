''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''

import time
from multiprocessing import Process, Value
from src.Utilities.SecureSocket import SecureSocket
from src.Server.ClientConnectionHandler import ClientConnectionHandler
import pickle
from src.Utilities.constants import OperationCodes
from src.Utilities.constants import ConnectionCodes
from src.Utilities.channel import DirectedChannel, UndirectedChannel
from typing import List
from threading import Thread

IP = '0.0.0.0'
PORT = 1234
SERVER_INFO = (IP, PORT)
DEFAULT_CLIENTS = 4


class Communication(Process):

    def __init__(self, output_queue: DirectedChannel, channel: UndirectedChannel, operation_code: Value):
        super(Communication, self).__init__()
        self._output_queue = output_queue
        self._channel = channel
        self._operation_code = operation_code
        self._server_socket = SecureSocket()
        self._server_socket.bind(SERVER_INFO)
        self._server_socket.listen(DEFAULT_CLIENTS)
        self._connections: List[Thread] = []

    def run(self) -> None:
        connections_handler = ClientConnectionHandler(output_queue=self._output_queue,
                                                      channel=self._channel,
                                                      operation_code=self._operation_code)
        connections_handler.start()

        while self.working():
            if len(self._connections) < DEFAULT_CLIENTS:
                self._connections.append(Thread(target=self.accept, args=(connections_handler,)))
                self._connections[-1].start()

            for i in range(len(self._connections)):
                if not self._connections[i].is_alive():
                    del self._connections[i]
                    break
            time.sleep(2)
        self._server_socket.close()
        print("Socket Closed")

    def accept(self, connections_handler: ClientConnectionHandler):
        client_socket, addr = self._server_socket.accept()
        client_approval_attempt = pickle.loads(client_socket.recv())
        self._channel.send(client_approval_attempt)
        reply = self._recvblocking(attempts=100)
        client_socket.send(str(reply.value).encode())
        if reply == ConnectionCodes.CLIENT_APPROVED:
            orientation, _, _ = client_approval_attempt
            connections_handler.add_client(client_socket=client_socket, orientation=orientation)

    def working(self):
        return self._operation_code.value != OperationCodes.NOT_WORKING

    def _recvblocking(self, attempts, delay=0.01):
        attempt_counter = 0
        while attempt_counter <= attempts:
            if self._channel.readable():
                return self._channel.recv()
            time.sleep(delay)
        return b'Message Not Received'
