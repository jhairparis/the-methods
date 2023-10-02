from PySide2 import QtCore, QtGui, QtWidgets
from copy import deepcopy
from pandas import DataFrame, read_clipboard
from Screens.components.Select import Select
from lib.Logic2 import Logic2
import numpy as np
import time
from lib.interpolation.lagrange import lagrange
from lib.interpolation.newton import (
    center,
    divided_diff,
    normalize,
    polynomialDDP,
    polynomialDDR,
)
from modules.MathToQPixmap import MathToQPixmap
from modules.MplCanvas import MplCanvas
from modules.mica.theme.getTheme import getTheme, rgb2hex
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class Ui_Interpolation(object):
    init_table = DataFrame(
        {
            "Wait...": [1, 2, 3, 5, 8, 13, 21],
        }
    )

    def createAnimationStart(self):
        t = np.linspace(0, 10, 101)
        (self.graph_line,) = self.graph_.axes.plot(
            t, np.sin(t + time.time()), color=rgb2hex(getTheme()["accent"])
        )

    def _update_canvas(self):
        if hasattr(self.graph_line.figure, "canvas"):
            t = np.linspace(0, 10, 101)
            self.graph_line.set_data(t, np.sin(t + time.time()))
            self.graph_line.figure.canvas.draw()

    def setupUi(self, MainWindow, MainWidget):
        from modules.TableModel import TableModel

        self.logic = Logic2()

        self.width = MainWindow.min_size.width()
        self.height = MainWindow.min_size.height() - 63

        font = QtGui.QFont()
        font.setFamily(MainWindow.font_family)
        font.setPointSize(MainWindow.font_size)
        font.setWeight(MainWindow.font_weight)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)

        self.scrollCentral = QtWidgets.QScrollArea(MainWidget)
        self.scrollCentral.setFixedSize(QtCore.QSize(self.width, self.height))

        self.interpolation = QtWidgets.QWidget()
        self.interpolation.setFixedSize(QtCore.QSize(self.width, self.height))

        self.window = QtWidgets.QFrame(self.interpolation)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        self.initWidget = QtWidgets.QWidget(self.window)

        centerHeight = ((self.height - 63) - 40) / 2
        self.getClipboardButton = QtWidgets.QPushButton(self.initWidget)
        self.getClipboardButton.setEnabled(True)
        self.getClipboardButton.setMaximumSize(QtCore.QSize(150, 40))
        self.getClipboardButton.setGeometry(
            QtCore.QRect((self.width - 320) / 2, centerHeight, 150, 40)
        )
        self.getClipboardButton.setFont(font)
        self.getClipboardButton.setStyleSheet("")
        self.getClipboardButton.setObjectName("getClipboardButton")

        self.getEXCELButton = QtWidgets.QPushButton(self.initWidget)
        self.getEXCELButton.setEnabled(True)
        self.getEXCELButton.setMaximumSize(QtCore.QSize(150, 40))
        self.getEXCELButton.setGeometry(
            QtCore.QRect((self.width) / 2, centerHeight, 150, 40)
        )
        self.getEXCELButton.setFont(font)
        self.getEXCELButton.setStyleSheet("")
        self.getEXCELButton.setObjectName("getEXCELButton")

        # ---

        self.readyWidget = QtWidgets.QWidget(self.window)
        self.readyWidget.setVisible(False)

        self.labelCheck = QtWidgets.QLabel(self.readyWidget)
        self.labelCheck.setEnabled(True)
        self.labelCheck.setMinimumSize(QtCore.QSize(95, 40))
        self.labelCheck.setGeometry(QtCore.QRect(20, 20, 95, 40))
        self.labelCheck.setStyleSheet("")
        self.labelCheck.setObjectName("labelCheck")

        self.check = QtWidgets.QCheckBox(self.readyWidget)
        self.check.setStyleSheet("")
        self.check.setObjectName("check")
        self.check.setGeometry(QtCore.QRect(120, 25, 40, 40))

        self.method_box = Select(self.readyWidget)
        self.method_box.setGeometry(QtCore.QRect((self.width - 150) / 2, 20, 150, 40))
        self.method_box.setEnabled(True)
        self.method_box.setToolTip("")
        self.method_box.setStatusTip("")
        self.method_box.setWhatsThis("")
        self.method_box.setAccessibleName("")
        self.method_box.setAccessibleDescription("")
        self.method_box.setStyleSheet("")
        self.method_box.setCurrentText("")
        self.method_box.setMinimumContentsLength(0)
        self.method_box.setObjectName("method_box")
        self.method_box.addItem("")
        self.method_box.addItem("")
        self.method_box.addItem("")
        self.method_box.addItem("")

        self.clearButton = QtWidgets.QPushButton(self.readyWidget)
        self.clearButton.setEnabled(True)
        self.clearButton.setMaximumSize(QtCore.QSize(150, 40))
        self.clearButton.setGeometry(QtCore.QRect(self.width - 180, 20, 150, 40))
        self.clearButton.setFont(font)
        self.clearButton.setStyleSheet("")
        self.clearButton.setObjectName("clearButton")

        self.tableWidget = QtWidgets.QTableView(self.readyWidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 80, self.width - 50, 470))
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")

        model = TableModel(self.init_table)
        self.tableWidget.setModel(model)

        self.progressiveLabel = QtWidgets.QLabel(self.readyWidget)
        self.progressiveLabel.setStyleSheet("")
        self.progressiveLabel.setObjectName("label")
        self.progressiveLabel.setGeometry(QtCore.QRect(20, 460, self.width, 200))

        self.progressiveMath = QtWidgets.QLabel(self.readyWidget)
        self.progressiveMath.setStyleSheet("")
        self.progressiveMath.setObjectName("label")
        self.progressiveMath.setGeometry(QtCore.QRect(20, 510, self.width, 200))

        self.progressiveMathE = QtWidgets.QLabel(self.readyWidget)
        self.progressiveMathE.setStyleSheet("")
        self.progressiveMathE.setObjectName("label")
        self.progressiveMathE.setGeometry(QtCore.QRect(20, 530, self.width, 200))

        self.regressionLabel = QtWidgets.QLabel(self.readyWidget)
        self.regressionLabel.setStyleSheet("")
        self.regressionLabel.setObjectName("label")
        self.regressionLabel.setGeometry(QtCore.QRect(20, 550, self.width, 200))

        self.regressionMath = QtWidgets.QLabel(self.readyWidget)
        self.regressionMath.setStyleSheet("")
        self.regressionMath.setObjectName("label")
        self.regressionMath.setGeometry(QtCore.QRect(20, 570, self.width, 200))

        self.regressionMathE = QtWidgets.QLabel(self.readyWidget)
        self.regressionMathE.setStyleSheet("")
        self.regressionMathE.setObjectName("label")
        self.regressionMathE.setGeometry(QtCore.QRect(20, 590, self.width, 200))

        self.graph = QtWidgets.QWidget(self.readyWidget)
        self.graph.setGeometry(QtCore.QRect(20, 720, 622, 520))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_ = MplCanvas()
        self.createAnimationStart()
        self.graph__timer = self.graph_.new_timer(50)
        self.graph__timer.add_callback(self._update_canvas)
        self.graph__timer.start()

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_)
        self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph.setLayout(self.graph_layout)

        self.scrollCentral.setWidget(self.interpolation)

        self.valuesUI()
        self.actionsUI()

    def hiddenReadyWidget(self):
        self.readyWidget.setVisible(False)
        self.initWidget.setVisible(True)

        self.logic.method_title = "None"
        self.method_box.setCurrentIndex(-1)
        self.check.setChecked(False)

        self.interpolation.setFixedSize(QtCore.QSize(self.width, self.height))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))

    def showReadyWidget(self):
        self.initWidget.setVisible(False)
        self.readyWidget.setVisible(True)

        expand = self.height * 2.2
        self.interpolation.setFixedSize(QtCore.QSize(self.width - 16, expand))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, expand))

    def valuesUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.getClipboardButton.setText(_translate("MainWindow", "From Clipboard"))
        self.getEXCELButton.setText(_translate("MainWindow", "From EXCEL"))

        self.labelCheck.setText(_translate("MainWindow", "Center table"))

        self.method_box.setCurrentIndex(-1)
        self.method_box.setItemText(0, _translate("MainWindow", "Taylor"))
        self.method_box.setItemText(1, _translate("MainWindow", "Newton"))
        self.method_box.setItemText(2, _translate("MainWindow", "Lagrange"))

        self.clearButton.setText("Clear")

        self.progressiveLabel.setText("Interpolation progressive:")
        self.progressiveMath.setText("DDP=?")
        self.progressiveMathE.setText("DDP=?")

        self.regressionLabel.setText("Interpolation regression:")
        self.regressionMath.setText("DDR=?")
        self.regressionMathE.setText("DDP=?")

    def actionsUI(self):
        self.getClipboardButton.clicked.connect(self.getClipboard)
        self.clearButton.clicked.connect(self.returnInitWidget)
        self.check.clicked.connect(self.checkClicked)

        self.method_box.currentIndexChanged.connect(self.handleChangeMethod)

    def checkClicked(self):
        from modules.TableModel import TableModel

        if self.logic.method_title == "Newton":
            if self.check.isChecked():
                model = TableModel(DataFrame(self.logic.centerTable))
            else:
                model = TableModel(DataFrame(self.logic.table))
            self.tableWidget.setModel(model)

    def returnInitWidget(self):
        from modules.TableModel import TableModel

        self.graph_.axes.cla()
        self.graph_.draw()

        self.hiddenReadyWidget()

        self.logic.clear()

        model = TableModel(DataFrame(self.init_table))
        self.tableWidget.setModel(model)

    def showPolynomial(self, polynomial):
        self.showPoints()

        x = self.logic.base["x"]
        infinite = np.linspace(x[0], x[len(x) - 1], 150)

        print(self.logic.method_title)
        print(
            f"Real: {self.logic.base['f(x)'][0]}\n P: {polynomial(x[0])}\n -: {abs(polynomial(x[0]) - self.logic.base['f(x)'][0])}",
        )
        print(
            f"Real: {self.logic.base['f(x)'][len(x) - 1]}\n P: {polynomial(x[len(x) - 1])} -: {abs(polynomial(x[len(x) - 1]) - self.logic.base['f(x)'][len(x) - 1])}",
        )

        self.graph_.axes.plot(
            infinite,
            [polynomial(i) for i in infinite],
            color="gray",
            linestyle="--",
            zorder=1,
        )

        self.graph_.draw()

    def showPoints(self):
        self.graph_.axes.cla()

        x = self.logic.base["x"]
        y = self.logic.base["f(x)"]

        self.graph_.axes.scatter(
            x,
            y,
            color="red",
            marker="+",
            zorder=2,
        )

        self.graph_.draw()

    def initReadyWidget(self):
        from modules.TableModel import TableModel

        self.graph_.axes.cla()

        self.showPoints()

        self.logic.centerTable = {}
        self.logic.table = {}

        df = DataFrame(self.logic.base)
        model = TableModel(df)
        self.tableWidget.setModel(model)

        self.progressiveMath.setText("DDP=?")
        self.progressiveMathE.setText("DDP=?")
        self.regressionMath.setText("DDR=?")
        self.regressionMathE.setText("DDR=?")

    def handleChangeMethod(self):
        currentIndex = self.method_box.currentIndex()

        self.initReadyWidget()

        if currentIndex == 0:
            # self.runTaylor()
            return
        if currentIndex == 1:
            self.runNewton()
            return
        if currentIndex == 2:
            self.runLagrange()
            return

    def runLagrange(self):
        from modules.TableModel import TableModel

        self.logic.method_title = "Lagrange"

        n = len(self.logic.base["x"])
        p = lagrange(self.logic.base)

        self.progressiveLabel.setText("Interpolation Lagrange:")

        self.progressiveMath.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={p['solution']}$", 11)
        )

        self.progressiveMathE.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={p['expanded_latex']}$", 11)
        )

        self.regressionLabel.setText("")
        self.regressionMath.setText("")
        self.regressionMathE.setText("")

        self.showPolynomial(p["expanded"])

    def runNewton(self):
        from modules.TableModel import TableModel

        self.logic.method_title = "Newton"
        base = deepcopy(self.logic.base)

        self.logic.table = divided_diff(base)
        self.logic.centerTable = deepcopy(self.logic.table)

        n = len(self.logic.table["x"])

        normalize(self.logic.table, n)
        center(self.logic.centerTable, n)

        df = DataFrame(self.logic.table)
        model = TableModel(df)
        self.tableWidget.setModel(model)

        self.progressiveLabel.setText("Interpolation progressive:")
        self.regressionLabel.setText("Interpolation regression:")

        ddp = polynomialDDP(df)
        self.progressiveMath.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddp['solution']}$", 11)
        )
        self.progressiveMathE.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddp['expanded_latex']}$", 11)
        )

        ddr = polynomialDDR(df)
        self.regressionMath.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddr['solution']}$", 11)
        )
        self.regressionMathE.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddr['expanded_latex']}$", 11)
        )

        self.showPolynomial(ddp["expanded"])

    def getClipboard(self):
        self.showReadyWidget()

        self.logic.base = read_clipboard().to_dict(orient="list")

        self.initReadyWidget()
