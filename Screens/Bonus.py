from PySide2 import QtCore, QtGui, QtWidgets
from sympy import sympify
from numpy import linspace
from matplotlib.animation import FuncAnimation
from modules.MplCanvas import MplCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class Ui_Video(object):
    def setupUi(self, MainWindow, MainWidget):
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

        self.window = QtWidgets.QFrame(MainWidget)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        self.fn_input = QtWidgets.QLineEdit(self.window)
        self.fn_input.setGeometry(QtCore.QRect(20, 0, 150, 40))
        self.animateButton = QtWidgets.QPushButton(self.window)
        self.animateButton.setGeometry(QtCore.QRect(190, 0, 150, 40))

        self.playButton = QtWidgets.QPushButton(self.window)
        self.playButton.setGeometry(QtCore.QRect(360, 0, 150, 40))
        self.stopButton = QtWidgets.QPushButton(self.window)
        self.stopButton.setGeometry(QtCore.QRect(530, 0, 150, 40))
        self.resetButton = QtWidgets.QPushButton(self.window)
        self.resetButton.setGeometry(QtCore.QRect(700, 0, 150, 40))

        self.graph = QtWidgets.QWidget(self.window)
        self.graph.setGeometry(QtCore.QRect(20, 60, 622, 520))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_ = MplCanvas()
        (self.graph_line,) = self.graph_.axes.plot([0], [0], color="#FFA500")

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_)
        self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph.setLayout(self.graph_layout)

        self.valuesUI()
        self.actions(MainWindow)

    def animate(self, MainWindow):
        st = self.fn_input.text()

        if st.strip() == "" or (hasattr(self, "anim") and self.anim != None):
            return

        points = MainWindow.ui2.logic.base
        self.graph_.axes.scatter(points["x"], points["f(x)"], color="red")

        def fn(x):
            return sympify(st).subs("x", x).evalf()

        fig = self.graph_line.figure
        ax = self.graph_line.axes
        (ln,) = ax.plot([], [])
        xData, yData = [], []

        def init():
            ax.set_xlim(points["x"][0] - 0.5, points["x"][len(points["x"]) - 1] + 0.5)
            ax.set_ylim(
                points["f(x)"][len(points["f(x)"]) - 1] - 2,
                points["f(x)"][0] + 1,
            )
            return (ln,)

        def update(frame):
            xData.append(frame)
            yData.append(fn(frame))
            ln.set_data(xData, yData)
            return (ln,)

        self.anim = FuncAnimation(
            fig,
            update,
            frames=linspace(points["x"][0], points["x"][len(points["x"]) - 1], 100),
            init_func=init,
            blit=True,
            interval=250,
        )

        # anim.save("lines.gif")

    def valuesUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.animateButton.setText(_translate("MainWindow", "Animate!"))

        self.playButton.setText(_translate("MainWindow", "play"))
        self.stopButton.setText(_translate("MainWindow", "stop"))
        self.resetButton.setText(_translate("MainWindow", "reset"))

    def reset(self):
        # valid if self have .anim attribute
        if hasattr(self, "anim"):
            self.anim.event_source.stop()
            self.graph_.axes.clear()
            (self.graph_line,) = self.graph_.axes.plot([0], [0], color="#FFA500")
            self.anim = None
            self.graph_.draw()

    def play(self):
        if hasattr(self, "anim") and self.anim != None:
            self.anim.event_source.start()

    def stop(self):
        if hasattr(self, "anim") and self.anim != None:
            self.anim.event_source.stop()

    def actions(self, MainWindow):
        self.animateButton.clicked.connect(lambda: self.animate(MainWindow))

        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.stop)
        self.resetButton.clicked.connect(self.reset)
