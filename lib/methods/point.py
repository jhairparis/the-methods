def point(logic, fun, g, x_a, tol=1e-4, steps=100, x_b=None):
    logic.reset()

    logic.method_title = "Punto fijo"

    logic.data = {
        "x": logic.data_an,
        "g(x)": logic.data_fa,
        "relative error": logic.data_err,
    }

    old_error = 0
    for n in range(steps):
        logic.data_an.append("%.6f" % x_a)

        x_a = g(x_a)

        error = abs((x_a - old_error) / x_a)
        logic.data_err.append("%.6f" % error)
        logic.data_fa.append("%.6f" % x_a)

        if error < tol:
            return x_a

        old_error = x_a


    return x_a
