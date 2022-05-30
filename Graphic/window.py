import multiprocessing
import time
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
from multiprocessing import Process

TRUE = 1
FALSE = 0


class Window(Process):
    def __init__(self, operation_code: multiprocessing.Value):

        super(Window, self).__init__()
        self.operation_code = operation_code
        self.visible = multiprocessing.Value('i', 0)
        pygame.init()
        # pygame.display.init()

    def destroy(self):
        self.visible.value = FALSE

    def wake(self):
        self.visible.value = TRUE

    def run(self) -> None:
        while self.running():
            if self.visible.value == TRUE:

                # Create a displace surface object
                surface = pygame.display.set_mode((0, 0), pygame.SRCALPHA | pygame.FULLSCREEN)
                pygame.mouse.set_visible(False)
                surface.set_alpha(0)
                hwnd = pygame.display.get_wm_info()["window"]
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
                # Set window transparency color
                win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 1, win32con.LWA_ALPHA)

                while self.visible.value == TRUE:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.visible.value = FALSE
                    pygame.display.update()

                pygame.display.quit()
                pygame.display.init()

        pygame.quit()

    def running(self):
        return self.operation_code.value != OperationCodes.NOT_WORKING
