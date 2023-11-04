import sys
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Qt, QRect, QCoreApplication, QSize, QMetaObject
from Screens.Home import Ui_Home
from Screens.SolveOneVariable import Ui_SolveOneVariable
from Screens.DiffereantialEquation import Ui_DifferentialEquation
from Screens.Interpolation import Ui_Interpolation
from Screens.Bonus import Ui_Video
from modules.mica.styleSheet import ApplyMenuBlur
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
from modules.mica.styleSheet import setMicaWindow
from Screens.components.About import AboutDialog
from modules.mica.styleSheet import ApplyMenuBlur, setStyleSheet
import matplotlib
from icons import icons_rc, home_rc

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

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QRect(0, 0, self.min_size.width(), 63))
        self.menuBar.setStyleSheet("")
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setEnabled(True)
        self.menuFile.setObjectName("menuFile")

        self.actionNew = QtWidgets.QMenu(self.menuFile)
        self.actionNew.setEnabled(True)
        self.actionNew.setStyleSheet("")
        self.actionNew.setObjectName("actionNew")

        self.menuTopics = QtWidgets.QMenu(self.menuBar)
        self.menuTopics.setObjectName("menuTopics")

        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")

        self.setMenuBar(self.menuBar)

        self.solveOneVariable = QtWidgets.QAction(self)
        self.solveOneVariable.setObjectName("solveOneVariable")

        self.interpolation = QtWidgets.QAction(self)
        self.interpolation.setObjectName("interpolation")

        self.differentialEquations = QtWidgets.QAction(self)
        self.differentialEquations.setObjectName("differentialEquations")

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

        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setEnabled(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew.addAction(self.actionPlain_Text_Document)
        self.actionNew.addAction(self.actionRich_Text_Document)

        self.menuFile.addAction(self.actionNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)

        self.menuTopics.addAction(self.solveOneVariable)
        self.menuTopics.addAction(self.interpolation)
        self.menuTopics.addAction(self.differentialEquations)

        self.menuHelp.addAction(self.actionAbout)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTopics.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        # ---

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(self.min_size)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setFont(font)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setStyleSheet(
            """
            QTabWidget::pane {
                    border: none;
            }"""
        )

        self.tabHome = QtWidgets.QWidget(self.tabWidget)
        self.tabHome.setStyleSheet("")
        self.tabHome.setObjectName("home")

        self.homeUi = Ui_Home()
        self.homeUi.setupUi(self, self.tabHome)

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

        self.tabDifferentialEquations = QtWidgets.QWidget()
        self.tabDifferentialEquations.setStyleSheet("")
        self.tabDifferentialEquations.setObjectName("tabDifferentialEquations")

        self.ui3 = Ui_DifferentialEquation()
        self.ui3.setupUi(self, self.tabDifferentialEquations)

        self.tabBonus = QtWidgets.QWidget()
        self.tabBonus.setStyleSheet("")
        self.tabBonus.setObjectName("tabBonus")

        self.bonus = Ui_Video()
        self.bonus.setupUi(self, self.tabBonus)

        self.tabWidget.addTab(self.tabHome, "Home")
        self.tabWidget.addTab(self.tabSolveOneVariable, "Solve one variable")
        self.tabWidget.addTab(self.tabInterpolation, "Interpolation")
        self.tabWidget.addTab(self.tabDifferentialEquations, "Differential equations")
        self.tabWidget.addTab(self.tabBonus, "Bonus")

        self.setCentralWidget(self.tabWidget)

        self.valuesUI()
        self.actionUI()

    def valuesUI(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "The methods"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setTitle(_translate("MainWindow", "New"))

        self.menuTopics.setTitle(_translate("MainWindow", "Topics"))

        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        self.solveOneVariable.setText(_translate("MainWindow", "Solve one variable"))
        self.solveOneVariable.setShortcut(_translate("MainWindow", "Ctrl+1"))

        self.interpolation.setText(_translate("MainWindow", "Interpolation"))
        self.interpolation.setShortcut(_translate("MainWindow", "Ctrl+2"))

        self.differentialEquations.setText(
            _translate("MainWindow", "Differential equations")
        )
        self.differentialEquations.setShortcut(_translate("MainWindow", "Ctrl+3"))

        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionPlain_Text_Document.setText(_translate("MainWindow", "Project"))
        self.actionRich_Text_Document.setText(_translate("MainWindow", "Project File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+I"))

        ApplyMenuBlur(self.menuFile.winId().__int__())
        ApplyMenuBlur(self.actionNew.winId().__int__())
        ApplyMenuBlur(self.menuTopics.winId().__int__())
        ApplyMenuBlur(self.menuHelp.winId().__int__())

        QMetaObject.connectSlotsByName(self)

    def setWindowSolveOneVariable(self):
        self.menuBar.setVisible(True)
        self.tabWidget.setCurrentIndex(1)

    def setWindowInterpolation(self):
        self.menuBar.setVisible(True)
        self.tabWidget.setCurrentIndex(2)

    def setWindowDiffentialEquations(self):
        self.menuBar.setVisible(True)
        return

    def actionUI(self):
        self.solveOneVariable.triggered.connect(self.setWindowSolveOneVariable)
        self.interpolation.triggered.connect(self.setWindowInterpolation)
        self.differentialEquations.triggered.connect(
            lambda: self.tabWidget.setCurrentIndex(2)
        )

        self.actionAbout.triggered.connect(lambda: AboutDialog(self).exec())
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
