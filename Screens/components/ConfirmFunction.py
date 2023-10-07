from PySide2.QtWidgets import (
    QWidget,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
)
from Screens.components.Dialog import Dialog
from PySide2.QtCore import QSize
from modules.MathToQPixmap import MathToQPixmap


class ConfirmFunction(Dialog):
    fn = None
    x_0 = None
    n = None

    def __init__(self):
        super().__init__(None, True)

        self.setWindowTitle("Write f(x)")

        self.mainLayout = QVBoxLayout(self)

        self.labelFun = QLabel(self)
        self.labelFun.setStyleSheet("")
        self.labelFun.setObjectName("labelFun")

        self.fieldFun = QLineEdit(self)
        self.fieldFun.setEnabled(True)
        self.fieldFun.setMinimumSize(QSize(181, 40))
        self.fieldFun.setStyleSheet("")
        self.fieldFun.setObjectName("fieldFun")

        self.oneLine = QWidget()

        self.layoutLine = QHBoxLayout()
        self.layoutLine.addWidget(self.labelFun)
        self.layoutLine.addWidget(self.fieldFun)

        self.oneLine.setLayout(self.layoutLine)

        self.labelX0 = QLabel(self)
        self.labelX0.setObjectName("labelX0")

        self.fieldX0 = QLineEdit(self)
        self.fieldX0.setEnabled(True)
        self.fieldX0.setMinimumSize(QSize(181, 40))
        self.fieldX0.setStyleSheet("")
        self.fieldX0.setObjectName("fieldX0")

        self.twoLine = QWidget()

        self.layoutLine2 = QHBoxLayout()
        self.layoutLine2.addWidget(self.labelX0)
        self.layoutLine2.addWidget(self.fieldX0)

        self.twoLine.setLayout(self.layoutLine2)

        self.labelN = QLabel(self)
        self.labelN.setObjectName("labelN")

        self.fieldN = QLineEdit(self)
        self.fieldN.setEnabled(True)
        self.fieldN.setMinimumSize(QSize(181, 40))
        self.fieldN.setStyleSheet("")
        self.fieldN.setObjectName("fieldN")

        self.threeLine = QWidget()

        self.layoutLine3 = QHBoxLayout()
        self.layoutLine3.addWidget(self.labelN)
        self.layoutLine3.addWidget(self.fieldN)

        self.threeLine.setLayout(self.layoutLine3)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setStyleSheet("width:100px")

        self.mainLayout.addWidget(self.oneLine)
        self.mainLayout.addWidget(self.twoLine)
        self.mainLayout.addWidget(self.threeLine)
        self.mainLayout.addWidget(self.buttonBox)

        self.setLayout(self.mainLayout)

        self.valuesUI()

    def accept_(self):
        self.fn = self.fieldFun.text()
        self.x_0 = self.fieldX0.text()
        self.n = self.fieldN.text()
        return self.accept()

    def valuesUI(self):
        self.labelFun.setText("Write f(x):")
        self.labelX0.setText("Write x0:")
        self.labelN.setText("Write k:")

        self.buttonBox.accepted.connect(self.accept_)
        self.buttonBox.rejected.connect(self.reject)
