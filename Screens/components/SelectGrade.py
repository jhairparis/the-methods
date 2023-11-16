from PySide2.QtWidgets import (
    QWidget,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QSpinBox,
)
from Screens.components.Dialog import Dialog
from PySide2.QtCore import QSize
from modules.MathToQPixmap import MathToQPixmap


class SelectGrade(Dialog):
    grade = None

    def __init__(self):
        super().__init__(None, True)

        self.setWindowTitle("Write Grade")

        self.mainLayout = QVBoxLayout(self)
        self.oneLine = QWidget(self)
        self.oneLineLayout = QVBoxLayout()

        self.label_grade = QLabel()
        self.label_grade.setStyleSheet("")
        self.label_grade.setObjectName("label_grade")

        self.grade_box = QSpinBox()
        self.grade_box.setEnabled(True)
        self.grade_box.setMinimumSize(QSize(181, 40))
        self.grade_box.setObjectName("grade_box")
        self.grade_box.setStyleSheet("")

        self.oneLineLayout.addWidget(self.label_grade)
        self.oneLineLayout.addWidget(self.grade_box)

        self.oneLine.setLayout(self.oneLineLayout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setStyleSheet("width:100px")

        self.mainLayout.addWidget(self.oneLine)
        self.mainLayout.addWidget(self.buttonBox)

        self.setLayout(self.mainLayout)

        self.valuesUI()

    def accept_(self):
        self.grade = int(self.grade_box.text())
        return self.accept()

    def reject_(self):
        self.grade = None
        return self.reject()

    def valuesUI(self):
        self.label_grade.setText("Write taylor Grade:")

        self.buttonBox.accepted.connect(self.accept_)
        self.buttonBox.rejected.connect(self.reject_)
        return
