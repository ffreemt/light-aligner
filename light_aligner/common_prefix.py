"""
Get the common prefix
"""
from pathlib import Path
from itertools import takewhile


def common_prefix(strings):
    """Get common prefix

    >>> str_ = ['my_prefix_what_ever', 'my_prefix_what_so_ever', 'my_prefix_doesnt_matter']  # NOQA
    >>> common_prefix(str_)
    'my_prefix_'
    """
    if isinstance(strings, str):
        strings = strings.split()

    if not isinstance(strings, list):
        strings = list(strings)

    # if just one item, retrun itself, without the extra "_"
    if len(strings) == 1:
        elm = strings[0]
        # remove suffix if any
        elm = Path(elm)
        return str(elm).strip(elm.suffix)

    strings = [str(_) for _ in strings if _]
    c_prefix = "".join(
        c[0] for c in takewhile(lambda x: all(x[0] == y for y in x), zip(*strings))
    )
    if c_prefix:
        return c_prefix.strip("_") + "_"  # NOQA

    # if emptry c_prefix
    suff = Path(strings[0]).suffix
    return strings[0].strip(suff).strip("_") + "_"
