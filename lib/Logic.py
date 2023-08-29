from pandas import DataFrame
from sympy import sympify
from lib.methods.bisection import bisection
from lib.methods.newton import newton
from lib.methods.secant import secant


class Logic:
    method_title = ""

    data_an = []
    data_bn = []
    data_Pn = []
    data_fafp = []
    data_fa = []
    data_fb = []
    data_fp = []
    data_err = []

    data = {
        "an": data_an,
        "bn": data_bn,
        "Pn": data_Pn,
        "f(a)*f(p)": data_fafp,
        "relative error": data_err,
    }

    def get_method(self, index):
        methods = [bisection, newton, secant]

        return methods[index]

    def gen_fn(self, operation="x**2"):
        try:
            equation = sympify(operation)

            def f(x=1):
                return equation.subs("x", x).evalf()

            return f
        except:
            return lambda x: x**2

    def reset(self):
        self.method_title = ""
        self.data_an.clear()
        self.data_bn.clear()
        self.data_Pn.clear()
        self.data_fafp.clear()
        self.data_fa.clear()
        self.data_fb.clear()
        self.data_fp.clear()
        self.data_err.clear()

        self.data = {
            "an": self.data_an,
            "bn": self.data_bn,
            "Pn": self.data_Pn,
            "f(a)*f(p)": self.data_fafp,
            "relative error": self.data_err,
        }

    def show_table(self, gui=False):
        df = DataFrame(self.data)
        if gui:
            return df
        else:
            s = ""
            for i in range(len(self.data_an)):
                s += (
                    "Iteracion=  %03d" % i
                    + " ; a= "
                    + self.data_an[i]
                    + " ; p= "
                    + self.data_Pn[i]
                    + " ; b= "
                    + self.data_bn[i]
                    + " ; f(a)*f(p)= "
                    + self.data_fafp[i]
                    + " ; er= "
                    + self.data_err[i]
                    + "\n"
                )
            return s
