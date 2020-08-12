r"""find aligned pairs

Given: nll matrix: nll_matrix
Output: aligned pairs and confidence level

Refer to C:\dl\Dropbox\mat-dir\myapps\pytorch-nlp\rnn_embed\heatmap_nll.py
"""
import sys
import logging
# import inspect
import numpy as np
import pytest
import pickle

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

def find_aligned_pairs(  # pylint: disable=too-many-branches, too-many-locals
        nll_matrix,  # nll matrix/cos_mat
        thr=0.8,  #
        tol=4,
        numb=None,  # attempt to find numb pairs, overwrite thr
        matrix=False,  # if True, return t_set, prunned w_matrix
):
    """Find aligned pairs given an nll matrix

    Arguments:
        nll_matrix {[array]} -- [nll matrix]
        thr {[float]} -- [threhold, conf level >= thr]
        numb {integer} -- [numb of pairs to find, overwrite thr]
    Returns:
        [set] -- [triple: pair + conf level ]
    """

    # LOGGER.debug("Enter %s", inspect.stack()[0][3])
    w_matrix = np.copy(nll_matrix)

    min_ = w_matrix.min()
    tot_col = w_matrix.shape[1]
    tot_row = w_matrix.shape[0]
    sfactor = tot_col / tot_row
    # # delta = abs(tot_col - tot_row)
    # # delta = max(abs(tot_col - tot_row), 3)

    delta = 6
    delta = tol
    # delta_idx = max(2, int(idx/tot_row * delta))  # 2, 2...delta-1
    # col_idx = sfactor * idx  # 0...tot_col

    triple_set = []
    # LOGGER.debug('if numb is None:')

    if numb is None:  # use the thr
        while len(triple_set) < min(tot_row, tot_col):
            pair = divmod(w_matrix.argmax(), tot_col)
            max_ = w_matrix.max()

            if max_ < thr or max_ <= int(min_ / 2):
                break

            # check the pair falls within a band
            idx, col_idx = pair
            col_idx_exp = sfactor * idx
            # delta_idx = max(2, int(idx/tot_row * delta))
            delta_idx = max(2, round(0.5 + idx / tot_row * delta))
            # if int(abs(col_idx_exp - col_idx)) <= delta_idx:
            if int(abs(col_idx_exp - col_idx)) <= delta:
                triple_set += [list(pair) + [max_]]

                # reset columns
                for elm in range(tot_col):
                    w_matrix[idx, elm] = 0
                # reset rows
                for elm in range(tot_row):
                    w_matrix[elm, col_idx] = 0
            # reset in any case
            w_matrix[pair] = 0

        if matrix:
            return triple_set, w_matrix
        return triple_set

    # LOGGER.debug(' numb is None end ')
    # numb is None end

    # if numb is given (is not None): number of pairs to extract

    count = 0
    triple_set = []
    # break when idx > numb
    while len(triple_set) < min(tot_row, tot_col):
        pair = divmod(w_matrix.argmax(), tot_col)
        max_ = w_matrix.max()

        # skip if the entry is previously erased
        # or other smaller values
        if max_ > int(min_ / 2):
            # print(pair, max_)
            LOGGER.debug('pair: %s, max: %s', pair, max_)

            # check the pair falls within a band
            idx, col_idx = pair
            col_idx_exp = sfactor * idx
            # delta_idx = max(2, int(idx/tot_row * delta))
            delta_idx = max(2, round(0.5 + idx / tot_row * delta))  # noqa: F841
            # if int(abs(col_idx_exp - col_idx)) <= delta_idx:
            if int(abs(col_idx_exp - col_idx)) <= delta:
                triple_set += [list(pair) + [max_]]

            # erase just one cell
            w_matrix[pair] = int(min_ / 2)

        # make sure it exits
        count += 1
        if count >= numb or max_ <= int(min_ / 2):
            break

    return triple_set


def setup_module(module):
    print("setup_module module:%s" % module.__name__)


@pytest.fixture(scope='function')
def logging_setup():
    '''
    # def setup_module(function):
    setup module'''
    # print("setup_module function:%s" % function.__name__)
    print(" >>> logging_setup ")
    # http://pythontesting.net/framework/pytest/pytest-introduction/

    logging.basicConfig(
        format="\t> %(filename)s"
        " %(funcName)s"
        "-ln%(lineno)d"
        " %(levelname)s \n%(message)s",
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    logger = logging.getLogger()
    logger.info(' info ')

def test_wuch2_nllmatrix():
    ''' test wuch2 nllmatrix'''
    filename = r'nll_matrix_wuch2.pkl'
    with open(filename, 'rb') as fhandle:
        nll_matrix = pickle.load(fhandle)
    triple_set = find_aligned_pairs(nll_matrix)
    res = triple_set[0][0] if triple_set else None
    assert res == 6, 'Expected to be {}'.format(res)


# def test_wuch2_nllmatrix_numb10(logging_setup):
def test_wuch2_nllmatrix_numb10():
    ''' test wuch2 nllmatrix'''

    filename = r'nll_matrix_wuch2.pkl'
    with open(filename, 'rb') as fhandle:
        nll_matrix = pickle.load(fhandle)
    # triple_set = find_aligned_pairs(nll_matrix, numb=10)
    triple_set = find_aligned_pairs(nll_matrix, numb=10)
    res = triple_set[0][0] if triple_set else None
    assert res == 6, 'Expected to be {}'.format(res)
    # assert len(triple_set) == 10, 'Expected 10'
    assert len(triple_set) == 10, 'Expected 10'


def test_nll_matrix_wuch3glove100_flel_pkl():
    ''' test wuch2 nllmatrix'''

    filename = r'nll_matrix_wuch3glove100_flel.pkl'
    with open(filename, 'rb') as fhandle:
        nll_matrix = pickle.load(fhandle)
    src_len, tgt_len = nll_matrix.shape
    triple_set = find_aligned_pairs(nll_matrix, numb=max(src_len, tgt_len))
    res = triple_set[0][0] if triple_set else None
    assert res == 3, 'Expected to be {}'.format(res)
    # assert len(triple_set) == 44, 'Expected 44'
    assert len(triple_set) == 19, 'Expected 19'


def test_red_ch1():
    ''' test_red_ch1 '''

    filename = r'nll_matrix_redch1glove100_flel.pkl'
    with open(filename, 'rb') as fhandle:
        nll_matrix = pickle.load(fhandle)
    src_len, tgt_len = nll_matrix.shape
    triple_set = find_aligned_pairs(nll_matrix, numb=min(src_len, tgt_len))
    # 46, 31 (-4.46) ought to be 43, 31 (-1.66)

    res = triple_set[0][0] if triple_set else None
    assert res == 23, 'Expected to be {}'.format(res)
    assert len(triple_set) == 23, 'Expected 23'
    # assert triple_set[-6][:2] == (43, 31), 'ought to be (43, 31)'
    # [46, 34, -1.0531687]
    assert triple_set[-1][:2] == [46, 34], 'ought to be (46, 34)'


if __name__ == "__main__":

    logging.basicConfig(
        format="\t> %(filename)s"
        " %(funcName)s"
        "-ln%(lineno)d"
        " %(levelname)s \n%(message)s",
        level=logging.DEBUG,
        # stream=sys.stdout,
    )
    # logger = logging.getLogger()

    LOGGER.info("main info ")
    # test_wuch2_nllmatrix_numb10(logging_setup)
    test_wuch2_nllmatrix_numb10()
    # test_wuch2_nllmatrix()
