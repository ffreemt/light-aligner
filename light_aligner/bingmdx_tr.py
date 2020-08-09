r"""
BINGMDX: MDXDICT from w4w_to_en import MDXDICT
    C:\dl\Dropbox\mat-dir\pyqt\Sandbox\workpad\w4w_to_en\w4w_to_en\w4w_to_zh.py
"""

from typing import Dict, List, Union

from pathlib import Path

# import ujson as json
import msgpack
from textblob import TextBlob

# import logzero
from logzero import logger, setup_logger

from light_aligner.read_text import read_text

# from w4w_to_en import MDX_DICT, HWD
DIR_PATH = Path(__file__).parent

# DICT_FILE = Path(DIR_PATH, 'msbing_c_e.pkl')
# HWD_FILE = Path(DIR_PATH, 'msbing_c_e_hw.pkl')
# MDX_DICT = json.load(open(DICT_FILE))
# HWD = json.load(open(HWD_FILE))  # 26407
# msgpack.dump(MDX_DICT, open('light_aligner/msbing_c_e.msgpk', 'wb'))
# msgpack.dump(HWD, open('light_aligner/msbing_c_e_hw.msgpk', 'wb'))

DICT_FILE = Path(DIR_PATH, "msbing_c_e.msgpk")
HWD_FILE = Path(DIR_PATH, "msbing_c_e_hw.msgpk")
MDX_DICT = msgpack.load(open(DICT_FILE, "rb"))
HWD = msgpack.load(open(HWD_FILE, "rb"))  # Chinese header words in MSBING.mdx

# attempt to load userdict.txt if any
try:
    _ = Path(Path(DIR_PATH) / "userdict.txt")
    two_tuples = [  # pylint: disable=invalid-name
        elm.split(":", 2) for elm in read_text(_).splitlines() if elm.strip()
    ]
    # USERDICT = dict(two_tuples)  # type: Dict[str, str]
    # USERDICT = dict([elm[0], {"userdef": elm[1]}] for elm in two_tuples)  # type: Dict[str, Dict[str, str]]
    USERDICT = {}  # type: Dict[str, Dict[str, str]]
    for elm in two_tuples:
        USERDICT.update({elm[0]: {"userdef": elm[1]}})
except Exception as exc:
    logger.error(
        """ loading userdict.txt *%s* failed: %s, no userdict used""",
        Path(Path(DIR_PATH) / "userdict.txt"),
        exc,
    )
    USERDICT = {}
MDX_DICT.update(USERDICT)

map_tags = dict(  # pylint: disable=invalid-name
    [  # BlobText nltk.pos_tag to bingmdx
        ("CC", "conj"),
        ("CD", "num"),
        ("DT", "pron"),  # ("DT", "pron")?
        ("EX", ""),
        ("FW", ""),
        ("IN", "conj"),
        ("JJ", "adj"),
        ("JJR", "adj"),
        ("JJS", "adj"),
        ("LS", ""),
        ("MD", "modv"),
        ("NN", "n"),
        ("NNS", "n"),
        ("NNP", "n"),
        ("NNPS", "n"),
        ("PDT", ""),
        ("POS", ""),  # possessive ending parent‘s,
        ("PRP", "pron"),
        ("PRP$", "pron"),
        ("RB", "adv"),
        ("RBR", "adv"),
        ("RBS", "adv"),
        ("RP", ""),  # particle give up
        ("TO", ""),  # to go ‘to‘ the store
        ("UH", "int"),  # interjection errrrrrrrm
        ("VB", "v"),  # verb, base form take
        ("VBD", "v"),  # verb, past tense took
        ("VBG", "v"),  # verb, gerund/present participle taking
        ("VBN", "v"),  # verb, past participle taken
        ("VBP", "v"),  # verb, sing. present, non-3d take
        ("VBZ", "v"),  # verb, 3rd person sing. present takes
        ("WDT", "pron"),  # wh-determiner which
        ("WP", "pron"),  # wh-pronoun who, what
        ("WP$", "pron"),  # possessive wh-pronoun whose
        ("WRB", "adv"),  # wh-abverb where, when
    ]
)

logger = setup_logger(  # pylint: disable=invalid-name
    name = __file__,
    level = 20,  #info
)
logger.info("logger.name: %s", logger.name)

def bingmdx_tr(sent: Union[List[str], str]) -> str:
    """ use msbing mdx "traslate" sent to chinese.

    TODO: user defined dict takes precedence

    pytest --doctest-modules bingmdx_tr.py
    >>> bingmdx_tr("测试")
    '测试'
    >>> bingmdx_tr("")
    ''
    >>> bingmdx_tr("test")
    '试验；检测；考试；测验'
    >>> bingmdx_tr('make')
    '做；制造；使得；赚钱'
    >>> bingmdx_tr('you')
    '你'
    >>> bingmdx_tr('i')
    '我'
    """

    if isinstance(sent, list):
        sent = " ".join(sent)

    # need to keep names unchanged
    # blob = TextBlob(sent.lower())
    blob = TextBlob(sent)

    list_zh = []

    count = -1
    for word, tag in blob.tags:
        count += 1
        if word in HWD:  # already chinese
            list_zh.append(word)
            continue

        # check first unaltered form of word
        res = MDX_DICT.get(word)
        if res:
            # userdict  MDX_DICT.get('i') -> {'userdef': ' 我'}
            # if isinstance(res, str):
            if res.get("userdef"):
                list_zh.append(res.get("userdef"))
            else:
                # check tag
                _ = map_tags.get(tag)
                if res.get(_):
                    list_zh.append(res.get(_))
                else:  # for empty tags, return everything
                    word_tr = "".join([elm for elm in MDX_DICT.get(word).values()])
                    list_zh.append(word_tr)
            continue

        # lower case of word, BINGMDX
        res = MDX_DICT.get(word.lower())
        if res is None:  # word not in MDX_DICT
            list_zh.append(word)
            continue

        logger.debug("count: %s", count)
        logger.debug(" textblob tag: %s", tag)
        tag = map_tags.get(tag)  # map to binmdx tag
        logger.debug("msbing tag: %s", tag)
        logger.debug("word: %s", word)

        if not tag:  # for empty tags, return everything
            word_tr = "".join([elm for elm in res.values()])
        else:
            word_tr = res.get(tag)
            if word_tr is None:
                list_zh.append(word)
                continue
        list_zh.append(word_tr)

    return "".join(list_zh)
