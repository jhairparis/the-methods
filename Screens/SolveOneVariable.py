from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from Screens.components.Select import Select
from modules.mica.styleSheet import ApplyMenuBlur, setStyleSheet
import time
import numpy as np
from lib.Logic import Logic
from modules.MplCanvas import MplCanvas
from modules.TableModel import TableModel
from pandas import DataFrame
from lib.methods.newton import derivative
from Screens.components.Dialog import CustomDialog
from plyer import notification
from sympy import latex, sympify
from modules.MathToQPixmap import MathToQPixmap
from modules.mica.theme.getTheme import getTheme, rgb2hex

# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class Ui_SolveOneVariable(object):
    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        self.graph_line.set_data(t, np.sin(t + time.time()))
        self.graph_line.figure.canvas.draw()

    def createAnimationStart(self):
        t = np.linspace(0, 10, 101)
        (self.graph_line,) = self.graph_.axes.plot(
            t, np.sin(t + time.time()), color=rgb2hex(getTheme()["accent"])
        )

    def setupUi(self, MainWindow):
        self.logic = Logic()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(980, 650)
        MainWindow.setMinimumSize(QtCore.QSize(980, 650))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(11)
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
        font.setPointSize(11)
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

        self.createAnimationStart()
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

        self.method_box = Select(self.form)
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
        font.setPointSize(11)
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
        font.setPointSize(11)
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

        self.valuesUI(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionsUI(MainWindow)

    def valuesUI(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The methods"))

        self.label_method.setText(_translate("MainWindow", "Select method"))
        self.label_fn.setText(_translate("MainWindow", "Write the function"))
        self.label_iteration.setText(_translate("MainWindow", "Iteration"))
        self.label_tolerance.setText(_translate("MainWindow", "Tolerance"))
        self.label_x0.setText(_translate("MainWindow", "X0"))
        self.label_x1.setText(_translate("MainWindow", "X1"))

        self.x_left.setPlaceholderText(_translate("MainWindow", "limit x left"))
        self.x_right.setPlaceholderText(_translate("MainWindow", "limit x right"))
        self.y_up.setPlaceholderText(_translate("MainWindow", "limit y up"))
        self.y_down.setPlaceholderText(_translate("MainWindow", "limit y down"))

        self.method_box.setCurrentIndex(-1)
        self.method_box.setItemText(0, _translate("MainWindow", "Bisection"))
        self.method_box.setItemText(1, _translate("MainWindow", "Newton"))
        self.method_box.setItemText(2, _translate("MainWindow", "Secant"))
        self.method_box.setItemText(3, _translate("MainWindow", "Point"))

        self.fn_box.setPlaceholderText(_translate("MainWindow", "x**2"))

        self.tolerance_box.setPlaceholderText(_translate("MainWindow", "1e-3"))

        self.x1_box.setMinimum(-1000)
        self.x1_box.setMaximum(1000)

        self.x0_box.setMinimum(-1000)
        self.x0_box.setMaximum(1000)

        self.iteration_box.setMinimum(1)
        self.iteration_box.setMaximum(9999)

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

        ApplyMenuBlur(self.menuFile.winId().__int__())
        ApplyMenuBlur(self.actionNew.winId().__int__())
        ApplyMenuBlur(self.menuEdit.winId().__int__())
        ApplyMenuBlur(self.menuHelp.winId().__int__())

    def create_main_graph(self):
        self.graph_.axes.cla()

        if (
            not hasattr(self.x_left, "value")
            or not hasattr(self.x_right, "value")
            or not hasattr(self.y_up, "value")
            or not hasattr(self.y_down, "value")
            or not hasattr(self.fn_box, "value")
            or self.fn_box.value == ""
            or self.x_left.value == "-"
            or self.x_right.value == "-"
            or self.y_up.value == "-"
            or self.y_down.value == "-"
        ):
            return

        x_left = float(self.x_left.value)
        x_right = float(self.x_right.value)
        y_up = float(self.y_up.value)
        y_down = float(self.y_down.value)

        infinite = np.linspace(x_left, x_right, 101)

        gen = self.logic.gen_fn(self.fn_box.value)
        self.logic.fn = gen[0]

        if gen[1] == False:
            return

        ltx = latex(sympify(self.fn_box.value))
        self.label_fn.setPixmap(MathToQPixmap(f"${ltx}$", 11))

        (self.graph_line,) = self.graph_.axes.plot(
            infinite,
            [self.logic.fn(i) for i in infinite],
            color="gray",
            linestyle="--",
            zorder=1,
        )

        self.graph_line.axes.set_xlim(xmin=x_left, xmax=x_right)
        self.graph_line.axes.set_ylim(ymax=y_up, ymin=y_down)

        self.graph_.draw()

    def handleClickMethods(self):
        try:
            self.create_main_graph()
            method = self.method_box.currentIndex()
            x0 = self.x0_box.value()
            x1 = self.x1_box.value()
            tol = float(self.tolerance_box.value)
            steps = self.iteration_box.value()
            str_fn = self.fn_box.value
            fn = self.logic.gen_fn(str_fn)[0]

            m = self.logic.get_method(method)

            deri = derivative(str_fn)

            if method == 1:
                p = m(
                    logic=self.logic,
                    fun=fn,
                    deri=deri,
                    x_a=x0,
                    tol=tol,
                    steps=steps,
                    x_b=x1,
                )

                self.graph_.axes.scatter(
                    x0, fn(x0), label="X0", color="violet", zorder=3
                )
            elif method == 3:
                dlg = CustomDialog(str_fn)
                if dlg.exec():
                    p = m(
                        logic=self.logic,
                        g=dlg.sol_fn,
                        fun=fn,
                        x_a=x0,
                        x_b=x1,
                        tol=tol,
                        steps=steps,
                    )
                else:
                    print("Cancel!")

            else:
                p = m(
                    logic=self.logic,
                    fun=fn,
                    x_a=x0,
                    x_b=x1,
                    tol=tol,
                    steps=steps,
                )

            df = self.logic.show_table(True)

            model = TableModel(df)
            self.tableWidget.setModel(model)

            # render thing in graph

            if method == 0:
                var = np.linspace(x0, x1, 101)
                self.graph_.axes.plot(
                    var, [fn(i) for i in var], label="Range", color="red", zorder=2
                )

            self.graph_.axes.scatter(p, 0, label="Root", color="yellow", zorder=3)

            self.add_marks(method, df, fn)

            self.graph_.draw()

            return notification.notify(
                title="Result",
                message=f"{self.logic.method_title} method: {p}",
                app_icon=None,
                timeout=10,
            )
        except:
            return notification.notify(
                title="Error",
                message="Please fill all fields",
                app_icon=None,
                timeout=2,
            )

    def handleChangeMethod(self):
        model = self.tableWidget.model()
        if model:
            model.deleteLater()
            df = DataFrame(
                {
                    "Wait...": [1,2,3,5,8,13,21],
                }
            )
            model = TableModel(df)
            self.tableWidget.setModel(model)

        if len(self.logic.method_title) >= 1:
            self.create_main_graph()

    def subscription(self, value, who):
        self.graph__timer.stop()
        if who == 0:
            self.graph_.axes.cla()

            if len(value) >= 1:
                self.fn_box.value = value.strip()
                self.create_main_graph()
            else:
                self.createAnimationStart()
                self.graph__timer.start()
                self.graph_.draw()
            return

        if who == 1:
            self.tolerance_box.value = value
            return
        if who == 2:
            self.x_left.value = value
            self.create_main_graph()
            return
        if who == 3:
            self.x_right.value = value
            self.create_main_graph()
            return
        if who == 4:
            self.y_up.value = value
            self.create_main_graph()
            return
        if who == 5:
            self.y_down.value = value
            self.create_main_graph()
            return

    def add_marks(self, method, df, fn):
        ps = ["Pn", "p", "Xn", "x"]
        for i in df.index:
            self.graph_.axes.scatter(
                float(df[ps[method]].get(i)),
                fn(float(df[ps[method]].get(i))),
                label=f"{i} ite",
                marker="*",
                alpha=0.8,
                s=50,
                zorder=3,
            )
        return

    def actionsUI(self, MainWindow):
        self.pushButton.clicked.connect(self.handleClickMethods)

        self.method_box.currentIndexChanged.connect(self.handleChangeMethod)

        self.fn_box.textChanged.connect(lambda v: self.subscription(v, 0))
        self.tolerance_box.textChanged.connect(lambda v: self.subscription(v, 1))
        self.x_left.textChanged.connect(lambda v: self.subscription(v, 2))
        self.x_right.textChanged.connect(lambda v: self.subscription(v, 3))
        self.y_up.textChanged.connect(lambda v: self.subscription(v, 4))
        self.y_down.textChanged.connect(lambda v: self.subscription(v, 5))
        return
