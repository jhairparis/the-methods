from PySide2 import QtCore, QtGui, QtWidgets
from sympy import sympify, latex
from pandas import DataFrame
from lib.Logic3 import Logic3
from numpy import linspace
from lib.equation.Euler import Euler
from lib.equation.Taylor import Taylor
from lib.equation.Runge import Runge
from modules.MplCanvas import MplCanvas
from modules.mica.theme.getTheme import getTheme, rgb2hex
from modules.Notification import notify
from Screens.components.Select import Select
from Screens.components.SelectGrade import SelectGrade

# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class Ui_DifferentialEquation(object):
    init_table = DataFrame(
        {
            "Wait...": [1, 2, 3, 5, 8, 13, 21],
        }
    )

    def setupUi(self, MainWindow, MainWidget):
        from modules.TableModel import TableModel

        self.logic = Logic3()

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

        self.DiffEquation = QtWidgets.QWidget()
        self.DiffEquation.setFixedSize(QtCore.QSize(self.width - 20, self.height * 1.5))

        self.window = QtWidgets.QFrame(self.DiffEquation)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height * 1.5))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        self.form = QtWidgets.QWidget(self.window)
        self.form.setGeometry(QtCore.QRect(20, 0, 400, 500))
        # self.form.setStyleSheet("background-color: #d35353")
        self.formLayout = QtWidgets.QVBoxLayout()

        self.select_text = QtWidgets.QLabel(self.form)
        self.formLayout.addWidget(self.select_text)

        self.select_method = Select(self.window)
        self.select_method.setMinimumSize(QtCore.QSize(181, 40))
        self.select_method.setEnabled(True)
        self.select_method.setToolTip("")
        self.select_method.setStatusTip("")
        self.select_method.setWhatsThis("")
        self.select_method.setAccessibleName("")
        self.select_method.setAccessibleDescription("")
        self.select_method.setStyleSheet("")
        self.select_method.setCurrentText("")
        self.select_method.setMinimumContentsLength(0)
        self.select_method.setObjectName("select_method")
        self.select_method.addItem("")
        self.select_method.addItem("")
        self.select_method.addItem("")
        self.formLayout.addWidget(self.select_method)

        self.fn_text = QtWidgets.QLabel(self.form)
        self.formLayout.addWidget(self.fn_text)

        self.fn_box = QtWidgets.QLineEdit(self.form)
        self.fn_box.setEnabled(True)
        self.fn_box.setMinimumSize(QtCore.QSize(181, 40))
        self.fn_box.setStyleSheet("")
        self.fn_box.setObjectName("fn_box")
        self.formLayout.addWidget(self.fn_box)

        self.initY_text = QtWidgets.QLabel(self.form)
        self.formLayout.addWidget(self.initY_text)

        self.initY_box = QtWidgets.QDoubleSpinBox(self.form)
        self.initY_box.setEnabled(True)
        self.initY_box.setMinimumSize(QtCore.QSize(181, 40))
        self.initY_box.setStyleSheet("")
        self.initY_box.setObjectName("initY_box")
        self.formLayout.addWidget(self.initY_box)

        self.initX_text = QtWidgets.QLabel(self.form)
        self.formLayout.addWidget(self.initX_text)

        self.initX_box = QtWidgets.QDoubleSpinBox(self.form)
        self.initX_box.setEnabled(True)
        self.initX_box.setMinimumSize(QtCore.QSize(181, 40))
        self.initX_box.setStyleSheet("")
        self.initX_box.setObjectName("initX_box")
        self.formLayout.addWidget(self.initX_box)

        self.steps_text = QtWidgets.QLabel(self.form)
        self.formLayout.addWidget(self.steps_text)

        self.steps_box = QtWidgets.QSpinBox(self.form)
        self.steps_box.setEnabled(True)
        self.steps_box.setMinimumSize(QtCore.QSize(181, 40))
        self.steps_box.setStyleSheet("")
        self.steps_box.setObjectName("steps_box")
        self.formLayout.addWidget(self.steps_box)

        self.maxX_text = QtWidgets.QLabel(self.form)
        self.formLayout.addWidget(self.maxX_text)

        self.maxX_box = QtWidgets.QDoubleSpinBox(self.form)
        self.maxX_box.setEnabled(True)
        self.maxX_box.setMinimumSize(QtCore.QSize(181, 40))
        self.maxX_box.setStyleSheet("")
        self.maxX_box.setObjectName("maxX_box")
        self.formLayout.addWidget(self.maxX_box)

        self.ok = QtWidgets.QPushButton(self.form)
        self.ok.setEnabled(True)
        self.ok.setMaximumSize(QtCore.QSize(150, 40))
        self.ok.setFont(font)
        self.ok.setStyleSheet("")
        self.ok.setObjectName("ok")
        self.formLayout.addWidget(self.ok)

        self.form.setLayout(self.formLayout)

        self.graph = QtWidgets.QWidget(self.window)
        self.graph.setGeometry(QtCore.QRect(440, 0, 520, 520))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_ = MplCanvas()

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_)
        # self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph.setLayout(self.graph_layout)

        self.tableWidget = QtWidgets.QTableView(self.window)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 530, self.width - 40, 400))
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setStyleSheet("background-color: #53d35e;")

        model = TableModel(self.init_table)
        self.tableWidget.setModel(model)

        self.scrollCentral.setWidget(self.DiffEquation)

        self.valuesUI()
        self.actionsUI(MainWindow)

    def valuesUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.select_text.setText(_translate("MainWindow", "Select method:"))
        self.select_method.setCurrentIndex(-1)
        self.select_method.setItemText(0, _translate("MainWindow", "Euler"))
        self.select_method.setItemText(1, _translate("MainWindow", "Taylor"))
        self.select_method.setItemText(2, _translate("MainWindow", "Runge"))

        self.fn_text.setText(_translate("MainWindow", "Diff equation: "))
        self.fn_box.setPlaceholderText(_translate("MainWindow", "dy/dx = x + y(x)"))

        self.initX_text.setText(_translate("MainWindow", "Initial X: "))
        self.initX_box.setMinimum(-9999999)
        self.initX_box.setMaximum(9999999)

        self.initY_text.setText(_translate("MainWindow", "Initial Y: "))
        self.initY_box.setMinimum(-9999999)
        self.initY_box.setMaximum(9999999)

        self.steps_text.setText(_translate("MainWindow", "Steps: "))
        self.steps_box.setMinimum(0)
        self.steps_box.setMaximum(9999999)

        self.maxX_text.setText(_translate("MainWindow", "Max value X: "))
        self.maxX_box.setMinimum(-9999999)
        self.maxX_box.setMaximum(9999999)

        self.ok.setText(_translate("MainWindow", "OK"))

        return

    def updateTitle(self, rawText):
        try:
            text = latex(sympify("Eq(" + rawText.replace("=", ",") + ")"))
            self.graph_.axes.set_title("$" + text + "$", fontsize=15)
            self.graph_.draw()
        except:
            pass

    def updateGraph(self, res, initX, finalX):
        self.graph_.axes.set_title("$" + res["solution_latex"] + "$", fontsize=15)

        self.graph_.axes.scatter(
            self.logic.data_xi, self.logic.data_yi, label="Approx", color="yellow"
        )

        x_vals = linspace(initX, finalX, 400)
        y_vals = [res["solution"](x) for x in x_vals]

        theme = getTheme()

        self.graph_.axes.plot(x_vals, y_vals, color=rgb2hex(theme["palette"][3]))
        self.graph_.draw()

    def updateTable(self):
        from modules.TableModel import TableModel

        newModel = TableModel(DataFrame(self.logic.data))
        self.tableWidget.setModel(newModel)
        pass

    def solve(self):
        if (
            not self.fn_box.text().strip()
            and not self.initX_box.text().strip()
            and not self.initY_box.text().strip()
            and not self.steps_box.text().strip()
            and not self.maxX_box.text().strip()
        ):
            notify("Please fill all the fields")
            return

        self.graph_.axes.clear()
        self.graph_.draw()

        initX = float(self.initX_box.text())
        finalX = float(self.maxX_box.text())
        selected_method = self.select_method.currentIndex()

        try:
            if selected_method == 0:
                res = Euler(
                    self.logic,
                    self.fn_box.text(),
                    initX,
                    float(self.initY_box.text()),
                    int(self.steps_box.text()),
                    finalX,
                )
            elif selected_method == 1:
                dlg = SelectGrade()
                dlg.exec()

                if not dlg.grade:
                    notify("Please select a grade")
                    return

                res = Taylor(
                    self.logic,
                    self.fn_box.text(),
                    initX,
                    float(self.initY_box.text()),
                    dlg.grade,
                    int(self.steps_box.text()),
                    finalX,
                )
            elif selected_method == 2:
                res = Runge(
                    self.logic,
                    self.fn_box.text(),
                    initX,
                    float(self.initY_box.text()),
                    int(self.steps_box.text()),
                    finalX,
                )

            if res:
                self.updateTable()
                self.updateGraph(res, initX, finalX)
        except:
            notify("Please fill all the fields")
            return

    def actionsUI(self, MainWindow):
        self.ok.clicked.connect(self.solve)
        self.fn_box.textChanged.connect(self.updateTitle)
        return
