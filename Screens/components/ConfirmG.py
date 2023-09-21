import re
from PySide2.QtWidgets import (
    QWidget,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
)
from Screens.components.Dialog import Dialog
from PySide2.QtCore import QSize
from sympy import sympify, solve, latex
from modules.MathToQPixmap import MathToQPixmap


class ConfirmG(Dialog):
    eq = None
    ez = None
    sol = None
    sol_fn = None

    def replaceX(self, text):
        try:
            result = re.sub(r"(?<!exp)\b(x)\b", "y", text, 1)
            return result
        except:
            return text

    def checkCustomClicked(self):
        self.checkCustom.setChecked(True)
        self.checkAuto.setChecked(False)

    def checkAutoClicked(self):
        self.checkCustom.setChecked(False)
        self.checkAuto.setChecked(True)

    def setSolFn(self, fn):
        def f(x=1):
            return fn.subs("x", x).evalf()

        self.sol_fn = f

    def accept_(self):
        if self.checkAuto.isChecked():
            self.setSolFn(self.sol[0])
        elif self.checkCustom.isChecked():
            self.setSolFn(sympify(self.fieldCustomSolved.text()))

        self.accept()

    def __init__(self, fun):
        super().__init__(None, True)

        self.setWindowTitle("Confirm g1(x)")

        self.eq = sympify(fun)
        self.ez = sympify(self.replaceX(fun))
        self.sol = solve(self.ez, "y")

        self.setSolFn(self.sol[0])

        self.mainLayout = QVBoxLayout(self)

        self.labelFun = QLabel(self)
        self.labelFun.setStyleSheet("")
        self.labelFun.setObjectName("labelFun")

        self.labelFunX = QLabel(self)
        self.labelFunX.setStyleSheet("")
        self.labelFunX.setObjectName("labelFunX")

        self.fieldCustomSolved = QLineEdit(self)
        self.fieldCustomSolved.setEnabled(True)
        self.fieldCustomSolved.setMinimumSize(QSize(181, 40))
        self.fieldCustomSolved.setStyleSheet("")
        self.fieldCustomSolved.setObjectName("fieldCustomSolved")

        self.help = QLabel(self)
        self.help.setObjectName("help")

        self.labelFunSolved = QLabel(self)
        self.labelFunSolved.setObjectName("labelFunSolved")

        self.checkCustom = QCheckBox(self)
        self.checkCustom.setStyleSheet("")
        self.checkCustom.setObjectName("checkCustom")

        self.checkAuto = QCheckBox(self)
        self.checkAuto.setStyleSheet("")
        self.checkAuto.setObjectName("checkAuto")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setStyleSheet("width:100px")

        self.mainLayout.addWidget(self.labelFun)
        self.mainLayout.addWidget(self.labelFunX)
        self.mainLayout.addWidget(self.help)

        self.oneLine = QWidget()
        self.layoutLine = QHBoxLayout()
        self.layoutLine.addWidget(self.checkCustom)
        self.layoutLine.addWidget(self.fieldCustomSolved)
        self.oneLine.setLayout(self.layoutLine)

        self.twoLine = QWidget()
        self.layoutLine2 = QHBoxLayout()
        self.layoutLine2.addWidget(self.checkAuto)
        self.layoutLine2.addWidget(self.labelFunSolved)
        self.twoLine.setLayout(self.layoutLine2)

        self.mainLayout.addWidget(self.oneLine)
        self.mainLayout.addWidget(self.twoLine)
        self.mainLayout.addWidget(self.buttonBox)

        self.setLayout(self.mainLayout)

        self.valuesUI(fun)

    def valuesUI(self, fun):
        self.help.setText("Select the function g(x): ")

        eqLatex = f"$f(x)={latex(self.eq)}$"
        self.labelFun.setPixmap(MathToQPixmap(eqLatex, 10))

        ezLatex = f"$0={latex(self.ez)}$"
        self.labelFunX.setPixmap(MathToQPixmap(ezLatex, 10))

        self.fieldCustomSolved.setText(fun)

        solLatex = f"${latex(self.sol[0])}$"
        self.labelFunSolved.setPixmap(MathToQPixmap(solLatex, 10))

        # Interactive
        self.checkCustom.clicked.connect(self.checkCustomClicked)
        self.checkAuto.clicked.connect(self.checkAutoClicked)

        self.checkAuto.setChecked(True)
        self.checkCustom.setChecked(False)

        self.buttonBox.accepted.connect(self.accept_)
        self.buttonBox.rejected.connect(self.reject)
