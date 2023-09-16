import sys
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
import numpy as np
from modules.mica.styleSheet import ApplyMenuBlur, setMicaWindow
import darkdetect
import matplotlib
from lib.methods.newton import derivative
from modules.Dialog import CustomDialog
from plyer import notification
from sympy import latex, sympify
from modules.latexText import mathTex_to_QPixmap

matplotlib.use("Qt5Agg")

if darkdetect.isDark() == True:
    from dark import *
else:
    from light import *


class TheWindow(QMainWindow):
    def create_latex(self):
        ltx = latex(sympify(self.ui.fn_box.value))
        self.ui.label_fn.setPixmap(mathTex_to_QPixmap(f"${ltx}$", 11))
        return

    def create_main_graph(self):
        self.ui.graph_.axes.cla()

        if (
            hasattr(self.ui.x_left, "value")
            and hasattr(self.ui.x_right, "value")
            and hasattr(self.ui.y_up, "value")
            and hasattr(self.ui.y_down, "value")
            and hasattr(self.ui.fn_box, "value")
        ):
            x_left = float(self.ui.x_left.value)
            x_right = float(self.ui.x_right.value)
            y_up = float(self.ui.y_up.value)
            y_down = float(self.ui.y_down.value)

            infinite = np.linspace(x_left, x_right, 101)

            self.ui.logic.fn = self.ui.logic.gen_fn(self.ui.fn_box.value)

            self.create_latex()

            (self.graph_line,) = self.ui.graph_.axes.plot(
                infinite,
                [self.ui.logic.fn(i) for i in infinite],
                color="gray",
                linestyle="--",
                zorder=1,
            )

            self.graph_line.axes.set_xlim(xmin=x_left, xmax=x_right)
            self.graph_line.axes.set_ylim(ymax=y_up, ymin=y_down)

            self.ui.graph_.draw()

    def subscription(self, v, who):
        self.ui.graph__timer.stop()
        if who == 0:
            self.ui.graph_.axes.cla()

            if len(v) >= 1:
                self.ui.fn_box.value = v
                self.create_main_graph()
            else:
                t = np.linspace(0, 10, 101)
                (self.ui.graph_line,) = self.ui.graph_.axes.plot(
                    t, np.sin(t + time.time())
                )
                self.ui.graph__timer.start()
                self.ui.graph_.draw()

        if who == 1:
            self.ui.tolerance_box.value = v
        if who == 2:
            self.ui.x_left.value = v
            self.create_main_graph()
        if who == 3:
            self.ui.x_right.value = v
            self.create_main_graph()
        if who == 4:
            self.ui.y_up.value = v
            self.create_main_graph()
        if who == 5:
            self.ui.y_down.value = v
            self.create_main_graph()

    def add_marks(self, method, df, fn):
        ps = ["Pn", "p", "Xn", "x"]
        for i in df.index:
            self.ui.graph_.axes.scatter(
                float(df[ps[method]].get(i)),
                fn(float(df[ps[method]].get(i))),
                label=f"{i} ite",
                marker="*",
                alpha=0.8,
                s=50,
                zorder=3,
            )
        return

    def click(self):
        try:
            self.create_main_graph()
            method = self.ui.method_box.currentIndex()
            x0 = self.ui.x0_box.value()
            x1 = self.ui.x1_box.value()
            tol = float(self.ui.tolerance_box.value)
            steps = self.ui.iteration_box.value()
            str_fn = self.ui.fn_box.value
            fn = self.ui.logic.gen_fn(str_fn)

            m = self.ui.logic.get_method(method)

            deri = derivative(str_fn)

            if method == 1:
                v = m(
                    logic=self.ui.logic,
                    fun=fn,
                    deri=deri,
                    x_a=x0,
                    tol=tol,
                    steps=steps,
                    x_b=x1,
                )

                self.ui.graph_.axes.scatter(
                    x0, fn(x0), label="X0", color="violet", zorder=3
                )
            elif method == 3:
                dlg = CustomDialog(str_fn)
                if dlg.exec():
                    v = m(
                        logic=self.ui.logic,
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
                v = m(
                    logic=self.ui.logic,
                    fun=fn,
                    x_a=x0,
                    x_b=x1,
                    tol=tol,
                    steps=steps,
                )

            df = self.ui.logic.show_table(True)

            model = TableModel(df)
            self.ui.tableWidget.setModel(model)

            # render thing in graph

            if method == 0:
                var = np.linspace(x0, x1, 101)
                self.ui.graph_.axes.plot(
                    var, [fn(i) for i in var], label="Range", color="red", zorder=2
                )

            self.ui.graph_.axes.scatter(v, 0, label="Root", color="yellow", zorder=3)

            self.add_marks(method, df, fn)

            self.ui.graph_.draw()

            return v
        except:
            notification.notify(
                title="Error",
                message="Please fill all fields",
                app_icon=None,
                timeout=10,
            )
            return None

    def change_method(self):
        model = self.ui.tableWidget.model()
        if model:
            model.deleteLater()
            df = DataFrame(
                {
                    "Hey": [],
                    "Hey2": [],
                    "Hey3": [],
                }
            )
            model = TableModel(df)
            self.ui.tableWidget.setModel(model)

        if len(self.ui.logic.method_title) >= 1:
            self.create_main_graph()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("icons/icon.ico"))
        setMicaWindow(self)

        ApplyMenuBlur(self.ui.menuFile.winId().__int__())
        ApplyMenuBlur(self.ui.actionNew.winId().__int__())
        ApplyMenuBlur(self.ui.menuEdit.winId().__int__())
        ApplyMenuBlur(self.ui.menuHelp.winId().__int__())

        self.setAttribute(Qt.WA_TranslucentBackground)
        if QtWin.isCompositionEnabled():
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        # CUSTOM LIST IN COMBOBOX
        self.ui.listview = QtWidgets.QListView()
        self.ui.method_box.setView(self.ui.listview)

        self.ui.method_box.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.ui.method_box.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.ui.method_box.setCurrentIndex(-1)
        ApplyMenuBlur(self.ui.method_box.view().window().winId().__int__())

        # CLICK
        self.ui.pushButton.clicked.connect(lambda: print("method res: ", self.click()))

        self.ui.method_box.currentIndexChanged.connect(self.change_method)

        self.ui.fn_box.textChanged.connect(lambda v: self.subscription(v, 0))
        self.ui.tolerance_box.textChanged.connect(lambda v: self.subscription(v, 1))
        self.ui.x_left.textChanged.connect(lambda v: self.subscription(v, 2))
        self.ui.x_right.textChanged.connect(lambda v: self.subscription(v, 3))
        self.ui.y_up.textChanged.connect(lambda v: self.subscription(v, 4))
        self.ui.y_down.textChanged.connect(lambda v: self.subscription(v, 5))

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    centralwidget = TheWindow()
    sys.exit(app.exec_())
