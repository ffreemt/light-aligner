""" tkinter aligner UI part.

based on  aligner_ui.py
"""

import os
import tkinter as tk
from tkinter import messagebox
# import atexit

import logzero
from logzero import logger

from aligner_ui import Aligner


def tkaligner() -> None:
    """ tkinter aligner UI part
    """

    root = tk.Tk()

    # top = tk.Toplevel(root)
    # Aligner(top)

    Aligner(root)

    logger.debug("tkaligner debug ")

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":

    _ = os.environ.get("ALIGNER_DEBUG")
    if _ is not None and _.lower() in ["1", "true"]:
        logzero.loglevel(10)  # 10: DEBUG, default 20: INFO:
    else:
        logzero.loglevel(20)
    logger.info('os.environ.get("ALIGNER_DEBUG"): %s', _)

    tkaligner()
