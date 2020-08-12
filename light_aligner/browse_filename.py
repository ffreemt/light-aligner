'''
browse to a file

https://pythonspot.com/tk-file-dialogs/
filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
'''
# import sys
from pathlib import Path


from tkinter import filedialog, Tk


def browse_filename(
    initialdir=Path.cwd(),
    title="Select a file",
    filetypes=(
        ("text files", "*.txt"),
        # ("gzip files", "*.gz"),
        # ("bzip2 files", "*.bz2"),
        ("all files", "*.*"),
    )
):
    ''' browse for a filename'''
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        parent=root,
        initialdir=initialdir,
        title=title,
        filetypes=filetypes,
    )
    return filename
