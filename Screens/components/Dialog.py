import re
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QWidget
from sympy import sympify, solve, latex
from modules.MathToQPixmap import MathToQPixmap
from modules.mica.styleSheet import setMicaWindow, setStyleSheet


class CustomDialog(QDialog):
    eq = None
    ez = None
    sol = None
    sol_fn = None

    def replace_x(self, text):
        try:
            result = re.sub(r"(?<!exp)\b(x)\b", "y", text, 1)
            return result
        except:
            return text

    def __init__(self, fun):
        super().__init__()

        self.setWindowTitle("Confirm g1(x)")

        setMicaWindow(self)
        setStyleSheet(self)

        self.eq = sympify(fun)
        self.ez = sympify(self.replace_x(fun))
        self.sol = solve(self.ez, "y")

        def f(x=1):
            return self.sol[0].subs("x", x).evalf()

        self.sol_fn = f

        message = QLabel("f(x):")

        self.label_fun = QLabel()
        eqLatex = f"${latex(self.eq)}$"
        self.label_fun.setPixmap(MathToQPixmap(eqLatex, 10))

        message2 = QLabel("x=")
        self.label_fun_x = QLabel()
        ezLatex = f"${latex(self.ez)}$"
        self.label_fun_x.setPixmap(MathToQPixmap(ezLatex, 10))

        message3 = QLabel("solved for x=")
        self.label_fun_solved = QLabel()
        solLatex = f"${latex(self.sol[0])}$"
        self.label_fun_solved.setPixmap(MathToQPixmap(solLatex, 10))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)
        self.layout.addWidget(self.label_fun)
        self.layout.addWidget(message2)
        self.layout.addWidget(self.label_fun_x)
        self.layout.addWidget(message3)
        self.layout.addWidget(self.label_fun_solved)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)