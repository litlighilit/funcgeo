from .cnf import (
    WIN_FIG_RATE_W,
    WIN_FIG_RATE_H,
    FIG_CAN_RATE_W,
    FIG_CAN_RATE_H,
    DPI,
    RES,
)
from .tkapp import Application


def _main(root):
    def locatewin():
        sc_w = root.winfo_screenwidth()
        sc_h = root.winfo_screenheight()
        w_w = WIN_FIG_RATE_W * sc_w
        w_h = WIN_FIG_RATE_H * sc_h
        s_w = (sc_w - w_w) / 2
        s_h = (sc_h - w_h) / 2
        return w_w, w_h, s_w, s_h

    def sizefig():
        width, height = winlocate[0:2]
        return FIG_CAN_RATE_W * width, FIG_CAN_RATE_H * height

    winlocate = locatewin()
    root.geometry("%dx%d+%d+%d" % (winlocate))
    root.configure(bg="#ababab")
    root.title("f-g")
    figsize = sizefig()
    app = Application(master=root, size=figsize, dpi=DPI, res=RES)
    app.pack(fill="both", expand=True)
    root.mainloop()


def main():
    from tkinter import Tk

    root = Tk()
    _main(root)


# now it's a pkg thus you can't run it as a module
#if __name__ == "__main__": main()
