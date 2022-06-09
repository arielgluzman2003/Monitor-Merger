from threading import Thread
from tkinter import Tk, Label, Button, Text, Radiobutton, IntVar
from tkinter.font import Font
from typing import List
from Utilities.SecureSocket import SecureSocket, SecureSocketException
from Utilities.constants import Orientation

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



def main():
    window = Tk()
    window.geometry('400x400')
    window.title('Monitor Merger')
    infoLabel = Label(window, text='Not Connected', font=Font(family="Helvetica", size=30))
    infoLabel.pack()
    codeField = Text(window, height=1, width=7, font=Font(family="Helvetica", size=60, weight="bold"))
    codeField.pack()
    var = IntVar()
    leftButton = Radiobutton(window, text="left", variable=var, value=int(Orientation.LEFT))
    rightButton = Radiobutton(window, text="right", variable=var, value=int(Orientation.RIGHT))
    topButton = Radiobutton(window, text="top", variable=var, value=int(Orientation.TOP))
    bottomButton = Radiobutton(window, text="bottom", variable=var, value=int(Orientation.BOTTOM))
    leftButton.pack()
    rightButton.pack()
    topButton.pack()
    bottomButton.pack()

    startButton = Button(window, text='Start', command=lambda: start(var, startButton, infoLabel))
    startButton.pack()
    window.mainloop()


def operation():
    pass


if __name__ == '__main__':
    main()
