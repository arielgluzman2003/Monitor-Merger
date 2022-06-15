"""
author: Ariel Gluzman
date: 2022
email: ariel.gluzman@gmail.com
"""

import multiprocessing
import pickle
from tkinter.font import Font
from tkinter.tix import *
from typing import List
from screeninfo import get_monitors, Monitor
from src.Client.main import Client
from src.Utilities.SecureSocket import SecureSocket, SecureSocketException
from src.Utilities.constants import Orientation, ConnectionCodes, OperationCodes
from multiprocessing import Value
from Server.main import Server, generate_code
import netifaces

PORT = 1234


def destroy_all(widgets: List[Widget]):
    for widget in widgets:
        widget.destroy()


def host_finder(default_gateway=netifaces.gateways()['default'][netifaces.AF_INET][0], port=PORT):
    subdomain = '.'.join(default_gateway.split('.')[:-1]) + '.'
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


def connect(orientation: IntVar, info_label: Label, code: str, start_button: Button,
            operation_code: multiprocessing.Value):
    if operation_code.value == OperationCodes.WORKING:
        operation_code.value = OperationCodes.NOT_WORKING
        start_button['text'] = 'Connect'

    else:
        print(f'trying to connect {orientation.get()}, with code {code}')
        sock, address = host_finder()
        if sock is None:
            info_label.config(text='No Server Found')
        else:
            for m in get_monitors():
                if m.is_primary:
                    dspl = m

            sock: SecureSocket
            sock.send(pickle.dumps((Orientation(orientation.get()), ConnectionCodes.CONNECTION_ATTEMPT, (code, dspl))))
            connection_code = sock.recv()

            if ConnectionCodes.CLIENT_DENIED_PASSCODE_WRONG.value == int(connection_code):
                info_label.config(text='Code Incorrect')
                startButton['text'] = 'Connect'
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

                startButton['text'] = 'Connect'
                return 'Orientation Unavailable'

            operation_code.value = OperationCodes.WORKING
            client = Client(sock, operation_code)
            client.start()
            start_button['text'] = 'Disconnect'


def host(operation_code, start_button: Button, code: str):
    if operation_code.value == OperationCodes.WORKING:
        operation_code.value = OperationCodes.NOT_WORKING
        start_button['text'] = 'Start'
    else:
        start_button['text'] = 'Stop'
        server = Server(code, operation_code)
        server.start()


