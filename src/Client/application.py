import multiprocessing
import os
import pickle
from tkinter.font import Font
from tkinter.tix import *
from typing import List
from screeninfo import get_monitors, Monitor

from src.Client.mini_main import Client
from src.Utilities.SecureSocket import SecureSocket, SecureSocketException
from src.Utilities.constants import Orientation, ConnectionCodes, OperationCodes
from multiprocessing import Value

PORT = 1234


def host_finder(subdomains: List[str], port=PORT):
    for subdomain in subdomains:
        if len(subdomain.split('.')) == 4:
            subdomain = '.'.join(subdomain.split('.')[:-1])  # Remove Last Octet
            subdomain += '.'
        for i in range(2, 256):
            client_socket = SecureSocket()
            default_timeout = client_socket.gettimeout()
            client_socket.settimeout(0.01)
            ip = subdomain + str(i)
            try:
                client_socket.connect((ip, PORT))
                client_socket.settimeout(default_timeout)
                return client_socket, ip
            except SecureSocketException:
                print(ip, '- Not A Host')
    return None, None


def connect(orientation: IntVar, info_label: Label, code: str, startButton: Button, operation_code: multiprocessing.Value):
    if operation_code.value == OperationCodes.WORKING:
        operation_code.value = OperationCodes.NOT_WORKING
        return

    print(f'trying to connect {orientation.get()}, with code {code}')
    sock, address = host_finder(['192.168.1.0', '10.0.8.0'], port=PORT)
    if sock is None:
        info_label.config(text='No Server Found')
        return 'No Server Found'

    my_display: Monitor
    for m in get_monitors():
        if m.is_primary:
            my_display = m

    sock: SecureSocket
    sock.send(pickle.dumps((Orientation(orientation.get()), ConnectionCodes.CONNECTION_ATTEMPT, (code, my_display))))
    connection_code = sock.recv()

    if ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG.value == int(connection_code):
        info_label.config(text='Code Incorrect')
        return 'Code Incorrect'

    if ConnectionCodes.CLIENT_DENIED_ORIENTATION_UNAVAILABLE.value == int(connection_code):
        orientation_code: int = orientation.get()
        if orientation_code == Orientation.LEFT.value:
            info_label.config(text='Left Monitor Is Already Taken.')
        if orientation_code == Orientation.RIGHT.value:
            info_label.config(text='Right Monitor Is Already Taken.')
        if orientation_code == Orientation.TOP.value:
            info_label.config(text='Top Monitor Is Already Taken.')
        if orientation_code == Orientation.BOTTOM.value:
            info_label.config(text='Bottom Monitor Is Already Taken.')

        return 'Orientation Unavailable'

    client = Client(sock, operation_code)
    operation_code.value = OperationCodes.WORKING
    client.start()


def connect_widgets(window: Tk, operation_code: multiprocessing.Value):
    for widget in window.winfo_children():
        widget.destroy()

    backButton = Button(window)
    backButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=10)
    backButton["font"] = ft
    backButton["fg"] = "#000000"
    backButton["justify"] = "center"
    backButton["text"] = "← back"
    backButton.place(x=10, y=10, width=70, height=25)
    backButton["command"] = lambda: init_widgets(window, operation_code)

    orientation = IntVar()
    enterCodeLabel = Label(window)
    ft = Font(family='Times', size=13)
    enterCodeLabel["font"] = ft
    enterCodeLabel["fg"] = "#333333"
    enterCodeLabel["justify"] = "center"
    enterCodeLabel["text"] = "Enter The Code That Appears On Server Monitor"
    enterCodeLabel.place(x=20, y=40, width=348, height=50)

    codeForm = Entry(window)
    codeForm["borderwidth"] = "1px"
    ft = Font(family='Times', size=48)
    codeForm["font"] = ft
    codeForm["fg"] = "#333333"
    codeForm["justify"] = "center"
    codeForm["text"] = "ABCDE"
    codeForm.place(x=90, y=90, width=217, height=58)

    rightRadioButton = Radiobutton(window)
    ft = Font(family='Times', size=18)
    rightRadioButton["font"] = ft
    rightRadioButton["fg"] = "#333333"
    rightRadioButton["justify"] = "center"
    rightRadioButton["text"] = "right"
    rightRadioButton["variable"] = orientation
    rightRadioButton["value"] = Orientation.RIGHT.value
    rightRadioButton.place(x=300, y=250, width=85, height=25)
    # rightRadioButton["command"] = self.rightRadioButton_command

    topRadioButton = Radiobutton(window)
    ft = Font(family='Times', size=18)
    topRadioButton["font"] = ft
    topRadioButton["fg"] = "#333333"
    topRadioButton["justify"] = "center"
    topRadioButton["text"] = "top"
    topRadioButton["variable"] = orientation
    topRadioButton["value"] = Orientation.TOP.value
    topRadioButton.place(x=160, y=190, width=85, height=25)
    # topRadioButton["command"] = self.topRadioButton_command

    leftRadioButton = Radiobutton(window)
    ft = Font(family='Times', size=18)
    leftRadioButton["font"] = ft
    leftRadioButton["fg"] = "#333333"
    leftRadioButton["justify"] = "center"
    leftRadioButton["text"] = "left"
    leftRadioButton["variable"] = orientation
    leftRadioButton["value"] = Orientation.LEFT.value
    leftRadioButton.place(x=20, y=250, width=85, height=25)
    # leftRadioButton["command"] = self.leftRadioButton_command

    bottomRadioButton = Radiobutton(window)
    ft = Font(family='Times', size=18)
    bottomRadioButton["font"] = ft
    bottomRadioButton["fg"] = "#333333"
    bottomRadioButton["justify"] = "center"
    bottomRadioButton["text"] = "bottom"
    bottomRadioButton["variable"] = orientation
    bottomRadioButton["value"] = Orientation.BOTTOM.value
    bottomRadioButton.place(x=160, y=310, width=90, height=25)
    # bottomRadioButton["command"] = self.bottomRadioButton_command

    connectionInfoLabel = Label(window)
    ft = Font(family='Times', size=18)
    connectionInfoLabel["font"] = ft
    connectionInfoLabel["fg"] = "#333333"
    connectionInfoLabel["justify"] = "center"
    connectionInfoLabel["text"] = ""
    connectionInfoLabel.place(x=50, y=350, width=300, height=41)

    connectButton = Button(window)
    connectButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=23)
    connectButton["font"] = ft
    connectButton["fg"] = "#000000"
    connectButton["justify"] = "center"
    connectButton["text"] = "Connect"
    connectButton.place(x=120, y=240, width=156, height=48)
    connectButton["command"] = lambda: connect(orientation, connectionInfoLabel, codeForm.get(), connectButton,operation_code)


