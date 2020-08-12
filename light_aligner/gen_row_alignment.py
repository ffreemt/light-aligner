"""Gen proper alignment for a given triple_set


    src_txt = 'data/wu_ch2_en.txt'
    tgt_txt = 'data/wu_ch2_zh.txt'

    assert Path(src_txt).exists()
    assert Path(tgt_txt).exists()

    src_text, _ = load_paras(src_txt)
    tgt_text, _ = load_paras(tgt_txt)

    cos_matrix = gen_cos_matrix(src_text, tgt_text)
    t_set, m_matrix = find_aligned_pairs(cos_matrix0, thr=0.4, matrix=True)

    resu = gen_row_alignment(t_set, src_len, tgt_len)
    resu = np.array(resu)

    idx = -1
    idx += 1; (resu[idx], src_text[int(resu[idx, 0])], tgt_text[int(resu[idx, 1])]) if all(resu[idx]) else resu[idx]

    idx += 1;  i0, i1, i2 = resu[idx]; '***' if i0 == '' else src_text[int(i0)], '***' if i1 == '' else tgt_text[int(i1)], '' if i2 == '' else i2

"""
import logging
import pickle
import numpy as np

# from bee_aligner.zip_longest_middle import zip_longest_middle
# from bee_aligner.find_aligned_pairs import find_aligned_pairs
from light_aligner.zip_longest_middle import zip_longest_middle
from light_aligner.find_aligned_pairs import find_aligned_pairs

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# print('Will [gen_row] be rerun?')


def gen_row_alignment(  # pylint: disable=too-many-locals
        t_set,
        src_len,
        tgt_len,
):
    """gen proper rows for given triple_set

    Arguments:
        [t_set {np.array or list}] -- [nll matrix]
        [src_len {int}] -- numb of source texts (para/sents)
        [tgt_len {int}] -- numb of target texts (para/sents)
    Returns:
        [np.array] -- [proper rows]
    """

    t_set = np.array(t_set, dtype='object')

    # len0 = src_len

    # len1 tgt text length, must be provided
    len1 = tgt_len

    # rearrange t_set as buff in increasing order
    buff = [[-1, -1, '']]  #
    idx_t = 0
    for elm in t_set:
        elm = t_set[idx_t]
        LOGGER.debug('%s, %s', idx_t, elm)

        # find loc to insert
        elm0, elm1, elm2 = elm
        for idx, loc in enumerate(buff):
            if loc[0] > elm0:
                break
        else:
            idx += 1  # last

        # make sure elm1 is within the range
        # prev elm1 < elm1 < next elm1
        if elm1 > buff[idx - 1][1]:
            try:  # overflow possible (idx + 1 in # last)
                next_elm = buff[idx][1]
            except IndexError:
                next_elm = len1
            if elm1 < next_elm:
                # insert '' if necessary
                # using zip_longest_middle
                buff.insert(idx, [elm0, elm1, elm2], )
                # LOGGER.debug('---')

        idx_t += 1
        # if idx_t == 24:  # 20:
        #     break

    # remove [-1, -1]
    # buff.pop(0)
    # buff = np.array(buff, dtype='object')

    # take care of the tail
    buff += [[src_len, tgt_len, '']]

    resu = []
    # merit = []

    for idx, elm in enumerate(buff[1:]):
        idx1 = idx + 1
        elm0_, elm1_, elm2_ = buff[idx1 - 1]  # idx starts from 0
        elm0, elm1, elm2 = elm
        del elm2_, elm2

        tmp0 = zip_longest_middle(
            list(range(elm0_ + 1, elm0)),
            list(range(elm1_ + 1, elm1)),
            fillvalue='',
        )
        # convet to list entries & attache merit
        tmp = [list(t_elm) + [''] for t_elm in tmp0]

        # update resu
        resu += tmp + [buff[idx1]]

    # remove the last entry
    return resu[:-1]

