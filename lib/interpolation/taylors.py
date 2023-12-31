from sympy import factorial, latex, sympify
from lib.precision import reduceThePrecision


def taylor(f_str: str, k: int, x0: float):
    f = sympify(f_str)
    pol = ""

    for i in range(k):
        num = latex(f.subs("x", x0).evalf())
        pol += f"({num}*(x-{x0})**{i})/{factorial(i)}+"
        f = f.diff()

    pol = pol[:-1]

    return reduceThePrecision(latex(sympify(pol)), 4)
