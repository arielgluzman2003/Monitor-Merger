from multiprocessing import Value
import pygame
import win32con
import win32gui
import win32api
from Utilities.constants import WindowCodes, OperationCodes
from multiprocessing import Process
from ctypes import windll

TRUE = 1
FALSE = 0

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow#parameters
SW_HIDE = 0
SW_SHOW = 1


class Window(Process):
    def __init__(self, operation_code: Value):

        super(Window, self).__init__()
        self.operation_code = operation_code
        self.visible = Value('i', 0)
        self.changed = Value('i', 0)
        pygame.init()

    def destroy(self):
        self.visible.value = FALSE
        self.changed.value = TRUE

    def wake(self):
        self.visible.value = TRUE
        self.changed.value = TRUE

    def run(self) -> None:
        self.changed.value = TRUE

        surface = pygame.display.set_mode((0, 0), pygame.SRCALPHA | pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        surface.set_alpha(0)
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 1, win32con.LWA_ALPHA)
        win32gui.ShowWindow(hwnd, SW_HIDE)

        while self.running():
            if self.visible.value == TRUE:
                if self.changed.value == TRUE:
                    # Bring Window To Front
                    win32gui.ShowWindow(hwnd, SW_SHOW)
                    win32gui.SetForegroundWindow(hwnd)
                self.changed.value = FALSE

            if self.visible.value == FALSE:
                if self.changed.value == TRUE:
                    win32gui.ShowWindow(hwnd, SW_HIDE)
                self.changed.value = FALSE

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.visible.value = FALSE

        pygame.quit()

    def running(self):
        return self.operation_code.value != OperationCodes.NOT_WORKING
