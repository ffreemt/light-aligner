""" test load_xlsx. """

from pathlib import Path

from light_aligner.load_xlsx import load_xlsx
from light_aligner.check_anchors import check_anchors

from logzero import logger


def test_load_xlsx_check_anchors_1():
    """ test load_xlsx 1. """
    filepath = r"data/hlm-ch1-_-p.xlsx"
    res = load_xlsx(filepath, anchors=anchors)
    assert res.shape == (151, 3)

    assert check_anchors(res) == 30
