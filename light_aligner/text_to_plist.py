""" convert text to p_list, given a two-tuple langs, e.g., ['en', 'zh'].

adopted from bee_aligner.text_to_plist
    bee_corr -> light_scores

based on bumblebee-aligner/data/proc_gatsby.py

from diskcache import FanoutCache

# cache = FanoutCache("diskcache")

# @cache.memoize(typed=True, expire=36000, tag='func')
def func():
    ...
"""

from typing import List, Optional, Union

import numpy as np
from itertools import zip_longest
from threading import currentThread

import langid
# import blinker
from polyglot.text import Detector
# from diskcache import FanoutCache

from logzero import logger

# import bee_aligner
# from bee_aligner.bee_corr import bee_corr
# from bee_aligner.single_or_dual import single_or_dual

from light_aligner.light_scores import light_scores
from light_aligner.single_or_dual import single_or_dual


# SIG_TABLE = blinker.signal("table")
# cache = FanoutCache("diskcache")  # pylint: disable=invalid-name
# cache.clear()

# fmt: off
# @cache.memoize(typed=True, expire=36000, tag='text_to_plist')
def text_to_plist(
        text_dual: Union[str, List[str]],
        langs: Optional[List[str]] = None,
) -> List[str]:
    # fmt: on
    """ convert text_dual to p_list, given a two-tuple langs, e.g., ['en', 'zh'].
    """

    c_thr = currentThread()

    if isinstance(text_dual, list):
        text_dual = "\n".join(text_dual)

    if langs is None:
        # langs = ['en', 'zh']
        langs = single_or_dual(text_dual)

    langid.set_languages(langs)

    # polyglot.Detector not in langs, use langid.classify

    # remove "\u3000"
    paras = [elm.strip() for elm in text_dual.replace("\u3000", " ").splitlines() if elm.strip()]

    if len(langs) == 1:
        _ = [*zip_longest(paras, [""], [""], fillvalue="")]
        c_thr.p_list = _
        return _

    # with timeme():  # 2094 ms
    langs_info = []
    for para in paras:
        lang = Detector(para, True).language.code
        if lang not in langs:
            lang = langid.classify(para)[0]
        langs_info.append(lang)

    if len(langs_info) < 2:
        logger.warning("langs_info: %s, nothing to separate, returning original text as the first column with two empty columns", langs_info)

        _ = [*zip_longest(paras, "", "", fillvalue="")]
        c_thr.p_list = _
        return _

    binary_info = [1]
    for idx, elm in enumerate(langs_info[1:], 1):
        if elm == langs_info[idx - 1]:
            binary_info.append(0)
        else:
            binary_info.append(1)

    left = []
    right = []
    l_or_r = 1
    for idx, para in enumerate(paras):
        if binary_info[idx]:
            # switch
            l_or_r = (l_or_r + 1) % 2
            if l_or_r:  # right
                right.append([])
            else:
                left.append([])
        if l_or_r:  # right
            right[-1].append(para)
        else:
            left[-1].append(para)

    left = ["\n".join(elm) for elm in left]
    right = ["\n".join(elm) for elm in right]

    _ = 5
    # corr0 = bee_aligner.bee_corr.bee_corr(left[1: _ + 1], right[:_]).diagonal()  # skip possible junk at the beginning
    # corr1 = bee_aligner.bee_corr.bee_corr(left[1: _ + 1], right[1:_ +1]).diagonal()

    # corr0 = bee_corr(left[1: _ + 1], right[:_]).diagonal()  # skip possible junk at the beginning
    # corr1 = bee_corr(left[1: _ + 1], right[1:_ +1]).diagonal()

    corr0 = light_scores(left[1: _ + 1], right[:_]).diagonal()  # skip possible junk at the beginning
    corr1 = light_scores(left[1: _ + 1], right[1:_ +1]).diagonal()

    if np.sum(corr0) > np.sum(corr1):
        p_list = [*zip_longest(left, [''] + right, fillvalue='')]
    else:
        p_list = [*zip_longest(left, right, fillvalue='')]

    _ = p_list[:]
    p_list = []
    for para in _:
        len0, len1 = len(para[0]), len(para[1])
        if len0 > 20 * len1 or len1 > 20 * len0:
            entry = [para[0], para[1], '']
        else:
            entry = [para[0], para[1], '0.66']
        p_list.append(entry)

    # logger.info(" update table via SIG_TABLE.send(df=p_list)")
    # SIG_TABLE.send("text_to_plist", df=p_list)

    c_thr.p_list = p_list  # type: ignore

    return p_list
