'''
8 October 2021
author: Ariel Gluzman (ariel.gluzman@gmail.com)

About:
	class secureServer implements RSA encryption method using Pycrypto, rsa and pickle tools.
	secureServer follows the usage of network sockets of the higher layer-hierarchy, identically,
	the return values, and functionality its values remind of those of the default 'socket' library.
	->	i.e. to bind() the socket, listen(), and accept() a client connection.
	
	with that being said the major difference apart from the encryption, that is mentioned previously,
	is that server and client have two different classes, which are one at default 'socket' library,
	therefore an important thing to notice while using secureServer is that the return-type that is
	returned with 'secureServer.accept()' is a 'secureClient()'.
	
	'secureServer()' is merely a tool for connecting to clients with an addition of the RSA protocol,
	after recieving an encryption key from client, it immediately returns a 'secureClient()',
	and waits for as many clients defined to be able to at 'secureServer.listen()'
	
	**Warning: secure_sockets(secureServer/secureClient) use AES mode ECB, which deficiency is encryption
	of pictures which can still be understood post encryption, therefore 'secure_sockets' should not be
	used for encryption of photos.	
'''

from secure_client import secureClient
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pickle import dumps as pickle_dumps
import rsa
import socket


class secureServer:

    def __init__(self, net_protocol=socket.AF_INET, transport_protocol=socket.SOCK_STREAM, blocksize=32):

        #defaults are set to an IPv4 address, Stream-Socket(TCP).
        #Encryption Block-Size 32 (block encryption with AES)


        self._server_socket = socket.socket(net_protocol, transport_protocol)
        self._public_key, self._private_key = rsa.newkeys(512)  # generating RSA public, private keys
        self._blocksize = blocksize
        self._aes = None

    def bind(self, arguments):
        if type(arguments) not in (tuple, list):
            raise TypeError('argument given is not a tuple/string.')
        ip, port = arguments[0], arguments[1]
        '''
        :param ip:
        :param port:
        '''
        if type(ip) is not str:
            raise ValueError("IP value given is invalid %s is not 'str'." % ip)
        if type(port) is not int:
            raise ValueError("PORT value given is invalid %s is not 'int'." % port)
        self._server_socket.bind((ip, port))

    def listen(self, clients):
        '''setting maximum client connection request queue length'''

        if type(clients) is not int:
            raise TypeError("argument must be of type 'str' not %s." % type(clients))
        self._server_socket.listen(clients)

    def accept(self):
        '''establishing connection, getting AES symmetric key and returning secureClient() for further use'''
        try:
            client_socket, addr = self._server_socket.accept()
        except socket.error as e:
            raise socket.error('An Error Occurred while trying to receive connection .' + e)
        pickled_pubkey = pickle_dumps(self._public_key)  # turning object into byte-array
        client_socket.send(pickled_pubkey)  # sending public key to client
        encrypted_symkey = client_socket.recv(4000)  # receiving an encrypted byte array of the symmetric key
        symmetric_key = rsa.decrypt(encrypted_symkey, self._private_key)  # decrypting byte array for symmetric key
        self._aes = AES.new(symmetric_key, AES.MODE_ECB)  # Crypto.Cipher.AES for encryption with symmetric key
        clt = secureClient()
        clt.copy_constructor(client_socket, symmetric_key)  # secure_client.secureClient with symmetric key and socket
        return clt

    def close(self):  # run at end of use
        self._server_socket.close()  # releasing file-descriptor related resources
