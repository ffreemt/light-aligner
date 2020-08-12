""" calculate coverage rate for tolerance and np matrix """

# from typing import Union

import numpy as np

from logzero import logger


def coverage_rate(mat: np.ndarray, tolerance: float = 6) -> float:
    """
    calculate coverage rate for tolerance and np matrix
    """

    try:
        mat = np.asarray(mat).copy()
    except TypeError:
        logger.error(" Unable to cnovert to np.asarray ")
        raise

    mat_min = mat.min()

    if mat.shape.__len__() == 1:
        mat = np.asarray([mat]).copy()

    row, col = mat.shape
    sfactor = col / row
    tot_coll = 0

    for idx in range(row):
        r, c = divmod(mat.argmax(), col)
        ideal_c = sfactor * r

        logger.debug("r: %s, c: %s", r, c)

        gap = abs(c - ideal_c)
        if gap <= tolerance:
            # reset rows
            mat[r] = 0
            # reset cols
            for jdx in range(row):
                mat[jdx, c] = 0
            tot_coll += 1
            logger.debug(" tot_coll: %s", tot_coll)
        else:
            mat[r, c] = mat_min

    return tot_coll / row


def main():
    """ main. """

    c_rate = coverage_rate([1])

    mat = np.asarray([[0, 1], [2, 3]])

    c_rate = coverage_rate(mat)
    print(c_rate)


if __name__ == "__main__":
    main()
