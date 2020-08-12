"""
gal-church align
"""

from math import log
from pylab import polyfit
import scipy.stats
from scipy.stats import norm

form polyglot.text import Text

BEAD_COSTS = {
    (1, 1): 0,
    (2, 1): 230,
    (1, 2): 230,
    (0, 1): 450,
    (1, 0): 450,
    (2, 2): 440,
}


def length_cost(sx, sy, mean_xy, variance_xy):
    """
    Calculate length cost given 2 sentence. Lower cost = higher prob.

    The original Gale-Church (1993:pp. 81) paper considers l2/l1 = 1 hence:
    delta = (l2-l1*c)/math.sqrt(l1*s2)

    If l2/l1 != 1 then the following should be considered:
    delta = (l2-l1*c)/math.sqrt((l1+l2*c)/2 * s2)
    substituting c = 1 and c = l2/l1, gives the original cost function.
    """
    lx, ly = sum(sx), sum(sy)
    m = (lx + ly * mean_xy) / 2
    try:
        delta = (lx - ly * mean_xy) / math.sqrt(m * variance_xy)
    except ZeroDivisionError:
        return float("-inf")
    return -100 * (log(2) + norm.logsf(abs(delta)))


# def _align(x, y, mean_xy, variance_xy, bead_costs=BEAD_COSTS):
def _align(x, y, mean_xy):
    """
    The minimization function to choose the sentence pair with
    cheapest alignment cost.
    """
    variance_xy = 6.8
    bead_costs = BEAD_COSTS

    m = {}
    for i in range(len(x) + 1):
        for j in range(len(y) + 1):
            if i == j == 0:
                m[0, 0] = (0, 0, 0)
            else:
                m[i, j] = min(
                    (
                        m[i - di, j - dj][0]
                        + length_cost(
                            x[i - di : i], y[j - dj : j], mean_xy, variance_xy
                        )
                        + bead_cost,
                        di,
                        dj,
                    )
                    for (di, dj), bead_cost in bead_costs.items()  # type: ignore
                    if i - di >= 0 and j - dj >= 0
                )

    i, j = len(x), len(y)
    while True:
        (c, di, dj) = m[i, j]
        if di == dj == 0:
            break
        yield (i - di, i), (j - dj, j)
        i -= di
        j -= dj


# def sent_length(sentence):
    # """ Returns sentence length without spaces. """
    # return sum(1 for c in sentence if c != " ")


# def align(sx, sy, mean_xy=1, variance_xy=6.8, bc=BEAD_COSTS):
def gc_align(sx: str, sy: str, mean: float = 1, word_based: bool = True):
    """ Main alignment function.

    for Chinese, Korean, Japanese, use
    mean = text_en.replace(" ", "").__len__() / text_zh.__len__()
    ~2.3 (lover ch10)

    """
    # cx = [*map(sent_length, sx)]
    # cy = [*map(sent_length, sy)]

    variance_xy = 6.8
    bc = BEAD_COSTS
    mean_xy = mean


    if word_based:
        cx = [len(Text(elm).words) for elm in sx]  # word based
        cy = [len(Text(elm).words) for elm in sy]
    else:
        cx = [len(elm) for elm in sx]  # char based
        cy = [len(elm) for elm in sy]

    # for (i1, i2), (j1, j2) in reversed(list(_align(cx, cy, mean_xy, variance_xy, bc))):

    # if seq_pairs:
        # return reversed(list(_align(cx, cy, mean_xy)))

    for (i1, i2), (j1, j2) in reversed(list(_align(cx, cy, mean_xy))):
        yield " ".join(sx[i1:i2]), " ".join(sy[j1:j2])
