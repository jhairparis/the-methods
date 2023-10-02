from sympy import latex, sympify


def lagrange(table: dict):
    x = table["x"]
    y = table["f(x)"]
    solution = ""

    for i in range(len(table["x"])):
        lNumerator = "1"
        lDenominator = "1"

        for j in range(len(table["x"])):
            if i != j:
                lNumerator += f"*(x-{x[j]})"
                lDenominator += f"*({x[i]}-{x[j]})"

        solution += f"((({lNumerator})/({lDenominator}))*{y[i]})+"

    solution = solution[:-1]

    fn = sympify(solution)
    expanded = fn.expand()

    return {
        "solution": solution,
        "base": lambda x: fn.subs("x", x).evalf(),
        "latex": latex(fn),
        "expanded": lambda x: expanded.subs("x", x).evalf(),
        "expanded_latex": latex(expanded),
    }
