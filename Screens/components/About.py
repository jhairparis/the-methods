from datetime import date
from PySide2.QtCore import Qt, QRect, QCoreApplication
from PySide2.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide2 import QtGui
from Screens.components.Dialog import Dialog
from Screens.components.MyLabel import MyLabel
from modules.mica.theme.getTheme import rgb2hex, getTheme


class AboutDialog(Dialog):
    def __init__(self, parent):
        super().__init__(parent, False)

        self.setWindowTitle("About")

        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.i = QWidget(self)

        self.layoutIcon = QHBoxLayout()

        pixmap = QtGui.QPixmap("icons/icon.png")
        self.icon = QLabel()
        self.icon.setPixmap(pixmap)
        self.icon.setScaledContents(True)
        self.icon.setFixedSize(150, 150)

        pixLicense = QtGui.QPixmap("icons/license.png")
        self.license = QLabel(self)
        self.license.setPixmap(pixLicense)
        self.license.setScaledContents(True)
        self.license.setFixedSize(88, 31)

        self.layoutIcon.addWidget(self.icon)

        self.i.setLayout(self.layoutIcon)

        self.title = MyLabel()
        self.title.setStyleSheet("font-size: 45px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)

        self.about = QLabel(self)
        self.version = QLabel(self)
        self.copy = QLabel(self)

        self.buildWith = QLabel(self)
        self.buildWith.setStyleSheet("font-size: 15px")

        self.thanks = MyLabel()
        self.thanks.setOpenExternalLinks(True)

        self.foundBug = QPushButton(self)
        self.foundBug.setEnabled(True)
        self.foundBug.setGeometry(QRect(60, 220, 191, 38))
        self.foundBug.setStyleSheet("")
        self.foundBug.setObjectName("hyperlinkButton")

        self.otherProjects = QPushButton(self)
        self.otherProjects.setEnabled(True)
        self.otherProjects.setGeometry(QRect(60, 220, 191, 38))
        self.otherProjects.setStyleSheet("")
        self.otherProjects.setObjectName("hyperlinkButton")

        self.split = QWidget(self)
        self.layoutSplit = QHBoxLayout()
        self.layoutSplit.addWidget(self.otherProjects)
        self.layoutSplit.addWidget(self.foundBug)
        self.layoutSplit.addWidget(self.license)
        self.split.setLayout(self.layoutSplit)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.i)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.about)
        self.layout.addWidget(self.buildWith)
        self.layout.addWidget(self.version)
        self.layout.addWidget(self.thanks)
        self.layout.addWidget(self.copy)
        self.layout.addStretch(1)
        self.layout.addWidget(self.split)

        self.setLayout(self.layout)

        self.valuesUI()

    def valuesUI(self):
        _translate = QCoreApplication.translate
        year = date.today().year
        palette = getTheme()["palette"]
        color = rgb2hex(palette[2])

        self.title.setText(_translate("MainWindow", "The methods"))
        self.about.setText(
            _translate(
                "MainWindow",
                "The methods are a project created for the subject of numerical analysis, based on books such as\nMatemáticas para Ingeniería. Métodos numéricos con Python (2017),\nAnálisis numérico / Richard L. Burden, J. Douglas Faires",
            )
        )
        self.buildWith.setText(
            _translate(
                "MainWindow",
                "Built with:\n  > Python 3.8.7\n  > Pandas\n  > PySide2\n  > Sympy\n  > Matplotlib",
            )
        )
        self.version.setText(_translate("MainWindow", "Version 1.0"))

        self.thanks.setText(
            _translate(
                "MainWindow",
                f"Thanks to project <a href='https://github.com/witalihirsch/QTWin11' style='color: {color}'>QTWin11</a> for UI base",
            )
        )
        self.copy.setText(
            _translate(
                "MainWindow",
                f"Copyright © {year} Jhair Paris. All rights reserved.",
            )
        )

        self.otherProjects.setText(_translate("MainWindow", "Other projects"))
        self.foundBug.setText(_translate("MainWindow", "Found a bug?"))

        # Interactive

        self.foundBug.clicked.connect(self.openFoundBug)
        self.otherProjects.clicked.connect(self.openOtherProjects)
        self.license.mousePressEvent = self.openLicense

    def openFoundBug(self):
        QtGui.QDesktopServices.openUrl(
            "https://github.com/jhairparis/the-methods/issues/new"
        )

    def openOtherProjects(self):
        QtGui.QDesktopServices.openUrl("https://jhairparis.com/projects")

    def openLicense(self, event):
        QtGui.QDesktopServices.openUrl(
            "https://github.com/jhairparis/the-methods/blob/main/LICENSE"
        )
