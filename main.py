import sys
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWinExtras import QtWin
from win32mica import ApplyMica, MICAMODE
import darkdetect

from modules.blurwindow import GlobalBlur

if darkdetect.isDark() == True:
    from dark import *
else:
    from light import *


class Template(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MICA FOR WINDOW
        hwnd = self.winId().__int__()
        mode = MICAMODE.DARK
        mode = MICAMODE.LIGHT
        mode = darkdetect.isDark()
        ApplyMica(hwnd, mode)

        # MICA FOR MENUS
        def ApplyMenuBlur(hwnd: int, window: self.ui.window):
            hwnd = int(hwnd)
            if darkdetect.isDark() == True:
                GlobalBlur(
                    hwnd,
                    Acrylic=True,
                    hexColor="#21212140",
                    Dark=True,
                    smallCorners=True,
                )
            else:
                GlobalBlur(
                    hwnd,
                    Acrylic=True,
                    hexColor="#faf7f740",
                    Dark=True,
                    smallCorners=True,
                )

        ApplyMenuBlur(self.ui.menuFile.winId().__int__(), self)
        ApplyMenuBlur(self.ui.actionNew.winId().__int__(), self)
        ApplyMenuBlur(self.ui.menuEdit.winId().__int__(), self)
        ApplyMenuBlur(self.ui.menuHelp.winId().__int__(), self)

        self.setAttribute(Qt.WA_TranslucentBackground)
        if QtWin.isCompositionEnabled():
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        # CUSTOM LIST IN COMBOBOX
        self.ui.listview = QtWidgets.QListView()
        self.ui.comboBox.setView(self.ui.listview)

        self.ui.comboBox.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.ui.comboBox.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.ui.comboBox.setCurrentIndex(-1)
        ApplyMenuBlur(self.ui.comboBox.view().window().winId().__int__(), self)

        # BUTTONS CLICK
        # self.ui.disablebtn.clicked.connect(lambda: self.ui.window.setEnabled(False))
        # self.ui.enablebtn.clicked.connect(lambda: self.ui.window.setEnabled(True))


        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    centralwidget = Template()
    sys.exit(app.exec_())
