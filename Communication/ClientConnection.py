from threading import Thread


class ClientConnection(Thread):
    def __init__(self, client_socket, output_queue, client_information_channel):
        super(ClientConnection, self).__init__()
        self._socket = client_socket
        self._output_queue = output_queue
        self._channel = client_information_channel


    def run(self) -> None:

        while True:
            pass

    def detach_all(self):
        pass