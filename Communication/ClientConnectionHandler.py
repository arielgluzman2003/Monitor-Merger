from threading import Thread


class ClientConnectionHandler(Thread):
    def __init__(self, output_queue, client_information_channel):
        super(ClientConnectionHandler, self).__init__()
        self._output_queue = output_queue
        self._channel = client_information_channel
        self.address

    def run(self) -> None:
        while True:
            pass
        self._socket.close()