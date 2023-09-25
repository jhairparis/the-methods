from numpy import isnan
from pandas import DataFrame
from sympy import latex, sympify




def center(table, max_length=None):
    # max(len(values) for values in table.values())
    for key, values in table.items():
        padding = (max_length - len(values)) // 2
        table[key] = (
            [None] * padding + values + [None] * (max_length - len(values) - padding)
        )

    return table


def divided_diff(table):
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

    for key in table.keys():
        if len(table[key]) < n:
            for i in range(n - len(table[key])):
                table[key].append(None)

    return DataFrame(table)


l = divided_diff(data)


def pol(table):
    ddpArr = []
    ddrArr = []
    for i in table:
        if i == "x":
            continue

        ddpArr.append(table.get(i).get(0))
        for j in range(len(table.get(i)) + 1):
            item = table.get(i).get(len(table.get(i)) - j)
            if item != None and not isnan(item):
                ddrArr.append(item)
                break

    def ddpGen(ddp):
        ddpStr = ""
        ddpSource = ""
        for i in range(len(ddp)):
            sc = f"*(x-{table['x'][i]})"
            ddpStr += "(" + str(ddp[i]) + ")" + ddpSource + "+"
            ddpSource += sc
        ddpStr = ddpStr[:-1]

        return ddpStr

    def ddrGen(ddr):
        ddrStr = ""
        ddrSource = ""
        for i in range(len(ddr)):
            scr = f"*(x-{table['x'][(len(ddr) - 1) - i]})"
            ddrStr += "(" + str(ddr[i]) + ")" + ddrSource + "+"
            ddrSource += scr

        ddrStr = ddrStr[:-1]

        return ddrStr

    sol = ddpGen(ddpArr)
    sol2 = ddrGen(ddrArr)

    print(sol, "\n", sympify(sol).expand(), "\n\n", sol2, "\n", sympify(sol2).expand())

