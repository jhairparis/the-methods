def secant(logic, fun, x_a, x_b, tol=1e-4, steps=100):
    logic.reset()

    logic.data = {
        "Xn-1": logic.data_an,
        "f(Xn-1)": logic.data_fa,
        "Xn-2": logic.data_bn,
        "f(Xn-2)": logic.data_fb,
        "Xn": logic.data_Pn,
        "relative error": logic.data_err,
    }

    logic.method_title = "Secante"

    old_error = 0
    p = x_b

    for n in range(steps):
        p = x_b - ((fun(x_b) * (x_b - x_a)) / (fun(x_b) - fun(x_a)))

        logic.data_an.append("%.6f" % x_a)
        logic.data_fa.append("%.6f" % fun(x_a))
        logic.data_bn.append("%.6f" % x_b)
        logic.data_fb.append("%.6f" % fun(x_b))
        logic.data_Pn.append("%.6f" % p)

        error = abs((p - old_error) / p)
        logic.data_err.append("%.6f" % error)

        if error < tol:
            return p

        x_a = x_b
        x_b = p

        old_error = p

    return p
