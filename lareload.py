"""
reload PACKAGE
"""
# import importlib

from logzero import logger

PACKAGE = "light_aligner"


def lareload(func, modname=None):  # modnmae: modname.py
    """
    exec( myreload( 'module') )  # note the quotes
    reload(import, imp.reload, from import *) modename
    """

    if modname is None:
        modname = func

    assert isinstance(modname, str) and isinstance(func, str), " Supply a string"

    modname = f"{PACKAGE}.{modname}"

    execline = "\nimport importlib\n"
    execline += "import " + modname
    execline += "\nimportlib.reload(" + modname
    execline += ")\nfrom " + modname
    execline += " import " + func

    # print(execline)
    logger.info("%s", execline)

    return execline
