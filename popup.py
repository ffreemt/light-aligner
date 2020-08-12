import tkinter as tk
from tkinter import messagebox

def popup(message, title=None):
    root = tk.Tk()
    root.withdraw()
    root.focus_force()
    messagebox.showinfo(title, message, parent=root, default = "ok")

    root.destroy()

popup('foo')