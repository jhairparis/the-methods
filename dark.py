from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from winreg import *
import time
import numpy as np
from lib.Logic import Logic
from modules.MplCanvas import MplCanvas
from modules.mica.styleSheet import setStyleSheet
from icons import styledark_rc

# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from modules.TableModel import TableModel
from pandas import DataFrame


class Ui_MainWindow(object):
    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        self.graph_line.set_data(t, np.sin(t + time.time()))
        self.graph_line.figure.canvas.draw()

    def setupUi(self, MainWindow):
        self.logic = Logic()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(980, 650)
        MainWindow.setMinimumSize(QtCore.QSize(980, 650))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        setStyleSheet(MainWindow)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.scrollCentral = QtWidgets.QScrollArea()

        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(50)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.window = QtWidgets.QFrame(self.centralwidget)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(19, 0, 991, 1302))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        # Right side
        self.graph = QtWidgets.QWidget(self.window)
        self.graph.setGeometry(QtCore.QRect(0, 0, 622, 520))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_ = MplCanvas()

        t = np.linspace(0, 10, 101)
        (self.graph_line,) = self.graph_.axes.plot(t, np.sin(t + time.time()))
        self.graph__timer = self.graph_.new_timer(50)
        self.graph__timer.add_callback(self._update_canvas)
        self.graph__timer.start()

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_)
        # self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph_control = QtWidgets.QWidget(self.window)
        self.graph_control_layout = QtWidgets.QHBoxLayout()

        self.x_left = QtWidgets.QLineEdit(self.graph_control)
        self.x_left.setEnabled(True)
        self.x_left.setMinimumSize(QtCore.QSize(95, 40))
        self.x_left.setStyleSheet("")
        self.x_left.setObjectName("x_left")

        self.x_right = QtWidgets.QLineEdit(self.graph_control)
        self.x_right.setEnabled(True)
        self.x_right.setMinimumSize(QtCore.QSize(95, 40))
        self.x_right.setStyleSheet("")
        self.x_right.setObjectName("x_right")

        self.y_up = QtWidgets.QLineEdit(self.graph_control)
        self.y_up.setEnabled(True)
        self.y_up.setMinimumSize(QtCore.QSize(95, 40))
        self.y_up.setStyleSheet("")
        self.y_up.setObjectName("y_up")

        self.y_down = QtWidgets.QLineEdit(self.graph_control)
        self.y_down.setEnabled(True)
        self.y_down.setMinimumSize(QtCore.QSize(95, 40))
        self.y_down.setStyleSheet("")
        self.y_down.setObjectName("y_up")

        self.graph_control_layout.addWidget(self.x_left)
        self.graph_control_layout.addWidget(self.x_right)
        self.graph_control_layout.addWidget(self.y_up)
        self.graph_control_layout.addWidget(self.y_down)

        self.graph_control.setLayout(self.graph_control_layout)

        self.graph_layout.addWidget(self.graph_control)

        self.graph.setLayout(self.graph_layout)

        # Left side
        self.form = QtWidgets.QWidget(self.window)
        self.form.setGeometry(QtCore.QRect(641, 0, 320, 520))
        # self.form.setStyleSheet("background:red;")

        self.label_method = QtWidgets.QLabel(self.form)
        self.label_method.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_method.setObjectName("label_method")

        self.method_box = QtWidgets.QComboBox(self.form)
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

        self.label_fn = QtWidgets.QLabel(self.form)
        self.label_fn.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_fn.setObjectName("label_fn")

        self.fn_box = QtWidgets.QLineEdit(self.form)
        self.fn_box.setEnabled(True)
        self.fn_box.setMinimumSize(QtCore.QSize(181, 40))
        self.fn_box.setStyleSheet("")
        self.fn_box.setObjectName("fn_box")

        self.label_iteration = QtWidgets.QLabel(self.form)
        self.label_iteration.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_iteration.setObjectName("label_iteration")

        self.iteration_box = QtWidgets.QSpinBox(self.window)
        self.iteration_box.setEnabled(True)
        self.iteration_box.setMinimum(1)
        self.iteration_box.setMaximum(9999)
        self.iteration_box.setGeometry(QtCore.QRect(50, 20, 190, 40))
        self.iteration_box.setStyleSheet("")
        self.iteration_box.setObjectName("iteration_box")

        self.label_tolerance = QtWidgets.QLabel(self.form)
        self.label_tolerance.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_tolerance.setObjectName("label_tolerance")

        self.tolerance_box = QtWidgets.QLineEdit(self.form)
        self.tolerance_box.setEnabled(True)
        self.tolerance_box.setMinimumSize(QtCore.QSize(181, 40))
        self.tolerance_box.setStyleSheet("")
        self.tolerance_box.setObjectName("tolerance_box")

        self.range = QtWidgets.QWidget(self.form)
        self.range_layout = QtWidgets.QHBoxLayout()
        self.range_layout.setContentsMargins(0, 0, 0, 0)
        self.range_layout.setSpacing(0)

        self.x0 = QtWidgets.QWidget(self.form)
        self.x0_layout = QtWidgets.QVBoxLayout()
        self.x0_layout.setSpacing(14)

        self.label_x0 = QtWidgets.QLabel(self.form)
        self.label_x0.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_x0.setObjectName("label_x0")

        self.x0_box = QtWidgets.QDoubleSpinBox(self.window)
        self.x0_box.setEnabled(True)
        self.x0_box.setMinimum(-1000)
        self.x0_box.setMaximum(1000)
        self.x0_box.setGeometry(QtCore.QRect(50, 70, 190, 40))
        self.x0_box.setStyleSheet("")
        self.x0_box.setObjectName("x0_box")

        self.x0_layout.addWidget(self.label_x0)
        self.x0_layout.addWidget(self.x0_box)

        self.x0.setLayout(self.x0_layout)

        self.x1 = QtWidgets.QWidget(self.form)
        self.x1_layout = QtWidgets.QVBoxLayout()
        self.x1_layout.setSpacing(14)

        self.label_x1 = QtWidgets.QLabel(self.form)
        self.label_x1.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_x1.setObjectName("label_x1")

        self.x1_box = QtWidgets.QDoubleSpinBox(self.form)
        self.x1_box.setEnabled(True)
        self.x1_box.setMinimum(-1000)
        self.x1_box.setMaximum(1000)
        self.x1_box.setGeometry(QtCore.QRect(50, 70, 190, 40))
        self.x1_box.setStyleSheet("")
        self.x1_box.setObjectName("x1_box")

        self.x1_layout.addWidget(self.label_x1)
        self.x1_layout.addWidget(self.x1_box)

        self.x1.setLayout(self.x1_layout)

        self.range_layout.addWidget(self.x0)
        self.range_layout.addWidget(self.x1)

        self.range.setLayout(self.range_layout)

        self.pushButton = QtWidgets.QPushButton(self.form)
        self.pushButton.setEnabled(True)
        self.pushButton.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")

        # put in layout
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setSpacing(14)

        self.form_layout.addRow(self.label_method)
        self.form_layout.addRow(self.method_box)

        self.form_layout.addRow(self.label_fn)
        self.form_layout.addRow(self.fn_box)

        self.form_layout.addRow(self.label_iteration)
        self.form_layout.addRow(self.iteration_box)

        self.form_layout.addRow(self.label_tolerance)
        self.form_layout.addRow(self.tolerance_box)

        self.form_layout.addRow(self.range)

        self.form_layout.addRow(self.pushButton)

        self.form.setLayout(self.form_layout)

        self.tableWidget = QtWidgets.QTableView(self.window)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(0, 526, 950, 500))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")

        model = TableModel(DataFrame(self.logic.data))
        self.tableWidget.setModel(model)

        self.scrollCentral.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollCentral.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollCentral.setWidgetResizable(True)
        self.scrollCentral.setWidget(self.centralwidget)

        MainWindow.setCentralWidget(self.scrollCentral)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 980, 63))
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
        MainWindow.setMenuBar(self.menuBar)
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setEnabled(True)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPlain_Text_Document = QtWidgets.QAction(MainWindow)
        self.actionPlain_Text_Document.setObjectName("actionPlain_Text_Document")
        self.actionRich_Text_Document = QtWidgets.QAction(MainWindow)
        self.actionRich_Text_Document.setObjectName("actionRich_Text_Document")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionAbout = QtWidgets.QAction(MainWindow)
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The methods"))

        self.label_method.setText(_translate("MainWindow", "Select method"))
        self.label_fn.setText(
            _translate("MainWindow", "Write the function (python syntax)")
        )
        self.label_iteration.setText(_translate("MainWindow", "Iteration"))
        self.label_tolerance.setText(_translate("MainWindow", "Tolerance"))
        self.label_x0.setText(_translate("MainWindow", "X0"))
        self.label_x1.setText(_translate("MainWindow", "X1"))

        self.x_left.setPlaceholderText(_translate("MainWindow", "limit x left"))
        self.x_right.setPlaceholderText(_translate("MainWindow", "limit x right"))
        self.y_up.setPlaceholderText(_translate("MainWindow", "limit y up"))
        self.y_down.setPlaceholderText(_translate("MainWindow", "limit y down"))

        self.method_box.setItemText(0, _translate("MainWindow", "Bisection"))
        self.method_box.setItemText(1, _translate("MainWindow", "Newton"))
        self.method_box.setItemText(2, _translate("MainWindow", "Secant"))
        self.method_box.setItemText(3, _translate("MainWindow", "Point"))

        self.fn_box.setPlaceholderText(_translate("MainWindow", "x**2"))

        self.tolerance_box.setPlaceholderText(_translate("MainWindow", "1e-3"))

        self.pushButton.setText(_translate("MainWindow", "Calculate"))

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
