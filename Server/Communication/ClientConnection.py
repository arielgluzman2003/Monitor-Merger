from threading import Thread
from Utilities.SecureSocket import SecureSocketException
from Utilities.Constants import ConnectionCodes
import pickle

class ClientConnection(Thread):
    def __init__(self, client_socket, channel):
        super(ClientConnection, self).__init__()
        self._socket = client_socket
        self._channel = channel
        self._active = True

    def run(self) -> None:
        while self._active:
            if self._channel.readable():
                try:
                    self._socket.send(pickle.dumps(self._channel.recv()))
                except SecureSocketException:
                    print("Client Disconnected")
                    self._channel.send(ConnectionCodes.CLIENT_DETACHED)
                    self._active = False
                    self._socket.close()
