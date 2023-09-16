import sys
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
from modules.mica.styleSheet import ApplyMenuBlur, setMicaWindow
from Screens.SolveOneVariable import Ui_SolveOneVariable
import matplotlib

matplotlib.use("Qt5Agg")


class TheWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SolveOneVariable()
        self.ui.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("icons/icon.ico"))
        setMicaWindow(self)

        ApplyMenuBlur(self.ui.menuFile.winId().__int__())
        ApplyMenuBlur(self.ui.actionNew.winId().__int__())
        ApplyMenuBlur(self.ui.menuEdit.winId().__int__())
        ApplyMenuBlur(self.ui.menuHelp.winId().__int__())

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
        ApplyMenuBlur(self.ui.method_box.view().window().winId().__int__())

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    centralwidget = TheWindow()
    sys.exit(app.exec_())
