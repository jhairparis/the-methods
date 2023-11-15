from sympy import Symbol, Function, dsolve,Eq,sympify


def solveDiff(eqMain: str, y: Function, x: Symbol, initX: float, initY: float):
    temp = eqMain.split("=")
    eqSympy = Eq(sympify(temp[0]), sympify(temp[1]))

    return dsolve(eqSympy, y(x), ics={y(initX): initY})
