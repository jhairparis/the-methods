from sympy import factorial, latex, sympify


f_str = input("f(x)=")
k = int(input("k="))
x0 = int(input("x0="))

f = sympify(f_str)

pol = ""

for i in range(k):
    num = latex(f.subs("x", x0).evalf())
    pol += f"({num}*(x-{x0})**{i})/{factorial(i)}+"
    f = f.diff()

pol = pol[:-1]


print(latex(sympify(pol)))
