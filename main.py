import sys
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
from modules.mica.styleSheet import setMicaWindow
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

        self.setAttribute(Qt.WA_TranslucentBackground)
        if QtWin.isCompositionEnabled():
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    centralwidget = TheWindow()
    sys.exit(app.exec_())
