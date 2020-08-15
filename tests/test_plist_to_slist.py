""" test plist_to_slist. """

from pathlib import Path
import numpy as np
import pandas as pd
from light_aligner.load_xlsx import load_xlsx
from light_aligner.plist_to_slist import plist_to_slist


def test_plist_to_slist1():
    """ test_plist_to_slist1. """
    filepath = "data/test-plist_to_slist.xlsx"
    df = pd.read_excel(Path(filepath).read_bytes(), header=None)
    df.replace(np.nan, "", inplace=True)

    plist = df.to_numpy()
    slist = plist_to_slist(plist)

    assert "Chapter" in slist[0][0]
    assert "章" in slist[0][1]

    assert "In fact" in slist[10][0]
    assert "事实上" in slist[10][1]


def test_plist_to_slist2():
    """ test_plist_to_slist1. """
    filepath = "data/Gatsby-200lines-dual.xlsx"
    df = load_xlsx(filepath)

    plist = df.to_numpy()
    slist = plist_to_slist(plist)

    assert "截然不同" in slist[-3][0]
    assert "sharply different" in slist[-3][1]

    assert not slist[-2][0]  # empty
    assert "uncivilized" in slist[-2][1]
