"""
author: Ariel Gluzman
date: 2022
email: ariel.gluzman@gmail.com
"""

from threading import Thread
from src.Utilities.SecureSocket import SecureSocketException, SecureSocket
from src.Utilities.constants import ConnectionCodes
import pickle
from src.Utilities.channel import UndirectedChannel
from datetime import datetime


class ClientConnection(Thread):
    def __init__(self, client_socket: SecureSocket, channel: UndirectedChannel):
        super(ClientConnection, self).__init__()
        self._socket = client_socket
        self._channel = channel
        self._active = True

    def run(self) -> None:
        while self._active:
            if self._channel.writeable():
                self._socket.setblocking(False)
                try:
                    message = self._socket.recv()
                    action_code, data = pickle.loads(message)
                    self._socket.setblocking(True)
                except (SecureSocketException, ValueError):
                    self._socket.setblocking(True)

            if self._channel.readable():
                try:
                    self._socket.send(pickle.dumps(self._channel.recv()))
                except SecureSocketException:
                    print("Client Disconnected")
                    self._channel.send((ConnectionCodes.CLIENT_DETACHED, datetime.now().strftime("%H:%M:%S")))
                    self._active = False
                    self._socket.close()
