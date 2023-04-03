#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pylab as pl
import os.path

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

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


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="tkGraf")
        self.lbl.pack()

        self.fileFrame = tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5, fill="x")
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(anchor="w", fill="x")
        self.fileBtn = tk.Button(self.fileFrame, text="...", command=self.selectFile)
        self.fileBtn.pack(anchor="e")

        self.dataformatVar = tk.StringVar(value="ROW")
        self.rowRadio = tk.Radiobutton(self.fileFrame, text="Data v řádcích", variable=self.dataformatVar, value="ROW")
        self.rowRadio.pack(anchor="w")
        self.columnRadio = tk.Radiobutton(self.fileFrame, text="Data ve sloupcích", variable=self.dataformatVar, value="COLUMN")
        self.columnRadio.pack(anchor="w")

        self.grafFrame = tk.LabelFrame(self, text="Graf")
        self.grafFrame.pack(padx=5, pady=5, anchor="w", fill="x")

        tk.Label(self.grafFrame, text="Titulek").grid(row=0, column=0)
        self.titleEntry = MyEntry(self.grafFrame)
        self.titleEntry.grid(row=0, column=1, sticky=tk.EW)

        tk.Label(self.grafFrame, text="osa X").grid(row=1, column=0)
        self.xEntry = MyEntry(self.grafFrame)
        self.xEntry.grid(row=1, column=1, columnspan=2, sticky=tk.EW)

        tk.Label(self.grafFrame, text="osa Y").grid(row=2, column=0)
        self.yEntry = MyEntry(self.grafFrame)
        self.yEntry.grid(row=2, column=1, sticky=tk.EW)

        tk.Label(self.grafFrame, text="mřížka").grid(row=3, column=0)
        self.gridVar = tk.BooleanVar(value=True)
        self.gridCheck = tk.Checkbutton(self.grafFrame, variable=self.gridVar)
        self.gridCheck.grid(row=3, column=1, sticky="w")

        self.lineVar = tk.StringVar(value="none")
        tk.Label(self.grafFrame, text="čára").grid(row=4, column=0)
        tk.OptionMenu(self.grafFrame, self.lineVar, "none", "-", "--", "-.", ":").grid(row=4, column=1, sticky="w")

        self.markerVar = tk.StringVar(value="none")
        tk.Label(self.grafFrame, text="marker").grid(row=5, column=0)
        tk.OptionMenu(self.grafFrame, self.markerVar, "none", *tuple("xX+P,.o*1234")).grid(row=5, column=1, sticky="w")

        tk.Button(self, text="Vykreslit", command=self.plot).pack(anchor="w")

        tk.Button(self, text="Quit", command=self.quit).pack(anchor="e")

        mainMenu = tk.Menu(self)

        fileMenu = tk.Menu(mainMenu)
        mainMenu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Open', command=self.quit)
        fileMenu.add_command(label='Save', command=self.quit)
        fileMenu.add_separator()
        fileMenu.add_command(label='Quit', command=self.quit)
        
        editMenu = tk.Menu(mainMenu)
        mainMenu.add_cascade(label='Edit', menu=editMenu)
        ovoceMenu = tk.Menu(editMenu)
        editMenu.add_cascade(label='ovoce', menu=ovoceMenu)
        zeleninaMenu = tk.Menu(editMenu)
        editMenu.add_cascade(label='zelenina', menu=zeleninaMenu)
        
        ovoceMenu.add_command(label='jabko')
        ovoceMenu.add_command(label='hruška')
        ovoceMenu.add_command(label='švestka')
        
        zeleninaMenu.add_radiobutton(label="zeli")
        zeleninaMenu.add_radiobutton(label="kapusta")
        zeleninaMenu.add_radiobutton(label="mrkev")

        mainMenu.add_cascade(label='Selection')

        self.config(menu=mainMenu)

    def selectFile(self):
        self.fileEntry.value = filedialog.askopenfilename()

    def plot(self):
        if not os.path.isfile(self.fileEntry.value):
            return
        with open(self.fileEntry.value, "r") as f:
            if self.dataformatVar.get() == "ROW":
                x = f.readline().split(";")
                y = f.readline().split(";")
                x = [float(i.replace(",", ".")) for i in x]
                y = [float(i.replace(",", ".")) for i in y]
            elif self.dataformatVar.get() == "COLUMN":
                x = []
                y = []
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    if ";" not in line:
                        continue
                    x1, y1 = line.split(";")
                    x.append(float(x1.replace(",", ".")))
                    y.append(float(y1.replace(",", ".")))

        bagr = {}
        bagr['linestyle'] = self.lineVar.get()
        bagr['marker'] = self.markerVar.get()

        pl.plot(x, y, linestyle=self.lineVar.get(), marker=self.markerVar.get())
        pl.title(self.titleEntry.value)
        pl.xlabel(self.xEntry.value)
        pl.ylabel(self.yEntry.value)
        pl.grid(self.gridVar.get())
        pl.show()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()