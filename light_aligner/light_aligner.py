"""
    light version of light_aligner

    refer to light_aligner.light_aligner.py
"""

from typing import List, Optional, Tuple, Union

import numpy as np
from threading import currentThread

import logzero
from logzero import logger

# from light_aligner.light_corr import light_corr

from light_aligner.light_scores import light_scores

from light_aligner.text_to_paras import text_to_paras

from light_aligner.find_aligned_pairs import find_aligned_pairs
from light_aligner.gen_row_alignment import gen_row_alignment


# fmt: off
def light_aligner(  # pylint: disable=too-many-locals
        src_text: Union[list, str],
        tgt_text: Union[list, str],
        cos_mat: Optional[np.ndarray] = None,  # score matrix from light_scores
        thr: Optional[float] = None,  # 1/1.618, golden radio = 1.618
        tol: int = 4,
        debug: Optional[bool] = False,
) -> List[Tuple[str, str, float]]:
    # fmt: on
    """ light aligner
    if thr is None: set to
        3 * np.mean(cos_mat)  # (3 * av_corr)

    adopted from bee_aligner
    refer also to bert_aligner
    in pypi-projects\bert_aligner
    """

    # for GUI in check_thread_update
    c_th = currentThread()

    # convert str to list
    if isinstance(src_text, str):  # pragma: no cover
        src_text = text_to_paras(src_text)
    if isinstance(tgt_text, str):  # pragma: no cover
        tgt_text = text_to_paras(tgt_text)

    if not isinstance(src_text, list):  # pragma: no cover
        raise SystemExit(f'[{__file__}]: src_text [{type(src_text)}] is not a list, exiting...')
    if not isinstance(tgt_text, list):  # pragma: no cover
        raise SystemExit(f'[{__file__}]: tgt_text [{type(tgt_text)}] is not a list, exiting...')

    logger_level = logger.level
    if debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    # if cos_mat not supplied, calculate it on spot
    # and cached to bee_aligner.cos_mat
    if cos_mat is None:
        # cos_mat = bee_corr(src_text, tgt_text)
        cos_mat = light_scores(src_text, tgt_text)

    src_len = len(src_text)
    tgt_len = len(tgt_text)

    # set default to 3 * av_correlation
    if thr is None:
        # thr = 3 * sum(sum(cos_mat)) / cos_max.size
        thr = 1.1 * np.mean(cos_mat)

        # make sure it's not too big
        if thr > 1 / 1.618:
            thr = 1 / 1.618

    logger.debug(' %s', '  Doing some more processing... find_aligned_pairs')
    t_set, _ = find_aligned_pairs(
        cos_mat,
        thr=thr,
        tol=tol,
        matrix=True)

    logger.debug(' %s', '  Hold on...gen_row_alignment')
    resu = gen_row_alignment(t_set, src_len, tgt_len)
    para_list = []

    # for idx in range(len(resu)):
    for idx, _ in enumerate(resu):
        idx0, idx1, idx2 = resu[idx]  # pylint: disable=invalid-name
        # out = ['' if idx0 == '' else src_text[int(idx0)], '' if idx1 == '' else tgt_text[int(
        out = ('' if idx0 == '' else src_text[int(idx0)], '' if idx1 == '' else tgt_text[int(
            idx1)], '' if idx2 == '' else f'{float(idx2):.2f}')
        para_list.append(out)

    c_th.para_list = para_list  # type: ignore

    # restore logger loglevel
    logzero.loglevel(logger_level)
    return para_list
