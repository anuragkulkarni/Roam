"""
TODO This is a SUPER SUPER OLD module and might not be needed anymore
"""
import sys
import win32gui
import win32con
import win32api

from qgis.PyQt.QtWidgets import QApplication, QWidget
from qgis.PyQt.QtCore import QObject, pyqtSignal

from roam.utils import log


class PowerState(QObject):
    poweroff = pyqtSignal()
    poweron = pyqtSignal()

    def __init__(self, widget):
        QObject.__init__(self)
        self.widget = widget
        self.__oldProc = win32gui.SetWindowLong(self.widget.winId(), \
                                                win32con.GWL_WNDPROC, \
                                                self.__WndProc)

    def __WndProc(self, hWnd, msg, wParam, lParam):
        if msg == win32con.WM_POWERBROADCAST:
            if wParam == win32con.PBT_APMSUSPEND:
                log("Power off")
                self.poweroff.emit()
            elif wParam == win32con.PBT_APMRESUMESUSPEND:
                log("Power ON")
                self.poweron.emit()
        else:
            win32api.SetWindowLong(self.widget.winId(),
                                   win32con.GWL_WNDPROC,
                                   self.__oldProc)

        return win32gui.CallWindowProc(self.__oldProc, hWnd, msg, wParam, lParam)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wid = QWidget()
    power = PowerState(wid)
    wid.show()
    sys.exit(app.exec_())
