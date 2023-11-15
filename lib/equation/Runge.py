from sympy import symbols, Function, simplify, latex
from lib.equation.solveDiff import solveDiff
from lib.precision import reduceThePrecision


def Runge(logic, eqMain, initX, initY, steps, maxValue):
    logic.reset()
    logic.method_title = "Euler"

    logic.data = {
        "ti": logic.data_xi,
        "Exact": logic.data_yir,
        "Runge-kuttar": logic.data_yi,
        "Relative error": logic.data_err,
    }

    X = symbols("x")
    Y = Function("y")

    eq = eqMain.split("=")[1].replace("y(x)", "y")
    eq = simplify(eq)

    f = lambda x, y: float(eq.subs(X, x).subs("y", y))

    eqMainSolve = solveDiff(eqMain, Y, X, initX, initY)

    xi = initX
    yi = initY
    h = (maxValue - initX) / steps

    for i in range(steps + 1):
        logic.data_xi.append(xi)
        logic.data_yi.append(yi)

        yReal = float(eqMainSolve.rhs.subs("x", xi).evalf())
        logic.data_yir.append(yReal)

        logic.data_err.append(abs((yReal - yi) / yReal))

        k1 = h * f(xi, yi)
        k2 = h * f(xi + ((1 / 2) * h), yi + ((1 / 2) * k1))
        k3 = h * f(xi + ((1 / 2) * h), yi + ((1 / 2) * k2))
        k4 = h * f(xi + h, yi + k3)

        yi += (1 / 6) * (k1 + (2 * k2) + (2 * k3) + k4)
        xi += h

    return {
        "solution": lambda x: eqMainSolve.rhs.subs("x", x).evalf(),
        "solution_latex": reduceThePrecision(latex(eqMainSolve)),
    }