def connect_widgets(window: Tk, operation_code: multiprocessing.Value):
    # Shared Value Between Radio Buttons
    orientation = IntVar()
    # region widgets
    #
    backButton = Button(window)
    #
    enterCodeLabel = Label(window)
    #
    codeForm = Entry(window)
    #
    rightRadioButton = Radiobutton(window)
    #
    topRadioButton = Radiobutton(window)
    #
    leftRadioButton = Radiobutton(window)
    #
    bottomRadioButton = Radiobutton(window)
    #
    connectionInfoLabel = Label(window)
    #
    connectButton = Button(window)

    widgets = [backButton, enterCodeLabel, codeForm, rightRadioButton, topRadioButton,
               leftRadioButton, bottomRadioButton, connectionInfoLabel, connectButton]
    # endregion
    # region design
    backButton["bg"] = "#f0f0f0"
    backButton["font"] = Font(family='Times', size=10)
    backButton["fg"] = "#000000"
    backButton["justify"] = "center"
    backButton["text"] = "← back"
    backButton.place(x=10, y=10, width=70, height=25)

    enterCodeLabel["font"] = Font(family='Times', size=13)
    enterCodeLabel["fg"] = "#333333"
    enterCodeLabel["justify"] = "center"
    enterCodeLabel["text"] = "Enter The Code That Appears On Server Monitor"
    enterCodeLabel.place(x=20, y=40, width=348, height=50)

    codeForm["borderwidth"] = "1px"
    codeForm["font"] = Font(family='Times', size=48)
    codeForm["fg"] = "#333333"
    codeForm["justify"] = "center"
    codeForm["text"] = "ABCDE"
    codeForm.place(x=90, y=90, width=217, height=58)

    rightRadioButton["font"] = Font(family='Times', size=18)
    rightRadioButton["fg"] = "#333333"
    rightRadioButton["justify"] = "center"
    rightRadioButton["text"] = "right"
    rightRadioButton["variable"] = orientation
    rightRadioButton["value"] = Orientation.RIGHT.value
    rightRadioButton.place(x=300, y=250, width=85, height=25)

    topRadioButton["font"] = Font(family='Times', size=18)
    topRadioButton["fg"] = "#333333"
    topRadioButton["justify"] = "center"
    topRadioButton["text"] = "top"
    topRadioButton["variable"] = orientation
    topRadioButton["value"] = Orientation.TOP.value
    topRadioButton.place(x=160, y=190, width=85, height=25)

    leftRadioButton["font"] = Font(family='Times', size=18)
    leftRadioButton["fg"] = "#333333"
    leftRadioButton["justify"] = "center"
    leftRadioButton["text"] = "left"
    leftRadioButton["variable"] = orientation
    leftRadioButton["value"] = Orientation.LEFT.value
    leftRadioButton.place(x=20, y=250, width=85, height=25)

    bottomRadioButton["font"] = Font(family='Times', size=18)
    bottomRadioButton["fg"] = "#333333"
    bottomRadioButton["justify"] = "center"
    bottomRadioButton["text"] = "bottom"
    bottomRadioButton["variable"] = orientation
    bottomRadioButton["value"] = Orientation.BOTTOM.value
    bottomRadioButton.place(x=160, y=310, width=90, height=25)

    connectionInfoLabel["font"] = Font(family='Times', size=18)
    connectionInfoLabel["fg"] = "#333333"
    connectionInfoLabel["justify"] = "center"
    connectionInfoLabel["text"] = ""
    connectionInfoLabel.place(x=50, y=350, width=300, height=41)

    connectButton["bg"] = "#f0f0f0"
    connectButton["font"] = Font(family='Times', size=23)
    connectButton["fg"] = "#000000"
    connectButton["justify"] = "center"
    connectButton["text"] = "Connect"
    connectButton.place(x=120, y=240, width=156, height=48)
    # endregion
    # region functionality
    backButton["command"] = lambda: [init_widgets(window, operation_code), destroy_all(widgets)]
    connectButton["command"] = lambda: connect(orientation, connectionInfoLabel,
                                               codeForm.get(), connectButton, operation_code)
    # endregion


