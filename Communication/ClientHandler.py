from threading import Thread


class ClientHandler(Thread):
    def __init__(self, client_socket, output_queue, client_information_channel):
        super(ClientHandler, self).__init__()
        self._socket = client_socket
        self._output_queue = output_queue
        self._channel = client_information_channel

    def run(self) -> None:
        while True:
            pass
        self._socket.close()