from sympy import symbols, Function, Eq, dsolve, simplify, sympify, latex
from lib.precision import reduceThePrecision


def Euler(logic, eqMain, initX, initY, steps, finalValue):
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

    temp = eqMain.split("=")
    f = simplify(temp[1].replace("y(x)", "y"))

    eqMain = Eq(sympify(temp[0]), sympify(temp[1]))
    eqMainSolve = dsolve(eqMain, y(x), ics={y(initX): initY})

    xi = initX
    findY = initY
    h = (finalValue - initX) / steps

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
