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

        width = MainWindow.min_size.width() * 2
        height = MainWindow.min_size.height()

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
        self.scrollCentral.setFixedSize(QtCore.QSize(width, height - 100))

        self.interpolation = QtWidgets.QWidget()
        self.interpolation.setFixedSize(QtCore.QSize(width - 90, height * 1.6))

        self.window = QtWidgets.QFrame(self.interpolation)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(0, 0, width, height * 2))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        self.getClipboardButton = QtWidgets.QPushButton(self.window)
        self.getClipboardButton.setEnabled(True)
        self.getClipboardButton.setGeometry(QtCore.QRect(20, 20, 150, 40))
        self.getClipboardButton.setMaximumSize(QtCore.QSize(150, 40))
        self.getClipboardButton.setFont(font)
        self.getClipboardButton.setStyleSheet("")
        self.getClipboardButton.setObjectName("getClipboardButton")

        self.getEXCELButton = QtWidgets.QPushButton(self.window)
        self.getEXCELButton.setEnabled(True)
        self.getEXCELButton.setMaximumSize(QtCore.QSize(150, 40))
        self.getEXCELButton.setGeometry(QtCore.QRect(180, 20, 150, 40))
        self.getEXCELButton.setFont(font)
        self.getEXCELButton.setStyleSheet("")
        self.getEXCELButton.setObjectName("getEXCELButton")

        self.clearButton = QtWidgets.QPushButton(self.window)
        self.clearButton.setEnabled(True)
        self.clearButton.setMaximumSize(QtCore.QSize(150, 40))
        self.clearButton.setGeometry(QtCore.QRect(340, 20, 150, 40))
        self.clearButton.setFont(font)
        self.clearButton.setStyleSheet("")
        self.clearButton.setObjectName("clearButton")

        self.check = QtWidgets.QCheckBox(self.window)
        self.check.setStyleSheet("")
        self.check.setObjectName("check")
        self.check.setGeometry(QtCore.QRect(20, 70, 40, 40))

        self.tableWidget = QtWidgets.QTableView(self.window)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 120, 950, 500))
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")

        model = TableModel(self.init_table)
        self.tableWidget.setModel(model)

        self.progressiveLabel = QtWidgets.QLabel(self.window)
        self.progressiveLabel.setStyleSheet("")
        self.progressiveLabel.setObjectName("label")
        self.progressiveLabel.setGeometry(QtCore.QRect(20, 620, width, 200))

        self.progressiveMath = QtWidgets.QLabel(self.window)
        self.progressiveMath.setStyleSheet("")
        self.progressiveMath.setObjectName("label")
        self.progressiveMath.setGeometry(QtCore.QRect(20, 650, width, 200))

        self.progressiveMathE = QtWidgets.QLabel(self.window)
        self.progressiveMathE.setStyleSheet("")
        self.progressiveMathE.setObjectName("label")
        self.progressiveMathE.setGeometry(QtCore.QRect(20, 680, width, 200))

        self.regressionLabel = QtWidgets.QLabel(self.window)
        self.regressionLabel.setStyleSheet("")
        self.regressionLabel.setObjectName("label")
        self.regressionLabel.setGeometry(QtCore.QRect(20, 710, width, 200))

        self.regressionMath = QtWidgets.QLabel(self.window)
        self.regressionMath.setStyleSheet("")
        self.regressionMath.setObjectName("label")
        self.regressionMath.setGeometry(QtCore.QRect(20, 740, width, 200))

        self.regressionMathE = QtWidgets.QLabel(self.window)
        self.regressionMathE.setStyleSheet("")
        self.regressionMathE.setObjectName("label")
        self.regressionMathE.setGeometry(QtCore.QRect(20, 770, width, 200))

        self.scrollCentral.setWidget(self.interpolation)

        self.valuesUI()
        self.actionsUI()

    def valuesUI(self):
        self.getClipboardButton.setText("From Clipboard")
        self.getEXCELButton.setText("From EXCEL")
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

        self.logic.clear()

        model = TableModel(DataFrame(self.init_table))
        self.tableWidget.setModel(model)

    def getClipboard(self):
        from modules.TableModel import TableModel

        self.logic.base = read_clipboard().to_dict(orient="list")
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
            MathToQPixmap(f"$P_{n-1}={ddp['solution']}$", 11)
        )
        self.progressiveMathE.setPixmap(
            MathToQPixmap(f"$P_{n-1}={ddp['expanded_latex']}$", 11)
        )

        ddr = polynomialDDR(df)
        self.regressionMath.setPixmap(MathToQPixmap(f"$P_{n-1}={ddr['solution']}$", 11))
        self.regressionMathE.setPixmap(
            MathToQPixmap(f"$P_{n-1}={ddr['expanded_latex']}$", 11)
        )