def host_widgets(window: Tk):
    for widgets in window.winfo_children():
        widgets.destroy()

    backButton = Button(window)
    backButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=10)
    backButton["font"] = ft
    backButton["fg"] = "#000000"
    backButton["justify"] = "center"
    backButton["text"] = "← back"
    backButton.place(x=10, y=10, width=70, height=25)
    backButton["command"] = lambda: init_widgets(window)

    operationButton = Button(window)
    operationButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=28)
    operationButton["font"] = ft
    operationButton["fg"] = "#000000"
    operationButton["justify"] = "center"
    operationButton["text"] = "Start"
    operationButton.place(x=100, y=260, width=194, height=46)
    # operationButton["command"] = self.operationButton_command

    hostInfoLabel = Label(window)
    ft = Font(family='Times', size=15)
    hostInfoLabel["font"] = ft
    hostInfoLabel["fg"] = "#333333"
    hostInfoLabel["justify"] = "center"
    hostInfoLabel["text"] = "To Connect,\nEnter The Code:"
    hostInfoLabel.place(x=25, y=40, width=130, height=50)

    codeLabel = Label(window)
    ft = Font(family='Times', size=48)
    codeLabel["font"] = ft
    codeLabel["fg"] = "#333333"
    codeLabel["justify"] = "center"
    codeLabel["text"] = "ABCDE"
    codeLabel.place(x=80, y=107, width=220, height=48)


def init_widgets(window: Tk, operation_code: multiprocessing.Value):
    operation_code.value = OperationCodes.NOT_WORKING
    for widgets in window.winfo_children():
        widgets.destroy()

    welcomeLabel = Label(window)
    ft = Font(family='Times', size=15)
    welcomeLabel["font"] = ft
    welcomeLabel["fg"] = "#333333"
    welcomeLabel["justify"] = "center"
    welcomeLabel["text"] = "Pick One Of The\nFollowing Options"
    welcomeLabel.place(x=42, y=30, width=300, height=100)

    hostButton = Button(window)
    hostButton["anchor"] = "center"
    hostButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=18)
    hostButton["font"] = ft
    hostButton["fg"] = "#000000"
    hostButton["justify"] = "center"
    hostButton["text"] = "Host"
    hostButton.place(x=130, y=150, width=131, height=30)
    hostButton["command"] = lambda: host_widgets(window)

    connectButton = Button(window)
    connectButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=18)
    connectButton["font"] = ft
    connectButton["fg"] = "#000000"
    connectButton["justify"] = "center"
    connectButton["text"] = "Connect"
    connectButton.place(x=130, y=220, width=131, height=30)
    connectButton["command"] = lambda: connect_widgets(window, operation_code)

    hostButtonTip = Balloon(window)
    hostButtonTip.bind_widget(hostButton, balloonmsg='Make This Computer Main Computer And Let Others Connect')

    connectButtonTip = Balloon(window)
    connectButtonTip.bind_widget(connectButton, balloonmsg='Connect To Server')


def main():
    operation_code = Value('i', OperationCodes.NOT_WORKING)
    window = Tk()
    window.title('Monitor Merger')

    # setting window size
    width = 400
    height = 400
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(alignstr)
    window.resizable(width=False, height=False)
    window.iconbitmap(os.path.join('\\'.join(os.getcwd().split('\\')[:-2]), r'res\icon.ico'))

    init_widgets(window, operation_code)

    window.mainloop()


def operation():
    pass


if __name__ == '__main__':
    main()
