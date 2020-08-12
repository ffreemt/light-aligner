"""
suggest userdict terms.

"""

from typing import Tuple, List, Union

from textblob import TextBlob
from yaspin import yaspin
from linetimer import CodeTimer

from logzero import logger

from light_aligner.bingmdx_tr import bingmdx_tr, MDX_DICT  # ,EHWD
from light_aligner.read_text import read_text


# fmt: off
def suggest_udict_terms(
        text: Union[str, List[str]],
        silent: bool = False,
        spinner: bool = True,
# ) -> List[str]:
) -> Tuple[List[str], List[str]]:
    # fmt: on
    """
    suggest userdict terms.

    >>> filename = "data/hlm-ch1-en.txt"
    >>> text = read_text(filename)
    >>> len_ = len(suggest_udict_terms(text, True, False)[0])
    >>> len_
    54
    """
    if isinstance(text, list):
        try:
            text = " ".join(text)
        except Exception as exc:
            logger.error("%s", exc)

    text_= "Processing... takes a few secs for short text..."
    if silent:
        text_ = ""

    # with yaspin(text=text_):
    # if True:

    terms0, terms1 = [], []
    def doit():
        nonlocal terms0, terms1

        with CodeTimer(unit="s", silent=silent):
            # terms = set([word for word, tag in TextBlob(read_text(filename)).tags if tag in ["NNP"]])
            terms = set([word for word, tag in TextBlob(text).tags if tag in ["NNP"]])

            # terms = [term for term in terms if term.lower() not in EHWD]
            # terms = [term for term in terms if term.lower() == bingmdx_tr(term.lower())]

            terms0 = []  # NNP terms that do not appear in bingmdx_tr
            terms1 = []  # NNP terms already in bingmdx_tr
            for term in terms:
                # _ = bingmdx_tr(term.lower())
                # if term.lower() == _:

                _ = MDX_DICT.get(term.lower())
                if _ is not None:
                    _ = _.get("n")  # "n" => "NNP"

                if _ is None:
                    terms0.append([term, ""])
                else:
                    terms1.append([term, _])
    if spinner:
        with yaspin(text=text_):
            doit()
    else:
        doit()

    return sorted(terms0, key=lambda x: x[0]), sorted(terms1, key=lambda x: x[0])