def host_widgets(window: Tk, operation_code: Value):
    code = generate_code()
    # region widgets
    #
    backButton = Button(window)
    #
    codeLabel = Label(window)
    #
    operationButton = Button(window)
    #
    hostInfoLabel = Label(window)
    #
    leftMonitorLabel = Label(window)
    #
    rightMonitorLabel = Label(window)
    #
    topMonitorLabel = Label(window)
    #
    bottomMonitorLabel = Label(window)

    widgets = [backButton, codeLabel, operationButton, hostInfoLabel,
               leftMonitorLabel, rightMonitorLabel, topMonitorLabel, bottomMonitorLabel]
    # endregion
    # region design
    backButton["bg"] = "#f0f0f0"
    backButton["font"] = Font(family='Times', size=10)
    backButton["fg"] = "#000000"
    backButton["justify"] = "center"
    backButton["text"] = "← back"
    backButton.place(x=10, y=10, width=70, height=25)

    codeLabel["font"] = Font(family='Times', size=48)
    codeLabel["fg"] = "#333333"
    codeLabel["justify"] = "center"
    codeLabel["text"] = code
    codeLabel.place(x=80, y=107, width=220, height=48)

    operationButton["bg"] = "#f0f0f0"
    operationButton["font"] = Font(family='Times', size=28)
    operationButton["fg"] = "#000000"
    operationButton["justify"] = "center"
    operationButton["text"] = "Start"
    operationButton.place(x=100, y=160, width=194, height=46)

    hostInfoLabel["font"] = Font(family='Times', size=15)
    hostInfoLabel["fg"] = "#333333"
    hostInfoLabel["justify"] = "center"
    hostInfoLabel["text"] = "To Connect,\nEnter The Code:"
    hostInfoLabel.place(x=25, y=40, width=130, height=50)

    leftMonitorLabel["font"] = Font(family='Times', size=12)
    leftMonitorLabel["fg"] = "#333333"
    leftMonitorLabel["justify"] = "center"
    leftMonitorLabel["text"] = 'left'
    leftMonitorLabel.place(x=10, y=300, width=40, height=20)

    rightMonitorLabel["font"] = Font(family='Times', size=12)
    rightMonitorLabel["fg"] = "#333333"
    rightMonitorLabel["justify"] = "center"
    rightMonitorLabel["text"] = 'right'
    rightMonitorLabel.place(x=350, y=300, width=40, height=20)

    topMonitorLabel["font"] = Font(family='Times', size=12)
    topMonitorLabel["fg"] = "#333333"
    topMonitorLabel["justify"] = "center"
    topMonitorLabel["text"] = 'top'
    topMonitorLabel.place(x=180, y=250, width=40, height=20)

    bottomMonitorLabel["font"] = Font(family='Times', size=12)
    bottomMonitorLabel["fg"] = "#333333"
    bottomMonitorLabel["justify"] = "center"
    bottomMonitorLabel["text"] = 'bottom'
    bottomMonitorLabel.place(x=190, y=350, width=40, height=20)
    # endregion
    # region functionality
    operationButton["command"] = lambda: host(operation_code, operationButton, code)
    backButton["command"] = lambda: [init_widgets(window, operation_code), destroy_all(widgets)]
    # endregion


def init_widgets(window: Tk, operation_code: multiprocessing.Value):
    operation_code.value = OperationCodes.NOT_WORKING
    # region widgets
    #
    welcomeLabel = Label(window)
    #
    hostButton = Button(window)
    #
    connectButton = Button(window)
    #
    hostButtonTip = Balloon(window)
    #
    connectButtonTip = Balloon(window)

    widgets = [welcomeLabel, hostButton, connectButton, hostButtonTip, connectButtonTip]
    # endregion
    # region widgets
    welcomeLabel["font"] = Font(family='Times', size=15)
    welcomeLabel["fg"] = "#333333"
    welcomeLabel["justify"] = "center"
    welcomeLabel["text"] = "Pick One Of The\nFollowing Options"
    welcomeLabel.place(x=42, y=30, width=300, height=100)

    hostButton["anchor"] = "center"
    hostButton["bg"] = "#f0f0f0"
    hostButton["font"] = Font(family='Times', size=18)
    hostButton["fg"] = "#000000"
    hostButton["justify"] = "center"
    hostButton["text"] = "Host"
    hostButton.place(x=130, y=150, width=131, height=30)

    connectButton["bg"] = "#f0f0f0"
    connectButton["font"] = Font(family='Times', size=18)
    connectButton["fg"] = "#000000"
    connectButton["justify"] = "center"
    connectButton["text"] = "Connect"
    connectButton.place(x=130, y=220, width=131, height=30)

    hostButtonTip.bind_widget(hostButton, balloonmsg='Make This Computer Main Computer And Let Others Connect')
    connectButtonTip.bind_widget(connectButton, balloonmsg='Connect To Server')
    # endregion
    # region functionality
    hostButton["command"] = lambda: [host_widgets(window, operation_code), destroy_all(widgets)]
    connectButton["command"] = lambda: [connect_widgets(window, operation_code), destroy_all(widgets)]
    # endregion


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
    window.iconbitmap(os.path.join('\\'.join(os.getcwd().split('\\')[:-1]), r'res\icon.ico'))

    init_widgets(window, operation_code)

    window.mainloop()
    operation_code.value = OperationCodes.NOT_WORKING


def operation():
    pass


if __name__ == '__main__':
    main()
