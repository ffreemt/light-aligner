"""
get the number of positive numbers in the third col
"""

from typing import List, Union

import numpy as np

from logzero import logger


# fmt: off
def check_anchors(
        pslist: Union[np.array, List[Union[float, str]]]
) -> int:
    # fmt: on
    """
    get the number of valid anchors (positive numbers in the third col)
    """

    try:
        arr = np.asarray(pslist)
    except Exception as exc:
        logger.error("Unable to convert to numpy array: %s, likely not valid input", exc)
        raise

    if arr.shape .__len__() < 2:
        logger.error(" Not in proper form: %s", arr.shape)
        raise Exception("Invalid input. shape: %s" % str(arr.shape))

    sum_ = 0
    for elm in arr:
        try:
            val = float(elm[2])
        except Exception:
            val = 0
        if val > 0:
            sum_ += 1

    return sum_
