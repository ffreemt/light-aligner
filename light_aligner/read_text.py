""" read text """

from typing import Union

from pathlib import Path

try:
    import cchardet as chardet
except (ModuleNotFoundError, ImportError):
    import chardet

from logzero import logger


def read_text(filename: Union[str, Path]) -> str:
    """ read text from a file """

    if not Path(filename).exists():
        raise Exception(f" **{filename}** does not exist")

    try:
        encoding = chardet.detect(Path(filename).read_bytes()[:5000]).get("encoding")
        return Path(filename).read_text(encoding, errors="ignore")
    except Exception as exc:
        logger.error("exc: %s", exc)

    try:
        text = Path(filename).read_text("utf-8")
    except Exception as exc:
        logger.error("exc: %s", exc)
        raise
    return text
