"""
author: Ariel Gluzman
date: May 30th 2022
"""

# Extended Window Styles 'https://docs.microsoft.com/en-us/windows/win32/winmsg/extended-window-styles'

from multiprocessing import Value
import pygame
import win32con
import win32gui
from src.Utilities.constants import OperationCodes
from multiprocessing import Process

TRUE = win32con.TRUE
FALSE = win32con.FALSE


class TransparentWindow(Process):
    def __init__(self, operation_code: Value):

        super(TransparentWindow, self).__init__()
        self.operation_code = operation_code
        self.visible = Value('i', FALSE)
        self.changed = Value('i', FALSE)
        pygame.init()

    def destroy(self):
        self.visible.value = FALSE
        self.changed.value = TRUE

    def wake(self):
        self.visible.value = TRUE
        self.changed.value = TRUE

    def run(self) -> None:
        self.changed.value = TRUE

        # Open A full-screen Window
        surface = pygame.display.set_mode((0, 0), pygame.SRCALPHA | pygame.FULLSCREEN)
        # Make Mouse Cursor Not Visible
        pygame.mouse.set_visible(False)

        # Extract 'Handle to a Window' HWND
        hwnd = pygame.display.get_wm_info()["window"]

        # Set New Window-Attributes
        win32gui.SetWindowLong(hwnd,
                               win32con.GWL_EXSTYLE,  # Add Extended Styles
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)  # Get Previous Extended Window Styles
                               | win32con.WS_EX_LAYERED  # Make Window Layered, to Call 'SetLayeredWindowAttributes'
                               | win32con.WS_EX_TOOLWINDOW)  # Sets Window As Tool-Window, Makes Taskbar Icon Not Show

        # Set Window Alpha Attribute to 1 - Maximum Transparency
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 1, win32con.LWA_ALPHA)

        # Hide Window
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

        while self.running():
            if self.visible.value == TRUE:
                if self.changed.value == TRUE:
                    # Show Window
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    # Bring Window To Front
                    win32gui.SetForegroundWindow(hwnd)

                self.changed.value = FALSE

            if self.visible.value == FALSE:
                if self.changed.value == TRUE:
                    # Show Window
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                self.changed.value = FALSE

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.visible.value = FALSE

                if self.visible.value != FALSE:
                    # If Any Window Has Come To Front, Set Transparent Window To Front
                    if win32gui.GetForegroundWindow() != hwnd:
                        win32gui.SetForegroundWindow(hwnd)
                # pygame.display.update

        pygame.quit()

    def running(self):
        return self.operation_code.value != OperationCodes.NOT_WORKING
