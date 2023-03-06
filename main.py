#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
import pylab as pl

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw, width=43)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Grafy"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)

        self.frameEntry = tk.Frame(self)
        self.frameEntry.pack()

        self.entry = MyEntry(self.frameEntry)
        self.entry.pack()

        self.btn = tk.Button(self, text="...", command = self.select)
        self.btn.pack()
        self.btn1 = tk.Button(self, text="Kreslit", command = self.show)
        self.btn1.pack()
        self.btn2 = tk.Button(self, text="Quit",  command = self.quit)
        self.btn2.pack()

    def select(self):
        self.soubor = filedialog.askopenfilename()
        self.entry.delete(0, "end")
        self.entry.insert(0, self.soubor)

    def show(self):
        xaxis = []
        yaxis = []
        with open(self.soubor, 'r') as f:
            print(self.soubor)
            while True:
                line = f.readline()
                if line == '':  #jsem na konci souboru
                    break
                x, y = line.split()
                xaxis.append(float(x))
                yaxis.append(float(y))
        pl.plot(xaxis, yaxis)
        pl.show()


    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()
