import multiprocessing

import pygame
import win32con

from Graphic.display import current_display_dimensions
from multiprocessing import Value
from threading import Thread
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import sys
import win32gui
import win32api
from Utilities.constants import WindowCodes, OperationCodes


class Window(Thread):
    def __init__(self, operation_code: multiprocessing.Value):

        super(Window, self).__init__()
        self.operation_code = operation_code
        self.running = False
        pygame.init()
        pygame.display.init()

    def destroy(self):
        self.running = False

    def wake(self):
        self.running = True

    def run(self) -> None:
        while self.operation_code.value != OperationCodes.NOT_WORKING:
            if self.running:

                # Create a displace surface object
                surface = pygame.display.set_mode((0, 0), pygame.SRCALPHA | pygame.FULLSCREEN)
                pygame.mouse.set_visible(False)
                surface.set_alpha(0)
                print(surface.get_alpha())

                hwnd = pygame.display.get_wm_info()["window"]
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
                # Set window transparency color
                win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 1, win32con.LWA_ALPHA)

                while self.running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                    pygame.display.update()

                pygame.display.quit()
                pygame.display.init()

        pygame.quit()
