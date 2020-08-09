""" test w4w_to_zh
"""

from light_aligner.w4w_to_zh import w4w_to_zh


def test_sanity():
    """ test sanity. """
    assert w4w_to_zh("test")