def test_wuch2():
    """test wuch2"""

    filename = 't_set99_wuch2.pkl'
    with open(filename, 'rb') as fhandle:
        tset_ch2 = pickle.load(fhandle)

    resu = gen_row_alignment(tset_ch2, 99, 106)

    assert len(resu) >= 99, 'should be larger than 99'

    assert all(np.isclose(resu[0], [0, 0, -0.0062533836]))

    entry = ['', 5, '']
    idx = resu.index(entry)
    resu_ = resu[idx]
    assert all([elm == resu_[idx] for idx, elm in enumerate(entry)])

    entry = ['', 95, '']
    idx = resu.index(entry)
    resu_ = resu[idx]
    assert all([elm == resu_[idx] for idx, elm in enumerate(entry)])

    assert all(np.isclose(resu[-1], [98, 105, -3.1654365])), (np.array(resu).shape, resu[-1])


def test_wuch1():
    """test wuch1"""

    filename = 'nll_matrix_wuch1.pkl'
    with open(filename, 'rb') as fhandle:
        nll_matrix_ch1 = pickle.load(fhandle)

    # old gen_nllmatrix
    nll_matrix_ch1 = nll_matrix_ch1.T

    assert nll_matrix_ch1.shape == (30, 33)

    tset_ch1 = find_aligned_pairs(nll_matrix_ch1)
    src_len, tgt_len = nll_matrix_ch1.shape
    resu_ch1 = gen_row_alignment(tset_ch1, src_len, tgt_len)

    assert len(resu_ch1) >= src_len, 'should be larger than 99'

    assert all(np.isclose(resu_ch1[0], [0, 0, -0.02035301]))

    assert all(np.isclose(resu_ch1[-2], [28, 31, -0.020703452]))

    entry = [29, 32, '']
    idx = resu_ch1.index(entry)
    resu_ = resu_ch1[idx]
    assert all([elm == resu_[idx] for idx, elm in enumerate(entry)])

    # assert False, resu_ch1

    # entxt = 'wu_ch1_en.txt'
    # zhtxt = 'wu_ch1_zh.txt'
    # en = load_paras(r'data\\' + entxt)
    # zh = load_paras(r'data\\' + zhtxt)
    # for elm in resu_ch1:
    #     print('\n', en[0][elm[0]] if elm[0] else '')
    #     print(zh[0][elm[1]] if elm[1] else '', elm[2])

def test_wuch1a():
    """test wuch1a find_aligned_pairs(nll_matrix_ch1, numb=30)"""

    filename = 'nll_matrix_wuch1.pkl'
    with open(filename, 'rb') as fhandle:
        nll_matrix_ch1 = pickle.load(fhandle)

    # old gen_nllmatrix
    nll_matrix_ch1 = nll_matrix_ch1.T

    assert nll_matrix_ch1.shape == (30, 33)

    src_len, tgt_len = nll_matrix_ch1.shape
    tset_ch1 = find_aligned_pairs(nll_matrix_ch1, numb=src_len)
    resu_ch1 = gen_row_alignment(tset_ch1, src_len, tgt_len)

    assert len(resu_ch1) >= src_len, 'should be larger than 99'

    assert all(np.isclose(resu_ch1[0], [0, 0, -0.02035301]))
    assert all(np.isclose(resu_ch1[-2], [28, 31, -0.020703452]))

    entry = ['', 25, '']
    idx = resu_ch1.index(entry)
    resu_ = resu_ch1[idx]
    assert all([elm == resu_[idx] for idx, elm in enumerate(entry)])

    assert resu_ch1[27] == ['', 25, '']
    # assert False, resu_ch1

    # entxt = 'wu_ch1_en.txt'
    # zhtxt = 'wu_ch1_zh.txt'
    # en = load_paras(r'data\\' + entxt)
    # zh = load_paras(r'data\\' + zhtxt)
    # for elm in resu_ch1:
    #     print('\n', en[0][elm[0]] if elm[0] != '' else '')
    #     print(zh[0][elm[1]] if elm[1] != '' else '', elm[2])
