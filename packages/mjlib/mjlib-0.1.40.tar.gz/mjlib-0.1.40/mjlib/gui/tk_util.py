from tkinter import messagebox
import time
from pynput.mouse import Controller


def alert(title, message):
    return messagebox.askokcancel(title, message)

 # file = filedialog.askopenfilename(
 #     initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir, 'configs')),
 #     filetypes=(("json files", "*.json"),), title="Select config file to load")

 # file = filedialog.asksaveasfilename(
 #     initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir, 'configs')),
 #     filetypes=(("json files", "*.json"),), title="Select where to save config file")

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