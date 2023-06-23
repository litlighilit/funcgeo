from numpy import *

from .tools.rmtan90 import rmtan90
from .tools.replace import *


def get_all_mode():
    m1 = list("bcgkmrwy")
    m2 = "-- - -. :".split()
    m3 = list(".,ov^<>1234sp*hHd|_+x")
    for i in m1, m2, m3:
        i.append("")
    all_mode = []
    for i in m1:
        for j in m2:
            for z in m3:
                all_mode.append(i + j + z)
    return all_mode


all_mode = get_all_mode()


def flog(base, x):
    y = log(x) / log(base)
    return y


d1 = "^", "lg", "ln(", "log_{", "}("
d2 = "**", "log10", "log(", "flog(", ","
dic = dict(zip(d1, d2))


def trans2py(expr):
    res = expr
    for i in dic:
        res = res.replace(i, dic[i])

    res = replace2mul(res)
    res = replace2abs(res)
    return res


class FG:
    def_input = "(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0"

    @staticmethod
    def def_join(l):
        return ",".join(l)

    def __init__(self, input_getter, expilic_func_drawer, impilic_func_drawer):
        # @args:
        #   input_getter: ()->str
        #   expilic_func_drawer: (x, y, fmt, style, expr) -> Any where x,y: array_like; fmt: str; style: dict; expr: str
        #   impilic_func_drawer: (x, y, z, expr) -> Any where x,y,z: array_like; expr: str
        self.get_input = input_getter
        self.draw_expfunc = expilic_func_drawer
        self.draw_impfunc = impilic_func_drawer

    def parse_input(self, st):
        #ss = input("func expression(press Enter to plot):")
        s = st if not st.isspace() else self.def_input
        if s == ("quit()" or "exit()"):
            exec(s)
        ls = s.lower().split(",")
        on, om = True, True
        i = 0
        while i <= len(ls) - 1:
            if "n=" in ls[i]:
                self.n = eval(ls.pop(i).replace("n=", ""))
                on = False
                i -= 1
            if ls[i] in all_mode:
                mode = ls.pop(i)
                om = False
                i -= 1
            i += 1
        if on:
            self.n = 100
        if om:
            mode = "b-"
        self.mode = mode
        #sf = ",".join(ls)
        return ls

    def fp(self, ls):
        res1 = ls[0]
        res1 = trans2py(res1)
        res2 = ls[1]
        res2 = trans2py(res2)
        ar = ls[2].replace("=", "")
        ar = trans2py(ar)
        lt = ar.split("<")
        if len(lt) == 3:
            tn, tm = eval(lt.pop(0)), eval(lt.pop(-1))
        else:
            tn, tm = (-2, 2)
        exec(f"{lt[0]} = linspace({tn}, {tm}, {self.n})")
        exec(res1)
        exec(res2)
        # we must use `eval``, as in function local variables are referred by index and here `x`,`y` aren't indexed

        self.draw_expfunc(
            eval("x"),
            eval("y"),
            self.mode,
            dict(linewidth=1, picker=1.0),
            self.def_join(ls),
        )

    def fn(self, ls):
        le = len(ls)
        res0 = ls[0]
        res0 = trans2py(res0)
        rx = ls[1] if le >= 2 else "-2<x<2"
        rx = trans2py(rx)
        lx = rx.split("<")
        if res0.startswith("y="):
            exp = res0[2:]
            x = linspace(eval(lx[0]), eval(lx[2]), self.n)
            #except NameError: app.text.insert(0.0,'please check your input')
            y = eval(exp)

            rmtan90(exp, y, x, abs_tol=0.0)

            self.draw_expfunc(
                x, y, self.mode, dict(linewidth=1, picker=1.0), self.def_join(ls)
            )

        else:
            x = linspace(eval(lx[0]), eval(lx[-1]), self.n)
            ry = ls[2] if le >= 3 else "-2<y<2"
            ly = ry.split("<")
            y = linspace(eval(ly[0]), eval(ly[-1]), self.n)
            x, y = meshgrid(x, y)
            lres = res0.split("=")
            lres[-1] = "({})".format(lres[-1])
            res0 = "-".join(lres)
            #except NameError: app.text.insert(0.0,'please check your input')
            z = eval(res0)
            self.draw_impfunc(x, y, z, self.def_join(ls))

        #except RuntimeWarning: app.text.insert(0.0,'please check the domain of definition')

    def draw_expr(self, expr):
        ls = self.parse_input(expr)
        if len(ls) >= 3:
            if (ls[0].startswith("x=") and ls[1].startswith("y=")) or (
                ls[1].startswith("x=") and ls[0].startswith("y=")
            ):
                self.fp(ls)
        else:
            self.fn(ls)

    def draw(self):
        lf = self.get_input().split(";")
        if len(lf) != 0 and lf[0] != "":
            for e in lf:
                self.draw_expr(e)
            #app.draw()
