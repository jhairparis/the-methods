

def secant(logic, fun, x_a, x_b, tol=1e-4, steps=100):
    logic.reset()

    logic.data = {
        "an": logic.data_an,
        "f(n-1)": logic.data_bn,
        "relative error": logic.data_err,
    }

    logic.method_title = "Secante"

    logic.data_an.append("%.6f" % x_a)
    logic.data_err.append("None")
    logic.data_an.append("%.6f" % x_b)
    logic.data_err.append("None")

    old_error = x_b
    p = x_b

    for n in range(steps):
        p = x_b - ((fun(x_b) * (x_b - x_a)) / (fun(x_b) - fun(x_a)))

        logic.data_an.append("%.6f" % p)
        logic.data_bn.append(fun(x_b))
        error = abs((p - old_error) / p)
        logic.data_err.append("%.6f" % error)

        if error < tol:
            return p

        x_a = x_b
        x_b = p

        old_error = p

    return p
