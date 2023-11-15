from sympy import Symbol, Function, sympify, factorial, latex
from lib.precision import reduceThePrecision
from lib.equation.solveDiff import solveDiff


def Taylor(logic, eqMain, initX, initY, taylorGrade, steps, maxValue):
    logic.reset()
    logic.method_title = "Euler"

    logic.data = {
        "xi": logic.data_xi,
        "yi": logic.data_yi,
        "yi Real": logic.data_yir,
        "Relative error": logic.data_err,
    }

    X = Symbol("x")
    h_ = Symbol("h")
    Y = Function("y")

    f = sympify(eqMain.split("=")[1])
    eqMainSolve = solveDiff(eqMain, Y, X, initX, initY)

    gradesDiff = {
        0: f,
    }

    for i in range(1, taylorGrade + 1):
        gradesDiff[i] = gradesDiff[i - 1].diff("x").replace(Y(X).diff(X), f)

    # print("diffs:")
    # for i in gradesDiff:
    # print(i, latex(gradesDiff[i]))
    # print()

    T = f
    for i in range(2, taylorGrade + 1):
        T += ((h_ ** (i - 1)) / factorial(i)) * gradesDiff[i - 1]

    # print("T^" + str(taylorGrade) + ": \n", sp.latex(T), "\n")

    T_fun = lambda t, w, h: T.subs({X: t, Y(X): w, h_: h}).evalf()

    h = (maxValue - initX) / steps
    xi = float(initX)
    w = float(initY)

    # print("values of T:")
    for i in range(steps + 1):
        logic.data_xi.append(xi)
        logic.data_yi.append(w)

        yReal = float(eqMainSolve.rhs.subs("x", xi).evalf())
        logic.data_yir.append(yReal)
        logic.data_err.append(abs((yReal - w) / yReal))

        w = float(w + h * T_fun(xi, w, h))

        # print(T_fun(xi, lastW, h))

        xi += h

    return {
        "solution": lambda x: eqMainSolve.rhs.subs("x", x).evalf(),
        "solution_latex": reduceThePrecision(latex(eqMainSolve)),
    }
