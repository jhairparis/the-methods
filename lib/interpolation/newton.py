from pandas import DataFrame



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

    return DataFrame(center(table, n))


print(divided_diff(data))
