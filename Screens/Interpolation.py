from PySide2 import QtCore, QtGui, QtWidgets
from copy import deepcopy
from pandas import DataFrame, read_clipboard
from lib.Logic2 import Logic2

from lib.interpolation.newton import (
    center,
    divided_diff,
    normalize,
    polynomialDDP,
    polynomialDDR,
)
from modules.MathToQPixmap import MathToQPixmap


class Ui_Interpolation(object):
    init_table = DataFrame(
        {
            "Wait...": [1, 2, 3, 5, 8, 13, 21],
        }
    )

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

        self.clearButton = QtWidgets.QPushButton(self.readyWidget)
        self.clearButton.setEnabled(True)
        self.clearButton.setMaximumSize(QtCore.QSize(150, 40))
        self.clearButton.setGeometry(QtCore.QRect(self.width - 180, 20, 150, 40))
        self.clearButton.setFont(font)
        self.clearButton.setStyleSheet("")
        self.clearButton.setObjectName("clearButton")

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

        self.scrollCentral.setWidget(self.interpolation)

        self.valuesUI()
        self.actionsUI()

    def hiddenReadyWidget(self):
        self.readyWidget.setVisible(False)
        self.initWidget.setVisible(True)

        self.interpolation.setFixedSize(QtCore.QSize(self.width, self.height))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))

    def showReadyWidget(self):
        self.initWidget.setVisible(False)
        self.readyWidget.setVisible(True)

        self.interpolation.setFixedSize(
            QtCore.QSize(self.width - 16, self.height * 1.6)
        )
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height * 1.6))

    def valuesUI(self):
        self.getClipboardButton.setText("From Clipboard")
        self.getEXCELButton.setText("From EXCEL")

        self.labelCheck.setText("Center table")
        self.clearButton.setText("Clear")

        self.progressiveLabel.setText("Interpolation progressive:")
        self.progressiveMath.setText("DDP=?")

        self.regressionLabel.setText("Interpolation regression:")
        self.regressionMath.setText("DDR=?")

    def actionsUI(self):
        self.getClipboardButton.clicked.connect(self.getClipboard)
        self.clearButton.clicked.connect(self.clear)
        self.check.clicked.connect(self.checkClicked)

    def checkClicked(self):
        from modules.TableModel import TableModel

        if self.check.isChecked():
            model = TableModel(DataFrame(self.logic.centerTable))
        else:
            model = TableModel(DataFrame(self.logic.table))

        self.tableWidget.setModel(model)

    def clear(self):
        from modules.TableModel import TableModel

        self.hiddenReadyWidget()

        self.logic.clear()

        model = TableModel(DataFrame(self.init_table))
        self.tableWidget.setModel(model)

    def runMethod(self):
        from modules.TableModel import TableModel

        base = deepcopy(self.logic.base)

        self.logic.table = divided_diff(base)
        self.logic.centerTable = deepcopy(self.logic.table)

        n = len(self.logic.table["x"])

        normalize(self.logic.table, n)
        center(self.logic.centerTable, n)

        df = DataFrame(self.logic.table)
        model = TableModel(df)
        self.tableWidget.setModel(model)

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

    def getClipboard(self):
        from modules.TableModel import TableModel

        self.showReadyWidget()

        self.logic.base = read_clipboard().to_dict(orient="list")

        self.runMethod()

        df = DataFrame(self.logic.base)
        model = TableModel(df)
        self.tableWidget.setModel(model)
