import pickle

from Utilities.Constants import ConnectionCodes, OperationCodes, Orientation
from Utilities.SecureSocket import SecureSocket

IP = '127.0.0.1'
PORT = 1234
SERVER_INFO = (IP, PORT)


def main():
    sock = SecureSocket()
    sock.connect(SERVER_INFO)
    sock.send(pickle.dumps((Orientation.LEFT, 'ABCDE')))
    reply = sock.recv().decode()
    print(reply)
    if int(reply) == ConnectionCodes.CLIENT_APPROVED:
        print("YEEEEEEEEEEEEESAASSSSSSSSSSSSSSSSSS")


if __name__ == '__main__':
    main()
