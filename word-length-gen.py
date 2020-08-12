from pathlib import Path

from pprint import pprint

from polyglot.text import Text
from nltk.translate.gale_church import align_blocks  # para_gc

dest = r"data"
path_en = Path(dest) / "0test_en.txt"
path_zh = Path(dest) / "0test_zh.txt"

path_en = Path(dest) / "wu_ch3_en.txt"
path_zh = Path(dest) / "wu_ch3_zh.txt"

path_en = Path(dest) / "hlm-ch1-en.txt"
path_zh = Path(dest) / "hlm-ch1-zh.txt"

path_en = Path(dest) / "lover-ch10_en.txt"
path_zh = Path(dest) / "lover-ch10_zh.txt"

logger.info("%s, %s", path_en, path_zh)

text_en = "\n".join(elm.strip() for elm in read_text(path_en).splitlines() if elm.strip())
text_zh = "\n".join(elm.strip() for elm in read_text(path_zh).splitlines() if elm.strip())

word_len_ratio = len(Text(text_en).words)/len(Text(text_zh).words)
# assert 0.7 < word_len_ratio < 1 / 0.7
if not 0.7 < word_len_ratio < 1 / 0.7:
    logger.warning("\n\tText lengths (word-based (english), char-based (Chinese) ) \n\tin tow texts rather skewed: \n\t\t%.2f (expected 0.7-1.4) \n\tAlignment quality may suffer.", word_len_ratio)

paras_en = text_en.splitlines()
paras_zh = text_zh.splitlines()

r, c = 111, 110  # lover10 [9, 14, 14, 30, 7, 20, 2, 26, 13, 27], [23, 2, 4, 12, 32, 6, 23, 70]

r, c = (369, 368)  # lover10  [23, 13, 8], [5, 47]
r, c = (236, 235)  # [11, 8, 32, 22, 28, 14, 24, 8, 29, 25, 9, 31, 6], [10, 11, 25, 10, 14, 108, 32, 38, 50], (13, 9)

sents_en = [str(elm) for elm in Text(paras_en[r]).replace(";", ";\n").sentences]
sents_zh = [str(elm) for elm in Text(paras_zh[c]).sentences]

words_len_en = [Text(elm).words.__len__() for elm in sents_en]
words_len_zh = [Text(elm).words.__len__() for elm in sents_zh]

pprint([words_len_en, words_len_zh, (len(words_len_en), len(words_len_zh))])

_ = align_blocks(words_len_en, words_len_zh)
pprint([_, len(_), (len(words_len_en), len(words_len_zh))])

ali_sents_b = [[sents_en[i], sents_zh[j]] for i, j in align_blocks(words_len_en, words_len_zh)]
pprint([ali_sents_b, len(ali_sents_b)])