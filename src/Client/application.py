import os
from tkinter.font import Font
from tkinter.tix import *
from typing import List
from src.Utilities.SecureSocket import SecureSocket, SecureSocketException
from src.Utilities.constants import Orientation


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
                return ip, client_socket
            except SecureSocketException:
                print(ip, '- Not A Host')
    return None, None


def start(var: IntVar, button: Button, label: Label):
    orientations = [member.value for member in Orientation]
    if var.get() not in orientations:
        label['text'] = 'No Option Chosen'
        return

    label['text'] = 'Searching..'
    print(Orientation(var.get()))
    subdomains = ['192.168.1.0', '10.0.2.0']
    address, client_socket = host_finder(subdomains)

    if client_socket is None:
        print("Can't Connect")
        label['text'] = 'No Server Found'
        return


def connect_widgets(window: Tk):
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
    backButton["command"] = lambda: init_widgets(window)

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

    connectButton = Button(window)
    connectButton["bg"] = "#f0f0f0"
    ft = Font(family='Times', size=23)
    connectButton["font"] = ft
    connectButton["fg"] = "#000000"
    connectButton["justify"] = "center"
    connectButton["text"] = "Connect"
    connectButton.place(x=120, y=240, width=156, height=48)
    # connectButton["command"] = self.connectButton_command

    connectionInfoLabel = Label(window)
    ft = Font(family='Times', size=13)
    connectionInfoLabel["font"] = ft
    connectionInfoLabel["fg"] = "#333333"
    connectionInfoLabel["justify"] = "center"
    connectionInfoLabel["text"] = "Waiting....."
    connectionInfoLabel.place(x=100, y=350, width=209, height=41)


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


def init_widgets(window: Tk):
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
    connectButton["command"] = lambda: connect_widgets(window)

    hostButtonTip = Balloon(window)
    hostButtonTip.bind_widget(hostButton, balloonmsg='Make This Computer Main Computer And Let Others Connect')

    connectButtonTip = Balloon(window)
    connectButtonTip.bind_widget(connectButton, balloonmsg='Connect To Server')


def main():
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

    init_widgets(window)

    window.mainloop()


def operation():
    pass


if __name__ == '__main__':
    main()
