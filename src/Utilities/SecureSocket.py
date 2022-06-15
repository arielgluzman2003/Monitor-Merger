'''
secure-sockets v2.0
Author: Ariel Gluzman
Date: January 17th 2022
'''
import socket
from typing import Optional

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes as generate_key
from Crypto.Cipher import AES
import pickle
import rsa


def _construct(copy_socket, aes_object):
    new_socket = SecureSocket()
    new_socket._socket = copy_socket
    new_socket._aes = aes_object
    new_socket._acceptor = False
    return new_socket


class SecureSocket:

    def __init__(self, family=socket.AF_INET, socktype=socket.SOCK_STREAM, blocksize=32):
        self._address_family = family
        self._socket_type = socktype
        self._aes = None
        self._symmetric_key = -1
        self._blocksize = blocksize
        self._private_key = None
        self._public_key = None
        self._acceptor = -1
        self._socket = socket.socket(family, socktype)
        self.allow_address_reuse()

    def allow_address_reuse(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, arguments):
        if int(self._acceptor) == -1:  # Socket orientation not yet defined, used at first call.
            self._acceptor = True
        if not self._acceptor:
            raise SecureSocketException("Socket is not an 'Acceptor' type, cannot use function 'bind()'")

        self._public_key, self._private_key = rsa.newkeys(512)  # generating RSA public, private keys

        if type(arguments) not in (tuple, list):
            raise TypeError('argument given is not a tuple/string.')
        if len(arguments) != 2:
            raise ValueError("'arguments' variable has to contain 2 values, you gave %s " % len(arguments))

        ip, port = arguments[0], arguments[1]  # Extracting ip and port arguments
        '''
        :param ip: address in IPv4 Format, of interface to bind to.
        :param port: 0-65535, avoid using anywhere between 0-1024, especially the commonly used ports
            commonly used ports: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports
        '''
        if type(ip) is not str:
            raise ValueError("IP value given is invalid %s is not 'str'." % ip)
        if type(port) is not int:
            raise ValueError("PORT value given is invalid %s is not 'int'." % port)

        self._socket.bind((ip, port))  # Bind Socket to Address 'ip' and port 'port'

    def listen(self, backlog):

        if not self._acceptor:
            raise SecureSocketException("Socket is not an 'Acceptor' type, cannot use function 'listen()'")

        '''
        setting maximum client connection request queue length
        :param backlog (int) - Number of maximum who can be accepted before server starts dropping requests
        '''
        if type(backlog) is not int:
            raise TypeError("argument must be of type 'str' not %s." % type(backlog))
        self._socket.listen(backlog)

    def accept(self):
        if not self._acceptor:
            raise SecureSocketException("Socket is not an 'Acceptor' type, cannot use function 'accept()'")

        '''establishing connection, getting AES symmetric key and returning secureClient() for further use'''
        addr = None
        try:
            client_socket, addr = self._socket.accept()
        except socket.error as e:
            raise socket.error('An Error Occurred while trying to receive connection .' + e)
        pickled_pubkey = pickle.dumps(self._public_key)  # turning object into byte-array
        client_socket.send(pickled_pubkey)  # sending public key to client
        encrypted_symkey = client_socket.recv(4000)  # receiving an encrypted byte array of the symmetric key
        symmetric_key = rsa.decrypt(encrypted_symkey, self._private_key)  # decrypting byte array for symmetric key

        return _construct(client_socket, AES.new(symmetric_key, AES.MODE_ECB)), addr

    def connect(self, arguments):
        if int(self._acceptor) == -1:  # Socket orientation not yet defined, used at first call.
            self._acceptor = False
        if self._acceptor:
            raise SecureSocketException("Socket is an 'Acceptor' type, cannot use function 'connect()'")

        if type(arguments) not in (tuple, list):
            raise TypeError('argument given is not a tuple or list')
        if not len(arguments) == 2:
            raise ValueError('Arguments Error. secureClient requires 2-3 arguments, %s were given.' % len(arguments))

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

        self._symmetric_key = generate_key(self._blocksize)  # generates blocksize i.e 32 random bytes for symmetric key
        self._aes = AES.new(self._symmetric_key, AES.MODE_ECB)  # Crypto.Cipher.AES for encryption with symmetric key
        try:
            self._socket.connect((ip, port))
        except socket.error as e:
            raise SecureSocketException('An error occurred while trying to connect to server: ' + e.__str__())
        pickled_pubkey = self._socket.recv(4000)  # receives public key object as byte-array
        public_key = pickle.loads(pickled_pubkey)  # loads public key byte-array object
        self._socket.send(rsa.encrypt(self._symmetric_key, public_key))  # sends encrypted symmetric key

    def send(self, plaintext):
        if self._acceptor:
            raise SecureSocketException("Socket is an 'Acceptor' type, cannot use function 'send()'")
        '''
        :param plaintext: byte-array to be send
        :return: None
        padding data, adding its character length, and character-length length, encrypting and sending.
        for messsage b'hello', text=b'hello', len='5', len-of-len='1': b'15hello'
        that way client knows how much to receive, and can differentiate between messages.
        in this case message can load up to about 10mb.
        '''
        try:
            message = pad(plaintext, self._blocksize)  # max size 10mb
            length = str(len(message))  # max 9 characters
            len_of_length = str(len(length))  # max 1 character
            self._socket.send((len_of_length + length).encode() + self._aes.encrypt(message))
        except socket.error:
            raise SecureSocketException("Error Receiving Message")

    def recv(self):
        if self._acceptor:
            raise SecureSocketException("Socket is an 'Acceptor' type, cannot use function 'recv()'")
        '''
        :return: plain-text byte array
        gets length of length-of-data, length-of-data, and data.
        '''
        try:
            len_of_length = int(self._socket.recv(1).decode())
            length = int(self._socket.recv(len_of_length).decode())
            return unpad(self._aes.decrypt(self._socket.recv(length)), self._blocksize)
        except socket.error:
            raise SecureSocketException("Error Receiving Message")

    def close(self):
        self._socket.close()

    def gettimeout(self) -> Optional[float]:
        return self._socket.gettimeout()

    def settimeout(self, value: Optional[float]):
        self._socket.settimeout(value)

    def setblocking(self, flag: bool):
        self._socket.setblocking(flag)


class SecureSocketException(Exception):
    '''
    Raised When an Exception Regarding SecureSocket's Occurs
    Used like socket.error
    '''

    def __init__(self, message):
        super(SecureSocketException, self).__init__(message)
