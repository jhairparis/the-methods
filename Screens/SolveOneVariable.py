from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from Screens.components.Select import Select
import time
import numpy as np
from lib.Logic import Logic
from modules.MplCanvas import MplCanvas
from modules.TableModel import TableModel
from pandas import DataFrame
from lib.methods.newton import derivative
from Screens.components.ConfirmG import ConfirmG
from modules.Notification import notify
from sympy import latex, sympify
from modules.MathToQPixmap import MathToQPixmap
from modules.mica.theme.getTheme import getTheme, rgb2hex

# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class Ui_SolveOneVariable(object):
    def _update_canvas(self):
        if hasattr(self.graph_line.figure, "canvas"):
            t = np.linspace(0, 10, 101)
            self.graph_line.set_data(t, np.sin(t + time.time()))
            self.graph_line.figure.canvas.draw()

    def createAnimationStart(self):
        t = np.linspace(0, 10, 101)
        (self.graph_line,) = self.graph_.axes.plot(
            t, np.sin(t + time.time()), color=rgb2hex(getTheme()["accent"])
        )

    def setupUi(self, MainWindow, MainWidget):
        self.logic = Logic()
        self.logic.reset()

        width = MainWindow.min_size.width()
        height = MainWindow.min_size.height()

        self.scrollCentral = QtWidgets.QScrollArea(MainWidget)
        self.scrollCentral.setFixedSize(QtCore.QSize(width, height - 63))

        self.solveOneVariableW = QtWidgets.QWidget()
        self.solveOneVariableW.setMinimumSize(QtCore.QSize(width - 90, height * 1.6))

        self.window = QtWidgets.QFrame(self.solveOneVariableW)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(0, 0, width, height * 2))
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

        self.x_left_widget = QtWidgets.QWidget(self.graph_control)
        self.x_left_layout = QtWidgets.QVBoxLayout()

        self.x_left_label = QtWidgets.QLabel(self.x_left_widget)
        self.x_left_label.setObjectName("x_left_label")

        self.x_left = QtWidgets.QDoubleSpinBox(self.x_left_widget)
        self.x_left.setEnabled(True)
        self.x_left.setMinimumSize(QtCore.QSize(95, 40))
        self.x_left.setStyleSheet("")
        self.x_left.setObjectName("x_left")

        self.x_left_layout.addWidget(self.x_left_label)
        self.x_left_layout.addWidget(self.x_left)
        self.x_left_widget.setLayout(self.x_left_layout)

        self.x_right_widget = QtWidgets.QWidget(self.graph_control)
        self.x_right_layout = QtWidgets.QVBoxLayout()

        self.x_right_label = QtWidgets.QLabel(self.x_right_widget)
        self.x_right_label.setObjectName("x_right_label")

        self.x_right = QtWidgets.QDoubleSpinBox(self.graph_control)
        self.x_right.setEnabled(True)
        self.x_right.setMinimumSize(QtCore.QSize(95, 40))
        self.x_right.setStyleSheet("")
        self.x_right.setObjectName("x_right")

        self.x_right_layout.addWidget(self.x_right_label)
        self.x_right_layout.addWidget(self.x_right)
        self.x_right_widget.setLayout(self.x_right_layout)

        self.y_up_widget = QtWidgets.QWidget(self.graph_control)
        self.y_up_layout = QtWidgets.QVBoxLayout()

        self.y_up_label = QtWidgets.QLabel(self.graph_control)
        self.y_up_label.setObjectName("y_up_label")

        self.y_up = QtWidgets.QDoubleSpinBox(self.graph_control)
        self.y_up.setEnabled(True)
        self.y_up.setMinimumSize(QtCore.QSize(95, 40))
        self.y_up.setStyleSheet("")
        self.y_up.setObjectName("y_up")

        self.y_up_layout.addWidget(self.y_up_label)
        self.y_up_layout.addWidget(self.y_up)
        self.y_up_widget.setLayout(self.y_up_layout)

        self.y_down_widget = QtWidgets.QWidget(self.graph_control)
        self.y_down_layout = QtWidgets.QVBoxLayout()

        self.y_down_label = QtWidgets.QLabel(self.graph_control)
        self.y_down_label.setObjectName("y_down_label")

        self.y_down = QtWidgets.QDoubleSpinBox(self.graph_control)
        self.y_down.setEnabled(True)
        self.y_down.setMinimumSize(QtCore.QSize(95, 40))
        self.y_down.setStyleSheet("")
        self.y_down.setObjectName("y_up")

        self.y_down_layout.addWidget(self.y_down_label)
        self.y_down_layout.addWidget(self.y_down)
        self.y_down_widget.setLayout(self.y_down_layout)

        self.graph_control_layout.addWidget(self.x_left_widget)
        self.graph_control_layout.addWidget(self.x_right_widget)
        self.graph_control_layout.addWidget(self.y_up_widget)
        self.graph_control_layout.addWidget(self.y_down_widget)

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
        font.setFamily(MainWindow.font_family)
        font.setPointSize(MainWindow.font_size)
        font.setWeight(MainWindow.font_weight)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
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
        self.tableWidget.setGeometry(QtCore.QRect(20, 526, 950, 500))
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")

        model = TableModel(DataFrame(self.logic.data))
        self.tableWidget.setModel(model)

        self.scrollCentral.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollCentral.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollCentral.setWidgetResizable(True)
        self.scrollCentral.setWidget(self.solveOneVariableW)

        self.valuesUI()
        self.actionsUI()

    def valuesUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.label_method.setText(_translate("MainWindow", "Select method"))
        self.label_fn.setText(_translate("MainWindow", "Write the function"))
        self.label_iteration.setText(_translate("MainWindow", "Iteration"))
        self.label_tolerance.setText(_translate("MainWindow", "Tolerance"))
        self.label_x0.setText(_translate("MainWindow", "X0"))
        self.label_x1.setText(_translate("MainWindow", "X1"))

        self.x_left_label.setText(_translate("MainWindow", "limit x left"))
        self.x_right_label.setText(_translate("MainWindow", "limit x right"))
        self.y_up_label.setText(_translate("MainWindow", "limit y up"))
        self.y_down_label.setText(_translate("MainWindow", "limit y down"))

        self.method_box.setCurrentIndex(-1)
        self.method_box.setItemText(0, _translate("MainWindow", "Bisection"))
        self.method_box.setItemText(1, _translate("MainWindow", "Newton"))
        self.method_box.setItemText(2, _translate("MainWindow", "Secant"))
        self.method_box.setItemText(3, _translate("MainWindow", "Point"))

        self.fn_box.setPlaceholderText(_translate("MainWindow", "x**2"))

        self.tolerance_box.setPlaceholderText(_translate("MainWindow", "1e-3"))

        self.x_left.setMaximum(0)
        self.x_left.setMinimum(-999999)
        self.x_left.setDecimals(3)

        self.x_right.setMaximum(999999)
        self.x_right.setMinimum(0)
        self.x_right.setDecimals(3)

        self.y_up.setMaximum(999999)
        self.y_up.setMinimum(0)
        self.y_up.setDecimals(3)

        self.y_down.setMaximum(0)
        self.y_down.setMinimum(-999999)
        self.y_down.setDecimals(3)

        self.x1_box.setMinimum(-1000)
        self.x1_box.setMaximum(1000)

        self.x0_box.setMinimum(-1000)
        self.x0_box.setMaximum(1000)

        self.iteration_box.setMinimum(1)
        self.iteration_box.setMaximum(9999)

        self.pushButton.setText(_translate("MainWindow", "Calculate"))

    def death(self):
        self.graph__timer.stop()
        self.graph_.axes.cla()

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
                dlg = ConfirmG(str_fn)
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
                    notify("Cancel!", "g1(x)")

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

            return notify(
                f"{self.logic.method_title} method: {p}",
                "Result",
            )
        except:
            return notify("Please fill all fields")

    def handleChangeMethod(self):
        model = self.tableWidget.model()
        if model:
            model.deleteLater()
            df = DataFrame(
                {
                    "Wait...": [1, 2, 3, 5, 8, 13, 21],
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

    def actionsUI(self):
        self.pushButton.clicked.connect(self.handleClickMethods)

        self.method_box.currentIndexChanged.connect(self.handleChangeMethod)

        self.fn_box.textChanged.connect(lambda v: self.subscription(v, 0))
        self.tolerance_box.textChanged.connect(lambda v: self.subscription(v, 1))
        self.x_left.textChanged.connect(lambda v: self.subscription(v, 2))
        self.x_right.textChanged.connect(lambda v: self.subscription(v, 3))
        self.y_up.textChanged.connect(lambda v: self.subscription(v, 4))
        self.y_down.textChanged.connect(lambda v: self.subscription(v, 5))
