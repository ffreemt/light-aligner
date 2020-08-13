""" suggest a sensible tolerance for a matrix and coverage-rate (default 0.6).
"""

from typing import Optional

import numpy as np
from tqdm import trange
from logzero import logger

from .coverage_rate import coverage_rate


# fmt: off
def suggest_tolerance(
        mat: np.ndarray,
        c_rate: float = 0.66,
        limit: Optional[int] = None,
) -> int:
    # fmt: on
    """ suggest a sensible tolerance for a matrix and coverage-rate (default 0.66).
    """

    mat = np.asarray(mat)

    try:
        _, col = mat.shape
    except Exception as exc:
        logger.erorr(exc)
        raise

    if limit is None:
        limit = max(col // 2, 6)

    tolerance = 3
    if coverage_rate(mat, tolerance) >= c_rate:
        return tolerance

    # may try binary tree to speed up
    for tol in trange(tolerance + 1, limit + 1):
        _ = coverage_rate(mat, tol)
        if _ >= c_rate:
            logger.info(" search succeeded for mat of size %s", mat.size)
            return tol
    logger.warning(" mat of size %s most likely not a score matrix", mat.shape)
    logger.waning(" we searched hard but were unable to find a sensible tolerance, setting to max(half of %s, 6): %s", col, max(col // 2, 6))

    return max(col // 2, 6)
