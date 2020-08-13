"""
load_paras
"""

from typing import List

from pathlib import Path
import chardet

from logzero import logger


def load_paras(filepath: str) -> List[str]:
    """
    load paras
    """

    try:
        text = Path(filepath).read_text("utf-8")
    except Exception as exc:
        logger.warning("Path read_text('utf-8') exc: %s", exc)
        try:
            text = Path(filepath).read_text("gbk")
        except Exception as exc:  # pylint: disable=try-except-raise
            logger.warning("Path read_text('gbk') exc: %s", exc)
            _ = chardet.detect(Path(filepath).read_bytes()[:5000])
            encoding = _.get("encoding", "utf8")
            try:
                text = Path(filepath).read_text(encoding)
                logger.info("Successfully loaded with encoding %s", encoding)
            except Exception:  # pylint: disable=try-except-raise
                raise

    return [elm.strip() for elm in text.split("\n") if elm.strip()]
