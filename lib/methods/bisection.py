from plyer import notification


def bisection(logic, fun, x_a, x_b, tol=1e-4, steps=100):
    logic.reset()

    if fun(x_a) * fun(x_b) >= 0:
        notification.notify(
            title="Error",
            message="⚠️ The bisection method cannot be applied! ⚠️",
            app_icon=None,
            timeout=2,
        )
        return None

    logic.method_title = "Bisection"

    old_error = 0
    for n in range(steps):
        x_m = (x_a + x_b) / 2

        fafp = fun(x_a) * fun(x_m)
        error = abs((x_m - old_error) / x_m)

        logic.data_an.append("%.6f" % x_a)
        logic.data_bn.append("%.6f" % x_b)
        logic.data_Pn.append("%.6f" % x_m)
        logic.data_fafp.append("%.6F" % fafp)
        logic.data_err.append("%.6f" % error)

        if fun(x_m) == 0 or error < tol:
            return x_m
        if fun(x_a) * fun(x_m) < 0:
            x_b = x_m
        else:
            x_a = x_m

        old_error = x_m

    return (x_a + x_b) / 2
