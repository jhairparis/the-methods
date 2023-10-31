from sympy import symbols, Function, Eq, dsolve, init_printing, latex, sympify
from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QFont
from modules.mica.styleSheet import ApplyMenuBlur, setStyleSheet
from modules.MathToQPixmap import MathToQPixmap

init_printing(use_latex="mathjax")

# 3 * x * y(x).diff(x) - (x**2 - 9) * y(x) + 1 / x

def solve_equation(in_str):
    x = symbols("x")
    y = Function("y")

    eq_expr = sympify(in_str)
    the_problem = Eq(eq_expr, 0)

    res = dsolve(the_problem)
    return latex(res)
