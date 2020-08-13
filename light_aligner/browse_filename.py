"""
browse to a file

https://pythonspot.com/tk-file-dialogs/
filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
"""
# import sys
from pathlib import Path

from tkinter import filedialog, Tk

# from light_aligner.tkroot import tkroot


# fmt: off
def browse_filename(
        initialdir=Path.cwd(),
        title="Select a file",  # pylint: disable=duplicate-code
        filetypes=(
            ("text files", "*.txt"),
            # ("gzip files", "*.gz"),
            # ("bzip2 files", "*.bz2"),
            ("all files", "*.*"),
        ),
):
    # fmt: on
    """ browse for a filename"""
    root = Tk()   # Tk() started in __main__.py, multiple Tk may cause problems
    root.withdraw()
    if (initialdir / "data").exists():
        initialdir = initialdir / "data"
    filename = filedialog.askopenfilename(
        parent=root,
        # parent=tkroot,
        initialdir=initialdir,
        title=title,
        filetypes=filetypes,
    )
    return filename
