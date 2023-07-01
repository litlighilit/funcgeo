import matplotlib.collections
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#from matplotlib.backend_bases import key_press_handler # here hotkeys handlers are somehow useless

from os.path import dirname, join as pjoin
from functools import partial

from tkinter import Toplevel, Frame, StringVar, Menubutton, Label, Menu, Entry, Button
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
from tkinter.ttk import Separator

from .fg import FG

plt.rcParams["axes.unicode_minus"] = False


class StyleMenu(Toplevel):
    """layout:
    |b1|label|
    |b2|label|"""

    marker = " .,ov^<>1234sp*hHDd|_+x"  # specific chars

    def __init__(self, master=None, res=None, **cnf):
        # NOTE:
        #  if res is not None it must be an existing path
        #    otherwise here will raise `FileNotFoundError`
        super().__init__(master, cnf=cnf)
        self.res = res

        self.withdraw()
        ls_v = self.linestyle_v = StringVar(self)
        f1 = Frame(self)

        b1 = Menubutton(f1, text="change linestyle", relief="raised")
        Label(f1, textvariable=ls_v).pack(side="right")
        m = "- -- -. : None".split()
        line_menu = Menu(b1, tearoff=False)

        def add_l(l):
            line_menu.add_command(label=l, command=lambda: self.ch_linestyle(l))

        for i in m:
            add_l(i)  # capture i
        b1.config(menu=line_menu)
        b1.pack(side="right")

        f2 = Frame(self)
        m_v = self.marker_v = StringVar(self)
        b2 = Menubutton(f2, text="change marker:", relief="raised")
        self.marker_btn = b2  # used to remove or restore marker_btn
        Label(f2, textvariable=m_v).pack(side="right")
        mark_menu = Menu(b2, tearoff=False)

        def add_m(m):
            mark_menu.add_command(label=m, command=lambda: self.ch_marker(m))

        for i in self.marker:
            add_m(i)  # capture i
        m2_menu = Menu(mark_menu)

        ext_marker_res = self.res
        if ext_marker_res:
            with open(pjoin(dirname(__file__), ext_marker_res), encoding="utf-8") as f:
                mark2_d, mark2 = map(lambda c: c.split(","), f.read().split("\n"))
                for i, c in enumerate(mark2_d):
                    m2_menu.add_command(
                        label=c, command=lambda: self.ch_marker(mark2[i])
                    )
                mark_menu.add_cascade(label="ext", menu=m2_menu)

        def entk():
            s = askstring("", "marker:")
            self.ch_marker("$" + s + "$")

        mark_menu.add_command(label="custom", command=entk)

        b2.config(menu=mark_menu)
        b2.pack(side="right")

        f1.pack()
        Separator(self, orient="horizontal").pack(fill="x")
        f2.pack()

    def ch_linestyle(self, dest):
        obj = self.obj
        plt.setp(obj, linestyle=dest)
        self.master.canvas.draw()
        self.withdraw()

    def ch_marker(self, dest):
        obj = self.obj
        plt.setp(obj, marker=dest)
        self.master.canvas.draw()
        self.withdraw()

    def rm_marker_menu(self):
        self.marker_btn.pack_forget()

    def restore_marker_menu(self):
        self.marker_btn.pack()


class Handler:
    l0 = list("bcgkmrwy")
    l1 = "blue cyan green black magenta red white yellow".split()
    dc = dict(zip(l0, l1))

    def __init__(self, target, res={}):
        self.target = target
        self.target.style_menu = StyleMenu(self.target, res.get("marker", None))

    def ch_color(self, event):
        obj = event.artist

        if isinstance(obj, matplotlib.collections.PathCollection):
            c = obj.get_edgecolor()
            set_color = obj.set_edgecolor
        else:
            c = obj.get_color()
            set_color = obj.set_color
        if len(c) == 1:
            if isinstance(c, str):
                c = self.dc[c]
            else:
                c = tuple(round(i * 255) for i in c[0][:3])
        elif isinstance(c, tuple):
            c = tuple(round(i * 255) for i in c[:3])
        nc = (
            askcolor(color=c)[-1] or c
        )  # without 'or c', when askcolor returns `None`, there'll be an error
        set_color(nc)
        self.target.canvas.draw()

    def ch_style(self, event):
        obj = event.artist
        style_menu = self.target.style_menu
        style_menu.obj = obj
        if isinstance(obj, matplotlib.collections.PathCollection):
            style_menu.rm_marker_menu()  # PathCollection doesn't have `get_marker`
        else:
            style_menu.restore_marker_menu()
            style_menu.marker_v.set(obj.get_marker())
        style_menu.linestyle_v.set(obj.get_linestyle())
        style_menu.deiconify()
        # if `style_menu` was set as `self`'s attribute (and its master is `self.target`) and here we invoke is by `self.style_menu.deiconify()`
        #  then there'll be `_tkinter.TclError: bad window path name ".!application.!stylemenu"`

    def rmf(self, event):
        obj = event.artist
        sf = self.target.dfunc[str(obj)]
        # As we'll change the dict `self.target.dfunc` in the loop
        # if use the following:
        #  `for key in self.target.dfunc: ... `
        # then therer errors `RuntimeError: dictionary changed size during iteration`
        for key in tuple(self.target.dfunc):
            if self.target.dfunc[key] == sf:
                del self.target.dfunc[key]
        obj.remove()
        self.target.canvas.draw()
        self.target.rmenu.unpopup()


