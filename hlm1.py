""" align hlm1
"""

from pathlib import Path

import tkinter as tk  # for messagebox.askyesnocancel

from logzero import logger

from light_aligner.read_text import read_text
from light_aligner.bingmdx_tr import bingmdx_tr
from light_aligner.suggest_udict_terms import suggest_udict_terms

from gen_userdict import gen_userdict


def test_hlm1():
    """ test hml ch1"""
    dest = r"data"
    path_en = Path(dest) / "wu_ch3_en.txt"
    path_zh = Path(dest) / "wu_ch3_zh.txt"

    path_en = Path(dest) / "hlm-ch1-en.txt"
    path_zh = Path(dest) / "hlm-ch1-zh.txt"

    text_en = "\n".join(elm.strip() for elm in read_text(path_en).splitlines() if elm.strip())
    text_zh = "\n".join(elm.strip() for elm in read_text(path_zh).splitlines() if elm.strip())

    paras_en = text_en.splitlines()
    paras_zh = text_zh.splitlines()

    root = tk.Tk()
    root.withdraw()

    try:
        ans = tk.messagebox.askyesnocancel(" Generate user dict template?", "A user dict may help improve alignment. Continue?")  # True False None
    except KeyboardInterrupt:
        ans = None

    extra_dict = {}
    if ans:  # Yes
        import os

        dir_path = Path(path_en).absolute().parent
        filepath = Path(dir_path) / "userdict.txt"
        templ_path = Path(dir_path) / f"{Path(path_en).stem}-userdict.txt"

        terms0, terms1 = suggest_udict_terms(text_en)
        cont = "\n".join([":".join(elm) for elm in terms0])
        cont += "\n" + "\n".join([":".join(elm) for elm in terms1])

        Path(templ_path).write_text(cont, encoding="utf-8")
        logger.info(" userdict tempalte wirtten to *%s*", templ_path)
        os.startfile(templ_path)

        try:
            reply = tk.messagebox.askyesnocancel(" Generate user dict template?", "Edit the file when it's opened and save in the same directory as userdict.txt. Continue?")
        except KeyboardInterrupt:
            reply = None

        if reply:
            extra_dict = text2udict(read_text(filepath))
            # print(read_text(filepath))
        else:
            logger.info(" OK, no userdict.txt used. Proceed as usual.")

    mat2 = light_scores(text_en, text_zh, extra_dict=extra_dict)

    # plt.figure(26); plt.contourf(mat2, levels=40, cmap="gist_heat_r")
    # sns.heatmap(mat2, linewidth=0.01)
    # plt.show()

    logger.info(" mean: %s", mat2.mean())

    assert mat2.mean() > 0.2


if __name__ == "__main__":
    test_hlm1()
