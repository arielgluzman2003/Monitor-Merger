''''
Important Documentation
    Multiprocessing.Queue - https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue

'''''

IP = '0.0.0.0'
PORT = 1234
SERVER_INFO = (IP, PORT)
DEFAULT_LISTEN_QUEUE = 1

from multiprocessing import Process
from Network.secure_server import secureServer
from Network.secure_client import secureClient


class Communication(Process):

    def __init__(self, output_queue, channel, operation_code):
        super(Communication, self).__init__()
        self.output_queue = output_queue
        self.channel = channel
        self.operation_code = operation_code
        self.server_socket = secureServer()
        self.server_socket.bind(SERVER_INFO)
        self.server_socket.listen(DEFAULT_LISTEN_QUEUE)

