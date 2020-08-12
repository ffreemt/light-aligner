r""" text (: or TAB separate) to dict(userdef: 1 )
    takes only te first delimter if more than one exist
    discard the line if no delimiter exists.
"""

from typing import Optional, Dict

# from pathlib import Path
import re

# from light_aligner.read_text import read_text


# def text2udict(text: str, delim: Optional[str] = None):
def text2udict(text: str, delim: Optional[str] = None) -> Dict[str, Dict[str, str]]:
    r"""
    text (: or TAB separate) to {{"a": {"userdef": "def"}}, {"b": {"userdef": "def"}}}, text.splitlines() sep lines

    >>> text2udict(" a: b\n a")
    {'a': {'userdef': 'b'}}
    >>> text2udict(" a:: b\n a")
    {'a': {'userdef': 'b'}}
    >>> text2udict(" a\t b\n \n a")
    {'a': {'userdef': 'b'}}
    >>> text2udict(" a\t b\n \n c:d")
    {'a': {'userdef': 'b'}, 'c': {'userdef': 'd'}}
    """

    if delim is None:
        delim = ":\t"

    patt = re.compile("[" + re.escape(delim) + "]+")
    # patt = re.compile("[" + ":\t" + "]+")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    two_tuples = [patt.split(elm, 2) for elm in lines]

    # remove lines not containing delim
    two_tuples = [elm for elm in two_tuples if len(elm) > 1]

    # remove empty entries
    two_tuples = [
        [elm[0].strip(), elm[1].strip()]
        for elm in two_tuples
        if elm[0].strip() and elm[1].strip()
    ]

    dict_ = dict()
    for elm in two_tuples:
        dict_.update({elm[0]: {"userdef": elm[1]}})

    return dict_
