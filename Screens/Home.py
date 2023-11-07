from PySide2 import QtCore, QtGui, QtWidgets
from modules.MplCanvas import MplCanvas
import matplotlib.animation as animation
from matplotlib import get_data_path, font_manager
from pathlib import Path


class Ui_Home(object):
    def setupUi(self, MainWindow, MainWidget):
        MainWindow.menuBar.setVisible(False)
        self.width = MainWindow.min_size.width()
        self.height = MainWindow.min_size.height()

        self.Home = QtWidgets.QWidget(MainWidget)
        self.Home.setFixedSize(QtCore.QSize(self.width, self.height))

        self.Logo = QtWidgets.QLabel(self.Home)
        self.Logo.setGeometry(QtCore.QRect((self.width - 250) / 2, 0, 250, 250))

        self.animationText = QtWidgets.QWidget(self.Home)
        self.animationText.setGeometry(QtCore.QRect(0, -50, self.width, self.height))

        self.animationText_ = MplCanvas()

        fpath = Path(get_data_path(), "fonts/ttf/DejaVuSans-Bold.ttf")

        text = "The Methods"

        txt = self.animationText_.axes.text(
            0.5, 0.5, "", ha="center", va="center", color="#a32146"
        )
        txt.set_fontproperties(font_manager.FontProperties(fname=fpath, size=30))

        self.animationText_.axes.axis("off")

        def update(i):
            txt.set_text(text[: i + 1])
            return (txt,)

        self.anim = animation.FuncAnimation(
            self.animationText_.fig,
            update,
            frames=len(text),
            interval=100,
            repeat=False,
        )

        self.animationText_layout = QtWidgets.QVBoxLayout()
        self.animationText_layout.addWidget(self.animationText_)
        # self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.animationText.setLayout(self.animationText_layout)

        self.buttons = QtWidgets.QWidget(self.Home)
        self.buttons.setFixedSize(QtCore.QSize(608, 200))
        self.buttons.setGeometry(
            QtCore.QRect((self.width - 600) / 2, (self.height - 50) / 2, 608, 200)
        )
        # self.buttons.setStyleSheet("background-color: rgba(124, 202, 134, 0.5);")

        self.layout = QtWidgets.QHBoxLayout(self.Home)
        self.layout.setSpacing(50)

        self.group1 = QtWidgets.QWidget(self.Home)
        self.group1Layout = QtWidgets.QVBoxLayout()

        self.Topic1Label = QtWidgets.QLabel(self.group1)

        self.Topic1 = QtWidgets.QPushButton(self.group1)
        self.Topic1.setEnabled(True)
        self.Topic1.setStyleSheet("max-height: 600px")

        self.group1Layout.addWidget(self.Topic1)
        self.group1Layout.addWidget(self.Topic1Label)
        self.group1.setLayout(self.group1Layout)

        self.group2 = QtWidgets.QWidget(self.Home)
        self.group2Layout = QtWidgets.QVBoxLayout()

        self.Topic2Label = QtWidgets.QLabel(self.group2)

        self.Topic2 = QtWidgets.QPushButton(self.group2)
        self.Topic2.setEnabled(True)
        self.Topic2.setStyleSheet("max-height: 600px")

        self.group2Layout.addWidget(self.Topic2)
        self.group2Layout.addWidget(self.Topic2Label)
        self.group2.setLayout(self.group2Layout)

        self.group3 = QtWidgets.QWidget(self.Home)
        self.group3Layout = QtWidgets.QVBoxLayout()

        self.Topic3Label = QtWidgets.QLabel(self.group3)

        self.Topic3 = QtWidgets.QPushButton(self.Home)
        self.Topic3.setEnabled(True)
        self.Topic3.setStyleSheet("max-height: 600px")

        self.group3Layout.addWidget(self.Topic3)
        self.group3Layout.addWidget(self.Topic3Label)
        self.group3.setLayout(self.group3Layout)

        self.layout.addWidget(self.group1)
        self.layout.addWidget(self.group2)
        self.layout.addWidget(self.group3)

        self.buttons.setLayout(self.layout)

        self.by = QtWidgets.QLabel(self.Home)
        self.by.setGeometry(QtCore.QRect(self.width - 120, self.height - 50, 100, 50))

        self.valuesUI()
        self.actionsUI(MainWindow)

    def valuesUI(self):
        iconSize = QtCore.QSize(120, 120)
        self.Logo.setPixmap(QtGui.QPixmap(":/icons/icon.ico"))

        self.Topic1Label.setText("Solve one variable")
        self.Topic2Label.setText("Interpolation")
        self.Topic3Label.setText("Differential equations")

        self.Topic1.setIcon(QtGui.QIcon(":/icons/home/SolveOneVariable.png"))
        self.Topic1.setToolTip("Solve one variable")
        self.Topic1.setIconSize(iconSize)

        self.Topic2.setIcon(QtGui.QIcon(":/icons/home/Interpolation.png"))
        self.Topic2.setToolTip("Interpolation")
        self.Topic2.setIconSize(iconSize)

        self.Topic3.setIcon(QtGui.QIcon(":/icons/home/DifferentialEquations.png"))
        self.Topic3.setToolTip("Differential equations")
        self.Topic3.setIconSize(iconSize)

        self.by.setText("by Jhair Paris")
        return

    def actionsUI(self, MainWindow):
        self.Topic1.clicked.connect(MainWindow.setWindowSolveOneVariable)
        self.Topic2.clicked.connect(MainWindow.setWindowInterpolation)
        self.Topic3.clicked.connect(MainWindow.setWindowDifferentialEquations)

        return
