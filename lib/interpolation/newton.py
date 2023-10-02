from numpy import isnan
from pandas import DataFrame
from sympy import latex, sympify


def center(table: dict, max_length: int = None):
    # max(len(values) for values in table.values())
    for key, values in table.items():
        padding = (max_length - len(values)) // 2
        table[key] = (
            [None] * padding + values + [None] * (max_length - len(values) - padding)
        )


def normalize(table: dict, n: int):
    for key in table.keys():
        if len(table[key]) < n:
            for i in range(n - len(table[key])):
                table[key].append(None)


def divided_diff(table: dict) -> dict:
    x = table["x"]
    y = table["f(x)"]

    if len(x) != len(y):
        raise ValueError("x and y must have the same length")

    n = len(x)

    row = []
    table[0] = row
    for j in range(n - 1):
        row.append((y[j + 1] - y[j]) / (x[j + 1] - x[j]))

    i = 0
    while len(table) < n + 1:
        row = []
        for k in range(len(table[i]) - 1):
            row.append((table[i][k + 1] - table[i][k]) / (x[k + (i + 2)] - x[k]))
        table[i + 1] = row
        i += 1

    return table


def polynomialDDP(table: DataFrame):
    ddp = []
    for i in table:
        if i == "x":
            continue
        ddp.append(table.get(i).get(0))

    solution = ""
    ddpSource = ""
    for i in range(len(ddp)):
        sc = f"*(x-{table['x'][i]})"
        solution += "((" + str(ddp[i]) + ")" + ddpSource + ")+"
        ddpSource += sc

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


def polynomialDDR(table: DataFrame):
    ddr = []
    for i in table:
        if i == "x":
            continue
        for j in range(len(table.get(i)) + 1):
            item = table.get(i).get(len(table.get(i)) - j)
            if item != None and not isnan(item):
                ddr.append(item)
                break

    solution = ""
    ddrSource = ""
    for i in range(len(ddr)):
        scr = f"*(x-{table['x'][(len(ddr) - 1) - i]})"
        solution += "(" + str(ddr[i]) + ")" + ddrSource + "+"
        ddrSource += scr

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
