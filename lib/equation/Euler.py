from sympy import symbols, Function, simplify, latex
from lib.precision import reduceThePrecision
from lib.equation.solveDiff import solveDiff


def Euler(logic, eqMain, initX, initY, steps, maxValue):
    logic.reset()
    logic.method_title = "Euler"

    logic.data = {
        "xi": logic.data_xi,
        "yi": logic.data_yi,
        "yi Real": logic.data_yir,
        "Relative error": logic.data_err,
    }

    x = symbols("x")
    y = Function("y")

    f = simplify(eqMain.split("=")[1].replace("y(x)", "y"))

    eqMainSolve = solveDiff(eqMain, y, x, initX, initY)

    xi = initX
    findY = initY
    h = (maxValue - initX) / steps

    for i in range(steps + 1):
        logic.data_xi.append(xi)
        logic.data_yi.append(findY)

        yReal = float(eqMainSolve.rhs.subs("x", xi).evalf())

        logic.data_err.append(abs((yReal - findY) / yReal))
        logic.data_yir.append(yReal)

        findY = float(findY + h * f.subs({"x": xi, "y": findY}).evalf())

        xi += h

    return {
        "solution": lambda x: eqMainSolve.rhs.subs("x", x).evalf(),
        "solution_latex": reduceThePrecision(latex(eqMainSolve), 4),
    }
