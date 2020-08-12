"""
gen word length vector
    text -> paras, text.splitlines()
    paras -> sents, Text(line).sentences
    sents -> words, Text(sent).words
    len(words)
"""

from typing import List, Optional, Union

from polyglot.text import Text


# fmt: off
def gen_wlength_vec(
        text: Union[str, List[str]],
        break_semicol: bool = True,
        hint_language_code: Optional[str] = None,
) -> List[int]:
    # fmt: on
    """
    gen word length vector
        text -> paras, text.splitlines()
        paras -> sents, Text(line).sentences
        sents -> words, Text(sent).words
        len(words)
    >>> gen_wlength_vec(r"a; b\c")
    [2, 3]
    gen_wlength_vec(r"a; b\c")
    """

    if isinstance(text, list):
        text = "\n".join(text)

    if break_semicol:
        text = text.replace(";", ";\n")

    sents = Text(text, hint_language_code=hint_language_code).sentences
    # sents_w = [sent.words for sent in sents]
    return [len(sent.words) for sent in sents]
