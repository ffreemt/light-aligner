"""
get_filename
"""

from pathlib import Path

# from tkinter import filedialog as fd
import tkinter as tk
from tkinter import filedialog


# fmt: off
def get_filename(
        title="Select a file",
        initialdir=Path.home().as_posix(),
        filetypes=(
            ("text files", "*.txt"),
            # ("gzip files", "*.gz"),
            # ("bzip2 files", "*.bz2"),
            ("all files", "*.*"),
        ),
):
    # fmt: on
    """get_filename"""
    root = tk.Tk()
    root.withdraw()
    # f_dir = Path(__file__).parent
    # f_dir = Path.home()  # noqa:  F841
    f_name = filedialog.askopenfilename(
        parent=root, initialdir=initialdir, filetypes=filetypes, title=title,
    )
    return f_name


if __name__ == "__main__":
    get_filename()
