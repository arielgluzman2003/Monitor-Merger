''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''

from multiprocessing import Process
import Constants
from Communication.SecureSocket import SecureSocket
from Communication.ClientConnectionHandler import ClientConnectionHandler

IP = '0.0.0.0'
PORT = 1234
SERVER_INFO = (IP, PORT)
DEFAULT_LISTEN_QUEUE = 1


class Communication(Process):

    def __init__(self, output_queue, channel, operation_code):
        super(Communication, self).__init__()
        self._output_queue = output_queue
        self._channel = channel
        self._operation_code = operation_code
        self._server_socket = SecureSocket()
        self._server_socket.bind(SERVER_INFO)
        self._server_socket.listen(DEFAULT_LISTEN_QUEUE)

    def run(self) -> None:
        connections_handler = ClientConnectionHandler()
        while self._operation_code.value != Constants.OPERATION_CODE_NOT_WORKING:
            client_socket, addr = self._server_socket.accept()


        self._server_socket.close()
