import tkinter as tk
import tkinter.ttk as ttk
from math import sqrt

ymax = 0.05
xmax = 0.01

class Application:
    def __init__(self, master, points: list):
        self.master = master
        self.canvas = tk.Canvas(self.master, 
                                width=500, height=450, 
                                bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.canvas.create_line(60, 420, 60, 50, fill='black', arrow=tk.LAST)
        for i in range(11):
            h = 420 - i * 35
            if i != 0:
                self.canvas.create_line(60, h, 65, h)
            self.canvas.create_text(37, h, text="%.3f" % (ymax / 10 * i))
        self.canvas.create_text(55, 40, text="Rc/L0")

        self.canvas.create_line(60, 420, 420, 420, fill='black', arrow=tk.LAST)
        for i in range(1, 6):
            w = 60 + i * 68
            self.canvas.create_line(w, 415, w, 420)
            self.canvas.create_text(w - 6, 432, text="%.4f" % (xmax / 5 * i))
        self.canvas.create_text(440, 420, text="λ/a")

        indices = ["100", "110", "111", "200", "210", "211", "220", "221/300", 
                   "310", "311", "222", "320", "321", "400", "322/410", "330/411",
                   "331", "420", "421", "332", "422", "430/500", "431/510", "333/511"]
        for ind in indices:
            h, k, l = tuple(map(int, ind[:3]))
            incl = sqrt(h ** 2 + k ** 2 + l ** 2)
            rm = xmax + 0.0002
            bm = rm * incl
            if bm > ymax * 1.02:
                bm = ymax * 1.02
                rm = bm / incl
            x = rm / xmax * 5 * 68 + 60
            y = 420 - bm / ymax * 10 * 35
            self.canvas.create_line(60, 420, x, y)

        self.current_value = tk.DoubleVar()
        self.lines = None

        def write(event):
            x = 60 + self.slider.get() / xmax * 5 * 68
            ys = [420 - p / ymax * 10 * 35 for p in points]
            if self.lines is not None:
                for line in self.lines:
                    self.canvas.delete(line)
            self.lines = [self.canvas.create_line(x, 60, x, 420, fill='red')
                    ] + [self.canvas.create_line(x, y, x + 10, y, fill='red')
                         for y in ys] + [
                         self.canvas.create_text(450, 400, fill='red',
                            text='λ/a=%.5f' % self.slider.get())]

        self.slider = ttk.Scale(
            self.master,
            from_=0.0,
            to=xmax,
            length=350,
            orient='horizontal',
            variable=self.current_value,
            command=write
        )
        self.slider.pack()


def show(points: list):
    window = tk.Tk()
    window.geometry('500x500')
    window.title('index method')
    window.resizable(False, False)

    Application(window, points)
    window.mainloop()

show(list(map(float, input("Please input angles:\n").split())))