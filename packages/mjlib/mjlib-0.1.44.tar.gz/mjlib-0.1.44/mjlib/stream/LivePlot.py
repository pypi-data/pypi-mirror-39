from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import zeros
from tkinter import N, S, E, W,

class LivePlot:
    def __init_(self, root):
        self.window_length = 100
        self.x = range(self.window_length)
        Fig = Figure(figsize=(5, 4), dpi=100)
        self.FigSubPlot = Fig.add_subplot(111)
        # self.FigSubPlot.axes.get_xaxis().set_visible(False)
        # self.canvas.figure.axes[0].set_xlim(min(self.fig_x), max(self.fig_x))

        self.lines = []
        self.line1, = LiveLine(self,'r-')
        self.line2, = LiveLine(self,'y-')
        self.canvas = FigureCanvasTkAgg(Fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=10,
                                         sticky=N + S + W + E)

        self.stream1 = None
        self.stream2 = None


    def animate(self):
        for l in self.lines:
            l.animate()
        self.canvas.draw()

    def connect(self,stream,linei):
        def listener(sample):
            newY = self.lines[linei].y
            del newY[-1]
            newY.insert(0,sample)
            self.lines[linei].y = newY
        stream += listener

    class LiveLine:
        def __init__(self,livePlot,lineno,look):
            self.livePlot = livePlot
            self._line = livePlot.FigSubPlot.plot([], [], look)
            self.y = zeros(livePlot.window_length)
            livePlot.lines.append(self)
            self.i = len(livePlot.lines)-1

        def animate(self):
            self._line.set_data(self.livePlot.x, self.y)