""" para list to sent list. """
from typing import List, Optional, Union

from pathlib import Path
import numpy as np
import pandas as pd

from polyglot.text import Text, Detector

from logzero import logger

from light_aligner.align_sents import align_sents


# fmt: off
def plist_to_slist(  # pylint: disable=too-many-arguments
        plist: Union[str, np.array, List[List[Union[float, str]]]],
        lang1: Optional[str] = None,  # left col lang
        lang2: Optional[str] = None,  # right col lang
) -> List[List[str]]:
    # fmt: on
    """ para list to sent list.

    TODO: combine vs repeat (current implementation)
    """

    # lines with TAB separated, take first three columns only
    if isinstance(plist, str):
        text = plist[:]
        _ = [elm.strip() for elm in text.splitlines() if elm.strip()]

        plist = [elm.split("\t")[:3] for elm in _ if len(elm.split("\t")) > 2]  # pylint: disable=len-as-condition
        if not len(plist):
            logger.error(" %s does not appear to be properly formatted", text[:100])
            raise Exception("Invalid data")

    plist = np.asarray(plist)
    # use the first three columns
    assert plist.shape[1] > 2, "Invalid data"  # type: ignore
    shape = np.asarray(plist).shape

    # if not np.all(plist): raise Exception("Empty plist")

    if not lang1:
        _ = str("\n".join(plist[:, 0]))  # type: ignore
        try:
            lang1 = Detector(_).language.code
        except Exception as exc:
            logger.warning("Detector exc: %s", exc)
            lang1 = None
    if not lang2:
        _ = "\n".join(plist[:, 1])  # type: ignore
        try:
            lang2 = Detector(_).language.code
        except Exception as exc:
            logger.warning("Detector exc: %s", exc)
            lang2 = None
    # record valid rows with numerical positive valud in the 3rd column
    locs = []
    for idx, elm in enumerate(plist[:, 2]):  # type: ignore
        try:
            score = float(elm)
        except ValueError:
            continue
        if score > 0:
            locs.append(idx)
    if not locs:  # empty
        logger.warning(" the score column (3rd col) does not contain any valid value, something is probably wrong. We proceed nevertheless. ")

    curr_pos = shape[0]  # type: ignore
    if len(locs) / curr_pos < 0.2:
        logger.warning("Only about %.2f%% of the paras are aligned with certain confidence, sent level alignment quality will likely be poor.", len(locs) / curr_pos * 100)

    # collect aligned sent pairs
    sents_pair = []

    # handle possible rows before the first row with 3rd col equal to valid postive value
    if locs:
        curr_pos = locs[0]
    left = "\n".join(plist[:, 0][:curr_pos]).strip()  # type: ignore
    right = "\n".join(plist[:, 1][:curr_pos]).strip()  # type: ignore

    def align(left: str, right: str) -> List[str]:
        # possibly empty
        # insert \n after ;
        left = left.replace(";", ";\n")
        right = right.replace(";", ";\n")

        try:
            sents1 = [str(elm) for elm in Text(left, lang1).sentences]
        except ValueError:
            sents1 = [left.strip()]
        try:
            sents2 = [str(elm) for elm in Text(right, lang2).sentences]
        except ValueError:
            sents2 = [right.strip()]

        try:
            _ = align_sents(sents1, sents2, lang1, lang2)
        except Exception as exc:
            logger.warning(" align_sents exc: %s, something is wrong. There is nothing realy we can do but to deliver the orginal.", exc)
            _ = [[left, right]]
        return _  # type: ignore

    if left or right:  # no update if both empty
        sents_pair.extend(align(left, right))

    # handle the rest (the middle)
    # idx = 5; elm = locs[idx]
    for idx, elm in enumerate(locs[1:], 1):
        _ = "\n".join(plist[:, 0][locs[idx-1]:elm]).strip()  # type: ignore
        left = _
        right = "\n".join(plist[:, 1][locs[idx-1]:elm]).strip()  # type: ignore
        try:
            _ = align(left, right)
        except Exception as exc:
            logger.warning(" align (middle) exc: %s, deliver the original", exc)
            _ = [[left, right]]
        sents_pair.extend(_)

    # last entry
    _ = plist[:, 0][locs[-1]].strip()  # type: ignore
    left = _
    right = plist[:, 1][locs[-1]].strip()  # type: ignore
    try:
        _ = align(left, right)
    except Exception as exc:
        logger.warning(" align (middle) exc: %s, deliver the original", exc)
        _ = [[left, right]]
    sents_pair.extend(_)

    # possible tail
    if shape[0] > locs[-1]:
        _ = "\n".join(plist[:, 0][locs[-1] + 1:]).strip()  # type: ignore
        left = _
        right = "\n".join(plist[:, 1][locs[-1] + 1:]).strip()  # type: ignore
        try:
            _ = align(left, right)
        except Exception as exc:
            logger.warning(" align (middle) exc: %s, deliver the original", exc)
            _ = [[left, right]]
        sents_pair.extend(_)
    # return [["", "x"], ["a", "b"]]
    return sents_pair


def test1():
    """ plist_to_slist test1. """

    filepath = "data/test-plist_to_slist.xlsx"
    df_ = pd.read_excel(Path(filepath).read_bytes(), header=None)
    df_.replace(np.nan, "", inplace=True)
    plist = df_.to_numpy()
    res = plist_to_slist(plist)
    assert "Chapter" in str(res[0])
    assert "三章" in str(res[0])
    assert len(res) > 300

    assert "kitten" in str(res[-1])
    assert "小猫" in str(res[-1])
