from abc import ABC, abstractmethod
from tkinter import ttk, HORIZONTAL, StringVar, LEFT, RIGHT


class TkBuilder(ABC):
    def __init__(self, widget):
        self.widget = widget

    def Label(self, **kwargs):
        if not 'text' in kwargs:
            kwargs['text'] = "label text"
        l = ttk.Label(self.widget, **kwargs)
        return self.layout(l)

    def Button(self, text="button text", command=lambda: None):
        b = ttk.Button(self.widget, text=text, command=command)
        return self.layout(b)

    def RadioButton(self, text="radio button text", prop=None):
        rb = ttk.Radiobutton(self.widget, text=text, variable=prop, value=text)
        return self.layout(rb)

    def OptionMenu(self, *options, name=None,prop=None, initial=None):
        if name is not None:
            fram = ttk.Frame(self.widget)
            om = ttk.OptionMenu(fram, prop,initial, style='matt.TMenubutton', *options)
            return self._with_label(name,fram,om)
        else:
            om = ttk.OptionMenu(self.widget, prop,initial, style='matt.TMenubutton',*options)
            return self.layout(om)

    def CheckBox(self, text="checkbox text", prop=None):
        cb = ttk.Checkbutton(self.widget, text=text, onvalue=True, offvalue=False, variable=prop)
        return self.layout(cb)

    def Scale(self, min=1, max=10, initial=5, orient=HORIZONTAL):
        s = ttk.Scale(self.widget, from_=min, to_=max, orient=orient)
        s.set(initial)
        return self.layout(s)

    def Entry(self, name=None, initial=None, textvar=None, callback=None):

        if textvar is not None:
            v = textvar.get()
        else:
            textvar = StringVar(self.widget)
        if callback is not None:
            def proto_callback(*dummy):
                callback(textvar.get())

            textvar.trace(mode='w', callback=proto_callback)

        kwargs = {'textvariable': textvar, 'width': 10,'style':'matt.TEntry'}

        if initial is not None:
            textvar.set(initial)

        if name is not None:
            fram = ttk.Frame(self.widget)
            e = ttk.Entry(fram, **kwargs)
            return self._with_label(name,fram,e)
        else:
            e = ttk.Entry(self.widget, **kwargs)
            return self.layout(e)

    def SpinBox(self, prop=None, callback=None, min=1, max=10):
        s = tk.Spinbox(self.widget, textvariable=prop, from_=min, to_=max, width=5, callback=None)
        return self.layout(s)


    def _with_label(self,name,fram,w):
        l = ttk.Label(fram, text=name)
        l.pack(side=LEFT)
        w.pack(side=RIGHT)
        self.layout(fram)
        return w


    def canv(self, width=130, height=200, bg="white"):
        canv = ttk.Canvas(self.widget, width=width, height=height, bg=bg)
        return self.layout(canv)
        # canv.grid(row=0, column=9, sticky=W + N + S + E, columnspan=2)

    def _layout(self, widget):
        layout(widget)
        return widget

    @abstractmethod
    def layout(self, widget):
        pass
