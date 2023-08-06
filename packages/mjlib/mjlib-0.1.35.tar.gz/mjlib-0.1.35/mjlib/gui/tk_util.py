import sys
import warnings
from tkinter import messagebox


def alert(title, message):
    return messagebox.askokcancel(title, message)

