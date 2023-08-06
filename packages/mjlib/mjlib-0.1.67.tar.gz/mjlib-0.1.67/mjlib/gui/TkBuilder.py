import tkinter as tk
from abc import ABC, abstractmethod


class TkBuilder(ABC):
    def __init__(self, widget):
        self.widget = widget

    def Label(self, text="label text"):
        l = tk.Label(self.widget, text=text)
        return self.layout(l)

    def Button(self, text="button text", command=lambda: None):
        b = tk.Button(self.widget, text=text, command=command)
        return self.layout(b)

    def RadioButton(self, text="radio button text", prop=None):
        rb = tk.Radiobutton(self.widget, text=text, variable=prop, value=text)
        return self.layout(rb)

    def OptionMenu(self, prop=None, options=()):
        om = tk.OptionMenu(self.widget, variable=prop, *options)
        return self.layout(om)

    def CheckBox(self, text="checkbox text", prop=None):
        cb = tk.Checkbutton(self.widget, text=text, onvalue=True, offvalue=False, variable=prop)
        return self.layout(cb)

    def Scale(self, min=1, max=10, initial=5, orient=tk.HORIZONTAL):
        s = tk.Scale(self.widget, from_=min, to_=max, orient=orient)
        s.set(initial)
        return self.layout(s)

    def Entry(self, textvar=None, callback=None):
        if textvar is not None:
            v = textvar.get()
        e = tk.Entry(self.widget, textvariable=textvar, width=10,callback=callback)
        if textvar is not None:
            textvar.set(v)
        return self.layout(e)

    def SpinBox(self, prop=None, callback=None, min=1, max=10):
        s = tk.Spinbox(self.widget, textvariable=prop, from_=min, to_=max, width=5, callback=None)
        return self.layout(s)

    def canv(self, width=130, height=200, bg="white"):
        canv = tk.Canvas(self.widget, width=width, height=height, bg=bg)
        return self.layout(canv)
        # canv.grid(row=0, column=9, sticky=W + N + S + E, columnspan=2)

    def _layout(self, widget):
        layout(widget)
        return widget

    @abstractmethod
    def layout(self, widget):
        pass
