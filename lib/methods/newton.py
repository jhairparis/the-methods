from sympy import diff, sympify, abc


def derivative(functionX):
    dx = diff(sympify(functionX), abc.x)

    def fd(x: 1):
        return dx.evalf(subs={"x": x})

    return fd


def newton(logic, fun, deri, x_a, tol=1e-4, steps=100, x_b=None):
    logic.reset()

    logic.method_title = "Newton"

    logic.data = {
        "p": logic.data_an,
        "f(p)": logic.data_fa,
        "deirivada(p)": logic.data_fb,
        "f(p)/derivada(p)": logic.data_fp,
        "relative error": logic.data_err,
    }

    p = x_a
    old_error = 0
    for n in range(steps):
        logic.data_an.append("%.6f" % p)

        error = abs((p - old_error) / p)
        logic.data_err.append("%.6f" % error)

        logic.data_fa.append("%.6f" % fun(p))
        logic.data_fb.append("%.6f" % deri(p))
        logic.data_fp.append("%.6f" % (fun(p) / deri(p)))

        if error < tol:
            return p

        old_error = p
        p = p - (fun(p) / deri(p))

    return p
