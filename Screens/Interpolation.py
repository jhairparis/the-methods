from PySide2 import QtCore, QtGui, QtWidgets
from copy import deepcopy
from pandas import DataFrame, read_clipboard
from Screens.components.Select import Select
from plyer import notification
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
from lib.interpolation.taylors import taylor
from Screens.components.ConfirmFunction import ConfirmFunction
from modules.MathToQPixmap import MathToQPixmap
from modules.MplCanvas import MplCanvas
from modules.mica.theme.getTheme import getTheme, rgb2hex
# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


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

        self.instructions = QtWidgets.QLabel(self.initWidget)
        self.instructions.setEnabled(True)
        self.instructions.setMinimumSize(QtCore.QSize(200, 40))
        self.instructions.setGeometry(
            QtCore.QRect(
                (self.width - 200) / 2, (self.height - 63 - 120) / 2, 200, 10
            )
        )
        self.instructions.setStyleSheet("")
        self.instructions.setObjectName("instructions")

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

        self.labelMethod = QtWidgets.QLabel(self.readyWidget)
        self.labelMethod.setEnabled(True)
        self.labelMethod.setMinimumSize(QtCore.QSize(95, 40))
        self.labelMethod.setGeometry(QtCore.QRect(20, 20, 95, 10))
        self.labelMethod.setStyleSheet("")
        self.labelMethod.setObjectName("labelMethod")

        self.method_box = Select(self.readyWidget)
        self.method_box.setGeometry(QtCore.QRect(20, 60, 250, 40))
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

        self.labelCheck = QtWidgets.QLabel(self.readyWidget)
        self.labelCheck.setEnabled(True)
        self.labelCheck.setMinimumSize(QtCore.QSize(95, 40))
        self.labelCheck.setGeometry(QtCore.QRect(300, 20, 95, 40))
        self.labelCheck.setStyleSheet("")
        self.labelCheck.setObjectName("labelCheck")
        self.labelCheck.setVisible(False)

        self.check = QtWidgets.QCheckBox(self.readyWidget)
        self.check.setStyleSheet("")
        self.check.setObjectName("check")
        self.check.setGeometry(QtCore.QRect(335, 65, 40, 40))
        self.check.setVisible(False)

        self.clearButton = QtWidgets.QPushButton(self.readyWidget)
        self.clearButton.setEnabled(True)
        self.clearButton.setMaximumSize(QtCore.QSize(150, 40))
        self.clearButton.setGeometry(QtCore.QRect(self.width - 180, 20, 150, 40))
        self.clearButton.setFont(font)
        self.clearButton.setStyleSheet("")
        self.clearButton.setObjectName("clearButton")

        self.animation = QtWidgets.QPushButton(self.readyWidget)
        self.animation.setEnabled(True)
        self.animation.setMaximumSize(QtCore.QSize(150, 40))
        self.animation.setGeometry(QtCore.QRect(self.width - 180, 70, 150, 40))
        self.animation.setFont(font)
        self.animation.setStyleSheet("")
        self.animation.setObjectName("animation")

        self.tableWidget = QtWidgets.QTableView(self.readyWidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 120, self.width - 50, 470))
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setStyleSheet("background:red;")

        model = TableModel(self.init_table)
        self.tableWidget.setModel(model)

        self.graph = QtWidgets.QWidget(self.readyWidget)
        self.graph.setGeometry(QtCore.QRect(20, 610, 622, 520))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_ = MplCanvas()
        self.createAnimationStart()
        self.graph__timer = self.graph_.new_timer(50)
        self.graph__timer.add_callback(self._update_canvas)
        self.graph__timer.start()

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_)
        # self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph.setLayout(self.graph_layout)

        self.titleLabel = QtWidgets.QLabel(self.readyWidget)
        self.titleLabel.setStyleSheet("")
        self.titleLabel.setObjectName("label")
        self.titleLabel.setGeometry(QtCore.QRect(650, 620, self.width, 30))

        self.fistMath = QtWidgets.QLabel(self.readyWidget)
        self.fistMath.setStyleSheet("")
        self.fistMath.setObjectName("label")
        self.fistMath.setGeometry(QtCore.QRect(650, 660, self.width, 30))

        self.firstMathE = QtWidgets.QLabel(self.readyWidget)
        self.firstMathE.setStyleSheet("")
        self.firstMathE.setObjectName("label")
        self.firstMathE.setGeometry(QtCore.QRect(650, 700, self.width, 30))

        self.titleLabel2 = QtWidgets.QLabel(self.readyWidget)
        self.titleLabel2.setStyleSheet("")
        self.titleLabel2.setObjectName("label")
        self.titleLabel2.setGeometry(QtCore.QRect(650, 740, self.width, 30))
        self.titleLabel2.setVisible(False)

        self.secondMath = QtWidgets.QLabel(self.readyWidget)
        self.secondMath.setStyleSheet("")
        self.secondMath.setObjectName("label")
        self.secondMath.setGeometry(QtCore.QRect(650, 780, self.width, 20))
        self.secondMath.setVisible(False)

        self.secondMathE = QtWidgets.QLabel(self.readyWidget)
        self.secondMathE.setStyleSheet("")
        self.secondMathE.setObjectName("label")
        self.secondMathE.setGeometry(QtCore.QRect(650, 820, self.width, 20))
        self.secondMathE.setVisible(False)

        self.scrollCentral.setWidget(self.interpolation)

        self.valuesUI()
        self.actionsUI()

    def valuesUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.instructions.setText(_translate("MainWindow", "Select table of values"))

        self.getClipboardButton.setText(_translate("MainWindow", "From Clipboard"))
        self.getEXCELButton.setText(_translate("MainWindow", "From EXCEL"))

        self.labelCheck.setText(_translate("MainWindow", "Center table"))

        self.labelMethod.setText(_translate("MainWindow", "Method:"))

        self.method_box.setCurrentIndex(-1)
        self.method_box.setItemText(0, _translate("MainWindow", "Taylor"))
        self.method_box.setItemText(1, _translate("MainWindow", "Newton"))
        self.method_box.setItemText(2, _translate("MainWindow", "Lagrange"))

        self.clearButton.setText(_translate("MainWindow", "Clear"))

        self.animation.setText(_translate("MainWindow", "Animation"))

        self.titleLabel.setText(_translate("MainWindow", "Interpolation:"))
        self.fistMath.setText("F(x)=?")
        self.firstMathE.setText("F(x)=?")

        self.titleLabel2.setText(_translate("MainWindow", "Interpolation:"))
        self.secondMath.setText("F2(x)=?")
        self.secondMathE.setText("F2(x)=?")

    def actionsUI(self):
        self.getClipboardButton.clicked.connect(self.getClipboard)
        self.getEXCELButton.clicked.connect(
            lambda: notification.notify(
                title="Error",
                message="⚠️ This function will be soon available ⚠️",
                app_icon=None,
                timeout=2,
            )
        )
        self.clearButton.clicked.connect(self.returnInitWidget)
        self.check.clicked.connect(self.checkClicked)

        self.method_box.currentIndexChanged.connect(self.handleChangeMethod)

        # self.animation.clicked.connect(lambda: print(self.tableWidget.height()))

    def getClipboard(self):
        read = read_clipboard().to_dict(orient="list")

        if not "x" in read and not "f(x)" in read:
            notification.notify(
                title="Error",
                message="Please copy table with headers 'x' and 'f(x)'",
                app_icon=None,
                timeout=2,
            )
            return None

        self.logic.base = read

        self.showReadyWidget()
        self.initReadyWidget()

    def returnInitWidget(self):
        from modules.TableModel import TableModel

        self.graph_.axes.cla()
        self.graph_.draw()

        self.readyWidget.setVisible(False)
        self.initWidget.setVisible(True)

        self.logic.method_title = "None"
        self.method_box.setCurrentIndex(-1)
        self.check.setChecked(False)

        self.tableWidget.setGeometry(QtCore.QRect(20, 120, self.width - 50, 470))
        self.graph.setGeometry(QtCore.QRect(20, 610, 622, 520))

        self.titleLabel.setGeometry(QtCore.QRect(650, 620, self.width, 30))
        self.fistMath.setGeometry(QtCore.QRect(650, 660, self.width, 30))
        self.firstMathE.setGeometry(QtCore.QRect(650, 700, self.width, 30))
        self.titleLabel2.setGeometry(QtCore.QRect(650, 740, self.width, 30))
        self.secondMath.setGeometry(QtCore.QRect(650, 780, self.width, 20))
        self.secondMathE.setGeometry(QtCore.QRect(650, 820, self.width, 20))

        self.interpolation.setFixedSize(QtCore.QSize(self.width, self.height))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))

        self.logic.clear()

        model = TableModel(DataFrame(self.init_table))
        self.tableWidget.setModel(model)

    def checkClicked(self):
        from modules.TableModel import TableModel

        if self.logic.method_title == "Newton":
            if self.check.isChecked():
                model = TableModel(DataFrame(self.logic.centerTable))
            else:
                model = TableModel(DataFrame(self.logic.table))
            self.tableWidget.setModel(model)

    def handleChangeMethod(self):
        currentIndex = self.method_box.currentIndex()

        self.initReadyWidget()

        self.labelCheck.setVisible(False)
        self.check.setVisible(False)
        self.check.setChecked(False)
        self.titleLabel2.setVisible(False)
        self.secondMath.setVisible(False)
        self.secondMathE.setVisible(False)

        if currentIndex == 0:
            self.runTaylor()
            return
        if currentIndex == 1:
            self.labelCheck.setVisible(True)
            self.check.setVisible(True)
            self.titleLabel2.setVisible(True)
            self.secondMath.setVisible(True)
            self.secondMathE.setVisible(True)
            self.runNewton()
            return
        if currentIndex == 2:
            self.runLagrange()
            return

    def showPolynomial(self, polynomial):
        self.showPoints()

        x = self.logic.base["x"]
        infinite = np.linspace(x[0], x[len(x) - 1], 150)

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

    def showReadyWidget(self):
        self.initWidget.setVisible(False)
        self.readyWidget.setVisible(True)

        expand = self.height * 2.2
        self.interpolation.setFixedSize(QtCore.QSize(self.width - 16, expand))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, expand))

    def initReadyWidget(self):
        from modules.TableModel import TableModel

        self.graph_.axes.cla()

        self.showPoints()

        self.logic.centerTable = {}
        self.logic.table = {}

        df = DataFrame(self.logic.base)
        model = TableModel(df)
        self.tableWidget.setModel(model)
        tableHeight = (df["x"].count() * 31) + 32

        if tableHeight < 470:
            self.tableWidget.setGeometry(
                QtCore.QRect(20, 120, self.width - 50, tableHeight)
            )

            self.graph.setGeometry(QtCore.QRect(20, 120 + tableHeight + 20, 622, 520))

            self.titleLabel.setGeometry(
                QtCore.QRect(650, 120 + tableHeight + 10, self.width, 30)
            )
            self.fistMath.setGeometry(
                QtCore.QRect(650, 120 + tableHeight + 20 + 30, self.width, 30)
            )
            self.firstMathE.setGeometry(
                QtCore.QRect(650, 120 + tableHeight + 30 + 30 + 30, self.width, 30)
            )
            self.titleLabel2.setGeometry(
                QtCore.QRect(650, 120 + tableHeight + 40 + 30 + 30 + 30, self.width, 30)
            )
            self.secondMath.setGeometry(
                QtCore.QRect(
                    650, 120 + tableHeight + 50 + 30 + 30 + 30 + 30, self.width, 20
                )
            )
            self.secondMathE.setGeometry(
                QtCore.QRect(
                    650, 120 + tableHeight + 60 + 30 + 30 + 30 + 30 + 30, self.width, 20
                )
            )

        self.fistMath.setText("F(x)=?")
        self.firstMathE.setText("F(x)=?")
        self.secondMath.setText("F2(x)=?")
        self.secondMathE.setText("F2(x)=?")

    def runTaylor(self):
        self.logic.method_title = "Taylor"

        dlg = ConfirmFunction()

        if dlg.exec():
            n = int(dlg.n)
            s = dlg.fn
            x_0 = float(dlg.x_0)

            p = taylor(s, n, x_0)

            self.titleLabel.setText("Interpolation Taylor's:")

            self.fistMath.setPixmap(MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={p}$", 11))
            return

    def runLagrange(self):
        self.logic.method_title = "Lagrange"

        n = len(self.logic.base["x"])
        p = lagrange(self.logic.base)

        self.titleLabel.setText("Interpolation Lagrange:")

        self.fistMath.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={p['solution']}$", 11)
        )

        self.firstMathE.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={p['expanded_latex']}$", 11)
        )

        self.titleLabel2.setText("")
        self.secondMath.setText("")
        self.secondMathE.setText("")

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

        self.titleLabel.setText("Interpolation progressive:")
        self.titleLabel2.setText("Interpolation regression:")

        ddp = polynomialDDP(df)
        self.fistMath.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddp['solution']}$", 11)
        )
        self.firstMathE.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddp['expanded_latex']}$", 11)
        )

        ddr = polynomialDDR(df)
        self.secondMath.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddr['solution']}$", 11)
        )
        self.secondMathE.setPixmap(
            MathToQPixmap(f"$P_{'{'+str(n-1)+'}'}={ddr['expanded_latex']}$", 11)
        )

        self.showPolynomial(ddp["expanded"])
