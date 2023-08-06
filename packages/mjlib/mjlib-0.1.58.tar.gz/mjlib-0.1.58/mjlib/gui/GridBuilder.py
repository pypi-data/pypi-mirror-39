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
        self.hold = False

    def layout(self, widget):
        widget.grid(row=self.row, column=self.col)
        self._move()
        return widget

    def nextRow(self):
        if not self.hold:
            self.row += 1
            self.col = 0

    def evenOut(self):
        for i in range(self._maxCol + 1):
            tk.Grid.columnconfigure(self.widget, i, weight=1)
        for i in range(self._maxRow + 1):
            tk.Grid.rowconfigure(self.widget, i, weight=1)

    def resetExtraOptions(self):
        self.columnspan = 1

    def _move(self):
        if not self.hold:
            if self.orientation is tk.RIGHT:
                self.col += 1
            else:
                self.row += 1
            self._maxCol = max(self.col, self._maxCol)
            self._maxRow = max(self.row, self._maxRow)
