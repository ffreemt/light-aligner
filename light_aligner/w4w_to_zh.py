"""
word for word translate to Chinese based on Bing mdx.

"""

# import logging
from pathlib import Path
import re
import json

import langid

from logzero import logger

DIR_PATH = Path(__file__).parent

# just the first entry
# DICT_FILE = Path(DIR_PATH, 'msbing_c_e-.pkl')

# all entries
DICT_FILE = Path(DIR_PATH, "msbing_c_e.pkl")

HWD_FILE = Path(DIR_PATH, "msbing_c_e_hw.pkl")
# EHWD_FILE = Path(DIR_PATH, 'msbing_c_e_ehw.pkl')

# json.dump(mdx_dict1, open('msbing_c_e.pkl', 'w'))
# json.dump(keys_zh, open('msbing_c_e_hw.pkl', 'w')) # 5792952
MDX_DICT = json.load(open(DICT_FILE))

# chinese hw
HWD = json.load(open(HWD_FILE))  # 26407
# english hw
# EHWD = json.load(open(EHWD_FILE))  # 47358


def w4w_to_zh(text: list) -> list:
    """ w4w translate to Chinese based on msbing mdx """

    # wrap str in list
    if isinstance(text, str):
        text = [text]

    # make sure it's a list
    if not isinstance(text, list):
        logger.error("Input： *%s* not a list", text)
        raise Exception("Input not a list")

    if langid.classify(" ".join(text))[0] in ["zh"]:
        resu = text
    else:
        resu = []
        # for par in tqdm(text, desc='looking words up', unit='par'):
        for par in text:  # par is a string
            # insert a space before punctuations
            par = [
                elm.strip() for elm in re.sub(r"\b", " ", par).split() if elm.strip()
            ]
            w_str = ""
            # for elm in pseg.cut(par):
            for word in par:
                if word.lower() in HWD:
                    # is alerady an Chinese
                    str_ = word
                else:  # 60 ms vs 7.6 ms
                    jdata = MDX_DICT.get(word)
                    if jdata is None:
                        str_ = word
                        # str_ = ""
                    else:
                        # str_ = ' '.join(jp.match('$.*', jdata))
                        str_ = " ".join([val for val in jdata.values()])

                w_str += f" {str_}"
                # logger.debug('elm: %s, str_: %s', elm, str_)

            w_str = re.sub(r"\s+", " ", w_str)

            # dedup  does not seem to help
            # w_str = "".join(set(w_str))

            resu += [w_str.strip()]

    resu0 = []
    for par in resu:
        # remove ;
        par = par.replace(";", "")

        # remove 【.*】
        par = re.sub(r"【.*?】", "", par)

        # remove 〈.*〉
        par = re.sub(r"〈.*?〉", "", par)

        # possibly
        # par = ' '.join(re.findall(r'[a-zA-Z_]+', par)

        # remove (=rod) (=refrigerator) or similar
        par = re.sub(r"\(\=.*?\)", "", par)

        resu0 += [par]

    return resu0
