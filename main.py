import sys
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
import numpy as np
from win32mica import ApplyMica, MICAMODE
import darkdetect
import matplotlib
from lib.methods.bisection import bisection
from modules.blurwindow import GlobalBlur

matplotlib.use("Qt5Agg")

if darkdetect.isDark() == True:
    from dark import *
else:
    from light import *


class TheWindow(QMainWindow):
    def subscription(self, v, who):
        if who == 0:
            infinite = np.linspace(-25, 25, 1000)

            self.ui.logic.fn = self.ui.logic.gen_fn(v)

            self.ui.graph_.axes.cla()

            self.ui.graph_.axes.plot(
                infinite,
                [self.ui.logic.fn(i) for i in infinite],
                color="gray",
                linestyle="--",
                zorder=1,
            )

            self.ui.fn_box.value = v
            self.ui.graph_.draw()

        if who == 1:
            df = DataFrame(
                {
                    "Hey": [0, 1, 2],
                    "Hey2": [8, 4, 3],
                    "Hey3": [8, 4, 3],
                    "Hey4": [8, 4, 3],
                    "Hey5": [8, 4, 3],
                    "Hey6": [8, 4, 3],
                    "Hey7": [8, 4, 3],
                }
            )
            model = TableModel(df)
            self.ui.tableWidget.setModel(model)
            self.ui.tolerance_box.value = v

    def click(self):
        x0 = self.ui.x0_box.value()
        x1 = self.ui.x1_box.value()
        tol = float(self.ui.tolerance_box.value)
        steps = self.ui.iteration_box.value()

        method = bisection(self.ui.logic, self.ui.logic.fn, x0, x1, tol, steps)

        print(
            self.ui.method_box.currentIndex(),
            self.ui.fn_box.value,
            method,
            self.ui.logic.method_title
        )

        return None

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
        self.ui.method_box.setView(self.ui.listview)

        self.ui.method_box.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.ui.method_box.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.ui.method_box.setCurrentIndex(-1)
        ApplyMenuBlur(self.ui.method_box.view().window().winId().__int__(), self)

        # CLICK
        self.ui.pushButton.clicked.connect(self.click)

        self.ui.fn_box.textChanged.connect(lambda v: self.subscription(v, 0))
        self.ui.tolerance_box.textChanged.connect(lambda v: self.subscription(v, 1))

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    centralwidget = TheWindow()
    sys.exit(app.exec_())
