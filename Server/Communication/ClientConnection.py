from threading import Thread


class ClientConnection(Thread):
    def __init__(self, client_socket, channel):
        super(ClientConnection, self).__init__()
        self._socket = client_socket
        self._channel = channel
        self._active = True

    def run(self) -> None:
        while self._active:
            if self._channel.readable():
                self._socket.send(self._channel.recv())
