from sympy import latex, sympify
from lib.precision import reduceThePrecision


def lagrange(table: dict):
    x = table["x"]
    y = table["f(x)"]
    solution = ""

    for i in range(len(table["x"])):
        lNumerator = "1"
        lDenominator = "1"

        for j in range(len(table["x"])):
            if i != j:
                lNumerator += f"*(x-{float(x[j])})"
                lDenominator += f"*({float(x[i])}-{float(x[j])})"

        solution += f"((({lNumerator})/({lDenominator}))*{float(y[i])})+"

    solution = solution[:-1]

    fn = sympify(solution)
    expanded = fn.expand()

    return {
        "solution": solution,
        "base": lambda x: fn.subs("x", x).evalf(),
        "latex": reduceThePrecision(latex(fn), 4),
        "expanded": lambda x: expanded.subs("x", x).evalf(),
        "expanded_latex": reduceThePrecision(latex(expanded), 4),
    }
