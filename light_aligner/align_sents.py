""" align sents. """

from typing import List, Tuple, Optional, Union

import numpy as np
import pandas as pd
from pathlib import Path
from polyglot.text import Text, Detector
from nltk.translate.gale_church import align_blocks

from logzero import logger

from light_aligner.zip_longest_middle import zip_longest_middle


# fmt: off
def align_sents(
        text1: Union[List[str], str],
        text2: Union[List[str], str],
        lang1: Optional[str] = "",
        lang2: Optional[str] = "",
) -> List[Tuple[Union[int, str], Union[int, str]]]:
    # fmt: on
    """
    align sents.

    >> df = pd.read_excel(Path(filepath).read_bytes(), header=None)
    >> plist = df.to_numpy()
    >> text1 = [str(elm) for elm in Text(plist[4][0], 'en').sentences]
    >> text2 = [str(elm) for elm in Text(plist[4][1], 'zh').sentences]
    >> res = align_sents(text1, text2)
    >> res[0]
    (0, 0)
    >> res[-2]
    (6, 9)
    """
    def convert_text(text: str, lang=""):
        if not lang:
            try:
                lang = Detector(text, True).language.code
            except Exception as exc:
                logger.error(" Detector exc: %s", exc)
                lang = None
        try:
            _ = [str(elm) for elm in Text(text, lang).sentences]
        except ValueError:
            _ = [text.strip()]
        except Exception as exc:
            logger.error("polyglot.Text %s", exc)
            _ = [text.strip()]
        return _

    if isinstance(text1, str):
        text1 = convert_text(text1, lang1)
    if isinstance(text2, str):
        text2 = convert_text(text2, lang2)

    if not lang1:
        try:
            lang1 = Detector(" ".join(text1), True).language.code
        except Exception as exc:
            logger.error("%s", exc)
            raise
    if not lang2:
        try:
            lang2 = Detector(" ".join(text2), True).language.code
        except Exception as exc:
            logger.error("%s", exc)
            raise
    len1_list = [len(Text(sent.strip(), lang1).words) for sent in text1 if sent.strip()]
    len2_list = [len(Text(sent.strip(), lang2).words) for sent in text2 if sent.strip()]
    try:
        res = align_blocks(len1_list, len2_list)
    except Exception as exc:
        logger.error("align_blocks exc: %s", exc)
        # fall back
        _1 = range(len(len1_list))
        _2 = range(len(len2_list))
        res = zip_longest_middle([*_1], [*_2], "")

    # return [(1, 2), (0, 1), ("", 2)]
    # return res

    # align_blocks return empty []
    if not res:
        return np.asarray(zip_longest_middle(text1, text2, ""))

    # assemble sent pairs
    pairs = []
    for elm in res:
        try:
            left = text1[elm[0]]
        except TypeError: # leave as ""
            left = ""
        try:
            right = text2[elm[1]]
        except TypeError: # leave as ""
            right = ""
        pairs.append([left, right])
    return pairs


def test1():
    """ align sents test1. """

    filepath = "data/test-plist_to_slist.xlsx"
    df = pd.read_excel(Path(filepath).read_bytes(), header=None)
    plist = df.to_numpy()
    text1 = [str(elm) for elm in Text(plist[4][0].replace(";", ";\n"), 'en').sentences]
    text2 = [str(elm) for elm in Text(plist[4][1], 'zh').sentences]
    res = align_sents(text1, text2)
    # assert res[0] == (0, 0)
    # assert res[-2] == (6, 9)


def test_extreme_case1():
    """ align sents test1. """
    text1 = "Chapter 3"
    text2 = ""
    res = align_sents(text1, text2)
    assert res[0][0] == "Chapter 3"
    assert res[0][1] == ""
