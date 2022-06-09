import pickle

from src.Utilities.SecureSocket import SecureSocketException, SecureSocket
from tkinter import *
from tkinter import Text
from Graphic.display import Display
from src.Utilities.constants import Orientation

PORT = 1234
SIZE = 5


def find_peer(client_socket: SecureSocket, port):
    timeout = client_socket.gettimeout()
    client_socket.settimeout(0.01)
    addresses = ('192.168.1.' + str(octet) for octet in range(1, 256))
    for address in addresses:
        try:
            client_socket.connect((address, port))
            client_socket.settimeout(timeout)
            return address
        except SecureSocketException:
            print("Couldn't connect to host ({ip}, {port})".format(ip=address, port=port))

    client_socket.settimeout(timeout)
    return None


def attempt(window: Tk, code: str, orientation: Orientation, client_socket: SecureSocket):
    #peer_address = find_peer(client_socket, PORT)
    peer_address = ''
    client_socket.connect(('127.0.0.1', PORT))

    if peer_address is None:
        popup = Tk()
        popup.title("Connection Failed, no peer found")
        popup.geometry("200x100")
        messageLabel = Label(popup, text="Connection Failed,\nno peer found", font=("", 15))
        messageLabel.pack()
        closeButton = Button(popup, text="OK", command=popup.destroy, font=("", 20))
        closeButton.pack()

    else:
        client_socket.send(pickle.dumps((orientation, code, None)))
        window.destroy()


def run(client_socket: SecureSocket):
    while True:
        print(client_socket.recv())


def main():
    client_socket = SecureSocket()
    # address = find_peer(client_socket, PORT)

    current_display = Display()

    #  create a window first
    root = Tk()
    # define window dimensions width and height
    window_width = int(current_display.width * (1.0 / SIZE))
    window_height = int(current_display.height * (1.0 / SIZE))
    # get the screen size of your computer [width and height using the root object as foolows]
    screen_width = current_display.width
    screen_height = current_display.height
    # Get the window position from the top dynamically as well as position from left or right as follows
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    # this is the line that will center your window
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    # initialise the window

    enter_code_label = Label(root, text="Enter\nCode", font=("Gulim", 25))
    main_computer_label = Label(root, text="main\ncomputer", font=("Gulim", 25))

    inputtxt = Text(root,
                    height=1,
                    width=7)
    inputtxt.configure(font=("Microsoft Sans Serif", 50))

    button_action = lambda orientation: attempt(root, inputtxt.get("1.0", "end"), orientation, client_socket)

    top_button = Button(root, text="TOP", font=("Gulim", 25), command=lambda: button_action(Orientation.TOP))
    left_button = Button(root, text="LEFT", font=("Gulim", 25), command=lambda: button_action(Orientation.LEFT))
    right_button = Button(root, text="RIGHT", font=("Gulim", 25), command=lambda: button_action(Orientation.RIGHT))
    bottom_button = Button(root, text="BOTTOM", font=("Gulim", 25), command=lambda: button_action(Orientation.BOTTOM))

    enter_code_label.grid(row=0, column=0)
    main_computer_label.grid(row=2, column=2)
    inputtxt.grid(row=0, column=2)
    top_button.grid(row=1, column=2)
    left_button.grid(row=2, column=0)
    right_button.grid(row=2, column=4)
    bottom_button.grid(row=3, column=2)

    root.mainloop(0)

    run(client_socket)


if __name__ == '__main__':
    main()
