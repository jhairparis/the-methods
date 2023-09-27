import sys
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Qt, QRect, QCoreApplication, QSize, QMetaObject
from Screens.Interpolation import Ui_Interpolation
from modules.mica.styleSheet import ApplyMenuBlur
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
from modules.mica.styleSheet import setMicaWindow
from Screens.SolveOneVariable import Ui_SolveOneVariable
from Screens.components.About import AboutDialog
from modules.mica.styleSheet import ApplyMenuBlur, setStyleSheet
import matplotlib
from icons import icons_rc

matplotlib.use("Qt5Agg")


class TheWindow(QMainWindow):
    min_size = QSize(980, 650)
    font_family = "Segoe UI Variable Small"
    font_size = 11
    font_weight = 50

    def setupUI(self):
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.ico"))
        self.setObjectName("MainWindow")
        self.setEnabled(True)

        self.resize(self.min_size)
        self.setMinimumSize(self.min_size)

        font = QtGui.QFont()
        font.setFamily(self.font_family)
        font.setPointSize(self.font_size)
        font.setWeight(self.font_weight)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)

        self.setFont(font)

        setStyleSheet(self)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(self.min_size)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setFont(font)

        self.tabSolveOneVariable = QtWidgets.QWidget(self.tabWidget)
        self.tabSolveOneVariable.setStyleSheet("")
        self.tabSolveOneVariable.setObjectName("tabSolveOneVariable")

        self.ui = Ui_SolveOneVariable()
        self.ui.setupUi(self, self.tabSolveOneVariable)

        self.tabInterpolation = QtWidgets.QWidget()
        self.tabInterpolation.setStyleSheet("")
        self.tabInterpolation.setObjectName("tabInterpolation")

        self.ui2 = Ui_Interpolation()
        self.ui2.setupUi(self, self.tabInterpolation)

        self.tabWidget.addTab(self.tabSolveOneVariable, "Solve one variable")
        self.tabWidget.addTab(self.tabInterpolation, "Interpolation")

        self.setCentralWidget(self.tabWidget)

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QRect(0, 0, 980, 63))
        self.menuBar.setStyleSheet("")
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setEnabled(True)
        self.menuFile.setObjectName("menuFile")
        self.actionNew = QtWidgets.QMenu(self.menuFile)
        self.actionNew.setEnabled(True)
        self.actionNew.setStyleSheet("")
        self.actionNew.setObjectName("actionNew")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menuBar)

        self.actionUndo = QtWidgets.QAction(self)
        self.actionUndo.setObjectName("actionUndo")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setEnabled(True)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionPlain_Text_Document = QtWidgets.QAction(self)
        self.actionPlain_Text_Document.setObjectName("actionPlain_Text_Document")
        self.actionRich_Text_Document = QtWidgets.QAction(self)
        self.actionRich_Text_Document.setObjectName("actionRich_Text_Document")
        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCut = QtWidgets.QAction(self)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(self)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(self)
        self.actionPaste.setObjectName("actionPaste")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setEnabled(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew.addAction(self.actionPlain_Text_Document)
        self.actionNew.addAction(self.actionRich_Text_Document)
        self.menuFile.addAction(self.actionNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuHelp.addAction(self.actionAbout)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.valuesUI()
        self.actionUI()

    def valuesUI(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "The methods"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setTitle(_translate("MainWindow", "New"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionPlain_Text_Document.setText(_translate("MainWindow", "Project"))
        self.actionRich_Text_Document.setText(_translate("MainWindow", "Project File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+I"))

        ApplyMenuBlur(self.menuFile.winId().__int__())
        ApplyMenuBlur(self.actionNew.winId().__int__())
        ApplyMenuBlur(self.menuEdit.winId().__int__())
        ApplyMenuBlur(self.menuHelp.winId().__int__())

        QMetaObject.connectSlotsByName(self)

    def actionUI(self):
        def openAbout():
            about = AboutDialog(self)
            about.exec()

        self.actionAbout.triggered.connect(openAbout)
        self.actionExit.triggered.connect(self.close)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUI()

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
