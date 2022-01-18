'''
Author: Arie Gluzman
Creation Date: 1.12.2020

class secureClient():
    an encapsulation of RSA key transfer, AES encryption and socket connection and function.
    by using connect(), send() and receive() the user is implementing all three components.
'''

from Crypto.Random import get_random_bytes as generate_key
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pickle import loads as pickle_loads
import rsa
import socket

default_blocksize = 32


class secureClient:

    def __init__(self, net_protocol=socket.AF_INET, transport_protocol=socket.SOCK_STREAM):
        # defaults are set to an IPv4, TCP socket. Encryption Block-Size 32
        self._client_socket = socket.socket(net_protocol, transport_protocol)

    def connect(self, arguments):
        if type(arguments) not in (tuple, list):
            raise Exception('argument given is not a tuple or list')
        if not len(arguments) == 2:
            raise Exception('Arguments Error. secureClient requires 2-3 arguments, %s were given.' % len(arguments))

        ip, port = arguments[0], arguments[1]
        '''
        :param ip:
        :param port:
        :return:
        '''
        if type(ip) is not str:
            raise ValueError("IP value given is invalid %s is not 'str'." % ip)
        if type(port) is not int:
            raise ValueError("PORT value given is invalid %s is not 'int'." % port)
        self._ip = ip
        self._port = port
        self._blocksize = default_blocksize
        self._symmetric_key = generate_key(self._blocksize)  # generates blocksize i.e 32 random bytes for symmetric key
        self._aes = AES.new(self._symmetric_key, AES.MODE_ECB)  # Crypto.Cipher.AES for encryption with symmetric key
        try:
            self._client_socket.connect((self._ip, self._port))
        except socket.error as e:
            raise socket.error('An error occurred while trying to connect to server: ' + e)
        pickled_pubkey = self._client_socket.recv(4000)  # receives public key object as byte-array
        public_key = pickle_loads(pickled_pubkey)  # loads public key byte-array object
        self._client_socket.send(rsa.encrypt(self._symmetric_key, public_key))  # sends encrypted symmetric key

    def copy_constructor(self, client_socket, symkey):
        '''
        :param client_socket:
        :param symkey:
        used when socket and symmetric key are given before-hand and not by using connect()
        used at server after which receives symmetric key from client
        :return: None
        '''
        self._client_socket = client_socket
        self._symmetric_key = symkey
        self._blocksize = default_blocksize
        self._started = True
        self._aes = AES.new(self._symmetric_key, AES.MODE_ECB)

    def send(self, bytes):
        '''
        :param bytes: byte-array to be send
        :return: None

        padding data, adding its character length, and character-length length, encrypting and sending.
        for messsage b'hello', text=b'hello', len='5', len-of-len='1': b'15hello'
        that way client knows how much to receive, and can differentiate between messages.
        in this case message can load up to about 10mb.
        '''
        message = pad(bytes, self._blocksize)  # max size 10mb
        length = str(len(message))  # max 9 characters
        len_of_length = str(len(length))  # max 1 character
        self._client_socket.send((len_of_length + length).encode() + self._aes.encrypt(message))

    def recv(self):
        '''
        :return: plain-text byte array
        gets length of length-of-data, length-of-data, and data.
        '''
        len_of_length = int(self._client_socket.recv(1).decode())
        length = int(self._client_socket.recv(len_of_length).decode())
        return unpad(self._aes.decrypt(self._client_socket.recv(length)), self._blocksize)

    def close(self):  # used at the end of use
        self._client_socket.close()