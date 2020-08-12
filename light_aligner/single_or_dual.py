""" determine sing lang or dual-lang of text."""

from typing import List, Union

from polyglot.text import Detector

from logzero import logger


def single_or_dual(text: Union[List[str], str], confidence: int = 30) -> List[str]:
    """ determine sing lang or dual-lang of text.

    paras = [elm.strip() for elm in text.split("\n") if elm.strip()]
    langs = [Detector(para, True).language.code for para in paras]
    _ = defaultdict(int)
    for lang in langs:
        _[lang] += 1
    sorted_tuple = sorted(_.items(), key=lambda item: -item[1])
    logger.info("detected these langs: %s", sorted_tuple)

    return sorted_tuple

    """
    if isinstance(text, list):
        text = " ".join(text)

    try:
        langs = Detector(text).languages  # quiet=True
    except Exception as exc:
        logger.error(" Detector(text): %s", exc)
        langs = []

    logger.info("detected langs:")
    for lang in langs:
        logger.info("\n\t %s", lang)

    if not langs:
        logger.warning("Unable to detect language, returning []")
        return []

    if langs[1].confidence < confidence:
        return [langs[0].code]
    return [langs[0].code, langs[1].code]
