"""
author: Ariel Gluzman
date: 2022
email: ariel.gluzman@gmail.com
"""

from threading import Thread
import socket
from typing import List
from Crypto.Cipher import AES
from os.path import exists, isfile, isdir, join
from src.Utilities.SecureSocket import _construct as construct_socket


def valid_new_file(path) -> bool:
    if not exists(path):
        return False

    return True


def valid_path(path) -> bool:
    # Extract Directory From File
    directory = '\\'.join(path.split('\\')[:-1])
    if not isdir(directory):
        return False
    return True


class sendfile(Thread):
    def __init__(self, port: int, key: bytes, path: str, buffersize=1000):
        self.buffersize = buffersize
        super().__init__()
        if not valid_new_file(path):
            raise ValueError('Path Given is Either Non-Existent or Is Not a File.')

        self.file_buffers: List[bytes] = []
        file_content = b''
        with open(path, 'rb') as f:
            file_content = f.read()

        cursor = 0
        while len(file_content) - cursor > buffersize:
            self.file_buffers.append(file_content[cursor: cursor + buffersize])
            cursor += buffersize
        self.file_buffers.append(file_content[cursor:])

        self.name = path.split('\\')[-1]
        self.size = len(self.name)

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(1)
        self.key = key

    def run(self) -> None:
        client_socket, _ = self.server_socket.accept()
        file_socket = construct_socket(copy_socket=client_socket, aes_object=AES.new(self.key, AES.MODE_ECB))
        file_socket.send(self.name.encode())
        file_socket.send(str(len(self.file_buffers)).encode())  # Iterations
        for buffer in self.file_buffers:
            file_socket.send(buffer)
        client_socket.close()


class recvfile(Thread):
    def __init__(self, default_path: str, key: bytes, port, ip):
        if not valid_path(default_path):
            raise ValueError('Path Given Is Either Not Existent or Not a Directory.')
        self.default_path = default_path
        super().__init__()
        self.key = key
        self.connection_properties = (port, ip)

    def run(self) -> None:
        client_socket = socket.socket()
        client_socket.connect(self.connection_properties)
        file_socket = construct_socket(client_socket, AES.new(self.key, AES.MODE_ECB))
        file_name = file_socket.recv().decode()
        iterations = int(file_socket.recv().decode())
        for _ in range(iterations):
            with open(join(self.default_path, file_name), 'ab') as f:
                buffer = file_socket.recv()
                f.write(buffer)
        file_socket.close()
