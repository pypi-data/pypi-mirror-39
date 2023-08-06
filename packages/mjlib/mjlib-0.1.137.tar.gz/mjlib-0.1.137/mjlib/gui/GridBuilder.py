import tkinter as tk

from mjlib.gui.TkBuilder import TkBuilder


class GridBuilder(TkBuilder):
    def __init__(self, widget):
        TkBuilder.__init__(self, widget)
        self.row = 0
        self.col = 0
        self._maxRow = 0
        self._maxCol = 0
        self.orientation = tk.RIGHT
        self.columnspan = 1  # default tkinter value
        self.rowspan = 1  # default tkinter value
        self.sticky = ""
        self.hold = False

    def layout(self, widget):
        widget.grid(row=self.row, column=self.col, columnspan=self.columnspan, rowspan=self.rowspan, sticky=self.sticky)
        self._move()
        return widget

    def nextRow(self):
        if not self.hold:
            self.row += 1
            self.col = 0

    def evenOut(self,n=1):
        for i in range(self._maxCol + 1):
            tk.Grid.columnconfigure(self.widget, i, weight=n)
        for i in range(self._maxRow + 1):
            tk.Grid.rowconfigure(self.widget, i, weight=n)

    def resetExtraOptions(self):
        self.columnspan = 1
        self.rowspan = 1
        self.sticky = ""

    def _move(self):
        if not self.hold:
            self._maxCol = max(self.col, self._maxCol)
            self._maxRow = max(self.row, self._maxRow)
            if self.orientation is tk.RIGHT:
                self.col += 1
            else:
                self.row += 1

    def save(self):
        return {
            'row': self.row,
            'col': self.col,
            'orientation': self.orientation,
            'columnspan': self.columnspan,
            'rowspan': self.rowspan,
            'rowspan': self.rowspan,
            'sticky': self.sticky,
        }

    def load(self, save):
        for key, value in save.items():
            self.__setattr__(key, value)