class RightMenu(Menu):
    Y_OFFSET = 6
    INIT = "INIT"  # original label
    event = None
    copy = lambda self, exp: (
        self.master.clipboard_clear(),
        self.master.clipboard_append(exp),
    )

    def __init__(self, master, handler, **cnf):
        super().__init__(master, cnf, tearoff=0)

        # click to copy its definition
        self.add_command(
            label=self.INIT,
            foreground="grey",
            command=lambda: self.copy(handler.target.dfunc[str(self.event.artist)]),
        )

        self.add_command(
            label="set color", command=lambda: handler.ch_color(self.event)
        )
        self.add_command(
            label="set style", command=lambda: handler.ch_style(self.event)
        )

        self.add_separator()
        self.add_command(label="remove", command=lambda: handler.rmf(self.event))

    def popup(self, x, y):
        super().post(x, y + self.Y_OFFSET)

    def unpopup(self):
        super().unpost()

    def bind_evt(self, evt):
        self.event = evt

        def do_popup(event):
            try:  # avoid error after "remove"
                self.popup(event.x_root, event.y_root)
            finally:
                self.master.unbind("<Button-3>", id)

        id = self.master.bind("<Button-3>", do_popup)


def draw_expfunc(app, x, y, fmt, d, expr):
    (f,) = app.au.plot(x, y, fmt, **d)
    app.dfunc[str(f)] = expr


def draw_impfunc(app, x, y, z, expr):
    for i in app.au.contour(x, y, z, 0).collections:
        #print(i)
        i.set_picker(2.0)
        app.dfunc[str(i)] = expr


class Application(Frame):
    def __init__(self, master, size, dpi=100, res={}, cnf={}):
        super().__init__(master, cnf=cnf)
        self.dfunc = {}  # :dict[str, str]  # map id of obj to string of its expression
        self.fg = FG(
            self.get_input, partial(draw_expfunc, self), partial(draw_impfunc, self)
        )
        self.size = size
        self.dpi = dpi
        self.handler = Handler(self, res)
        self.rmenu = RightMenu(self.master, self.handler)
        self.init_canvas()
        self.create_widget()

    def fmain(self):
        self.fg.draw()
        self.draw()

    def create_widget(self):
        Label(self, text="expression").pack()
        self.input_v = StringVar()
        input_entry = Entry(self, textvariable=self.input_v)
        input_entry.bind("<Key-Return>", lambda x: self.fmain())
        input_entry.pack()
        Button(self, text="plot", command=self.fmain).pack()

    def init_canvas(self):
        figsize = tuple(map(lambda x: x / self.dpi, self.size))
        self.fig = plt.Figure(
            figsize=figsize,
            dpi=self.dpi,
            facecolor="#0000006f",
            edgecolor="#99e5ff0f",
            linewidth=3,
        )
        self.au = self.fig.add_subplot(111)
        self.au.axis("equal")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas._tkcanvas.pack(side="top", fill="both", expand=True)

        def popup(evt=None):
            if not evt:
                print("here")
            if evt:
                rmenu = self.rmenu
                rmenu.entryconfig(0, label=self.dfunc[str(evt.artist)])
                rmenu.bind_evt(evt)

        self.canvas.mpl_connect("pick_event", popup)
        NavigationToolbar2Tk(self.canvas, self)  #self.canvas.toolbar

        # add `exec` func
        def to_exec0(event):
            menu = Menu(self.master)

            def to_exec():
                pycmd = askstring("", "pycmd:")
                exec(pycmd)

            menu.add_command(label="cmd>python", command=to_exec)
            menu.post(event.x_root, event.y_root)

        self.master.bind("<Control-1>", to_exec0)

    def draw(self):
        self.canvas.draw()

    def get_input(self):
        res = self.input_v.get()
        self.input_v.set("")
        return res
