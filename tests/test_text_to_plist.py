""" test text_to_plist. """

# from pathlib import Path

# from bee_aligner.text_to_plist import text_to_plist
# from bee_aligner.single_or_dual import single_or_dual

from light_aligner.text_to_plist import text_to_plist
from light_aligner.single_or_dual import single_or_dual
from light_aligner.read_text import read_text


def test_text_to_plist1():
    """ test_text_to_plist1.
    data/了不起的盖茨比The Great Gatsby 中英双语.txt
    """
    # text = Path(r"data/了不起的盖茨比The Great Gatsby 中英双语.txt").read_text("utf8")

    filepath = r"data\Gatsby-200lines-dual.txt"
    text = read_text(filepath)

    s_or_d = single_or_dual(text)
    res = text_to_plist(text, s_or_d)

    assert not res[0][2]  # "" empty
    assert res[-2][2] in ["0.66"]
    assert res[-3][2] in ["0.66"]


_ = '''
def test_text_to_plist5000():
    """ test_text_to_plist3.
    data/gatsby-dual-test1.txt
    """
    text = Path(r"data/了不起的盖茨比The Great Gatsby 中英双语.txt").read_text("utf8")[:5000]

    s_or_d = single_or_dual(text)
    res = text_to_plist(text, s_or_d)

    # just col-1 is not empty
    assert not res[0][2]  # "" empty
    assert not res[0][1]  # "" empty
    assert not res[-1][2]  # "" empty
# '''
