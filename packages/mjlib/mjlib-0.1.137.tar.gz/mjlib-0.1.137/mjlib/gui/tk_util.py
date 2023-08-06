from tkinter import messagebox
import time
from pynput.mouse import Controller
import tkinter as tk
from tkinter import N, S, E, W, filedialog

def window_bounds(win,w,h,x,y):
    win.wm_geometry("%dx%d+%d+%d"%(w,h,x,y))


def circle(canv):
    # IF I DO
    # self.stim_feedback_canv.itemconfigure(self.circ_2, fill="white")
    # I NEED TO: self.canvas.draw()
    return canv.create_oval(20, 70, 120, 170)


def text(canv):
    return canv.create_text(70, 120, text="28Hz")

def line(canv):
    return canv.create_line(0, 25, 2000, 25)

def alert(title, message):
    return messagebox.askokcancel(title, message)

 # file = filedialog.askopenfilename(
 #     initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir, 'configs')),
 #     filetypes=(("json files", "*.json"),), title="Select config file to load")

 # file = filedialog.asksaveasfilename(
 #     initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir, 'configs')),
 #     filetypes=(("json files", "*.json"),), title="Select where to save config file")



# self.line2 = self.FigSubPlot.axes.axvline(x=config.cfg.FREQ2, linewidth=2, color='grey')
#         elif self.line1 is not None:
#             self.FigSubPlot.axes.lines.remove(self.line1)

def center(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def mouse_mover():
    mouse = Controller()
    keep_moving_mouse = True
    l = True
    while keep_moving_mouse:
        time.sleep(.01)
        if l:
            mouse.move(0, -1)
        else:
            mouse.move(0, 1)
        l = not l