""" a light-weight aligner"""

import os
import sys
from pathlib import Path

import tkinter as tk
from tkinter import messagebox

# pylint: disable=unused-import
from jinja2 import (  # type: ignore  # noqa: F401
    PackageLoader,
    Environment,
    ChoiceLoader,
    FileSystemLoader,
)

# pylint: enable=unused-import

# import torch
import numpy as np
import pandas as pd
from absl import app, flags  # type: ignore
from prompt_toolkit import HTML, print_formatted_text, prompt

# import warnings
# warnings.filterwarnings("ignore")
# warnings.filterwarnings('ignore', category=torch.serialization.SourceChangeWarning)

import logzero
from logzero import logger

from light_aligner import __version__
from light_aligner.light_aligner import light_aligner

from light_aligner.color_table_applymap import color_table_applymap
from light_aligner.common_prefix import common_prefix
from light_aligner.gen_filename import gen_filename
from light_aligner.browse_filename import browse_filename
from light_aligner.single_or_dual import single_or_dual
from light_aligner.text_to_plist import text_to_plist

from light_aligner.load_paras import load_paras
from light_aligner.load_xlsx import load_xlsx
from light_aligner.check_anchors import check_anchors

# from light_aligner.align_sents import align_sents
from light_aligner.plist_to_slist import plist_to_slist

# tkroot = tk.Tk()  # pylint: disable=invalid-name

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "src_file", "", "source file, browse to file location if left empty",
)
flags.DEFINE_string(
    "tgt_file", "", "target file, browse to file location if left empty",
)
flags.DEFINE_boolean(
    "version", False, f"light-aligner v.{__version__}",
)
flags.DEFINE_float(
    "thr", None, "a threhold (0. to 1.0), default to auto-adjust",
)
flags.DEFINE_boolean("debug", False, "display annoying debug messages.")


# pylint: disable=too-many-branches, too-many-statements, too-many-locals
def main(argv):
    """ __main__ main """

    del argv

    # root = tk.Tk()
    # root.withdraw()

    if FLAGS.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    _ = [
        "src_file",
        "tgt_file",
        "thr",
        "version",
        "debug",
    ]
    # args = CIMultiDict((elm, getattr(FLAGS, elm)) for elm in _)  # multidict._multidict.CIMultiDict  # noqa=E501

    args = dict((elm, getattr(FLAGS, elm)) for elm in _)
    logger.debug("\n\t args: %s", args)  # noqa=E501

    if args.get("version"):
        print(
            f"\t bumblebee-aligner v.{__version__} brought to you by mu@qq41947782, join qq-group 316287378 to be kept updated."
        )
        sys.exit(0)

    while 1:
        # try to load src_file 2 times
        _ = 0
        while not args.get("src_file").strip() and _ < 3:
            if _ > 0:
                title = f" retry {_}: select a file"
            else:
                title = "Select a file"
            logger.info("%s", "Select a file...")
            args["src_file"] = browse_filename(title=title)
            _ += 1
        if not args.get("src_file").strip():
            logger.warning(" Tried %s times, giving up", _)
            break
        # load src_text and detect dual-lang, if yes skip tgt_text
        src_file = args["src_file"]
        src_text = load_paras(src_file)
        logger.info("file 1: %s, ..., %s", src_text[0][:100], src_text[-1][:100])

        s_or_d = single_or_dual(src_text)
        if "en" in s_or_d and "zh" in s_or_d:
            root = tk.Tk()
            root.withdraw()
            ans = messagebox.askyesnocancel(
                "Dual-lang %s detected" % s_or_d,
                "Light-aligner thinks this is a dual-language %s file. Do you want to treat it as such?"
                % s_or_d,
            )
        else:  # normal single lang
            ans = False

        if ans:  # branch to process dual-lang file
            ...  # gen src_text and tgt_text
            p_list = text_to_plist(src_text)

            parent = Path(src_file).absolute().parent
            # src_stem = Path(src_file).stem
            stem = Path(src_file).stem
            suffix = ".xlsx"
            # tgt_stem = Path(tgt_file).stem
            # stem = common_prefix([stem, tgt_stem])
            # out_file = f'{parent / stem}-thr{thr}-tol{tol}{suffix}'
            out_file = f"{parent / stem}{suffix}"

            out_file = gen_filename(out_file)

            logger.debug(" out_file: %s", out_file)

            color_table_applymap(p_list, file=out_file)

            logger.info("\n\tFile written to **[%s]**", Path(out_file).absolute())

            logger.info("\n\t Opening **[%s]**", Path(out_file).absolute())

            # if args.get('startfile'):
            if sys.platform == "win32":
                os.startfile(out_file)

            # end of align and save
            # need to reset src_file tgt_file?

            # +++++++++++++++
            # align sents for dual ... get user input (out_file->out_file_s)
            root = tk.Tk()
            root.withdraw()
            ans = messagebox.askyesno(
                " Align sents ",
                "We now proceed to aligning sentences. You may wish to edit %s and save before the next step. Continue?",
            )
            logger.info("messagebox.askyesno ans: %s", ans)

            if ans:
                try:
                    anchors = 0
                    res = load_xlsx(out_file, anchors=anchors)
                except Exception as exc:
                    logger.error(" load_xlsx: %s", exc)
                    res = None

                if not (isinstance(res, int) or res is None):

                    anchors = check_anchors(res)

                    ans = True
                    if anchors < 1:
                        root = tk.Tk()
                        root.withdraw()
                        ans = messagebox.askyesno(
                            " No anchors found!",
                            "This is likely invalid data. We can proceed. But the result may not be that good for long texts. Continue?",
                        )
                    if ans:  # continue if anchors > 0 or anchors == 0 and ans == True
                        try:
                            # sents = align_sents(res)
                            slist = plist_to_slist(res)
                        except Exception as exc:
                            logger.error("align_sents: %s", exc)
                            slist = ""

                        if slist:
                            out_file_s = f"{Path(out_file).parent / stem}-s{suffix}"
                            out_file_s = gen_filename(out_file_s)
                            try:
                                writer = pd.ExcelWriter(out_file_s)
                                pd.DataFrame(slist).to_excel(writer, index=None, header=None)
                                writer.save()
                                flag = True
                            except Exception as exc:
                                logger.error(" save aligned sents exc: %s", exc)
                                flag = False
                            if flag:
                                logger.info(
                                    " aligned sents saved to *%s*",
                                    Path(out_file_s).absolute()
                                )

                                logger.info(
                                    "\n\t Opening **[%s]**", Path(out_file_s).absolute()
                                )

                                if sys.platform == "win32":
                                    os.startfile(out_file_s)

                # ---
            else:
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo(" Next ", "Alrihgt, it's your choice.")
            # get user input
            # ---------------

            user_input = prompt(
                HTML(
                    "Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: "
                )
            )
            if user_input.lower().strip().startswith("q"):
                break
            else:
                continue

            # return dual-lang file process

        # normal
        # try to load tgt_file 2 times
        _ = 0
        while not args.get("tgt_file").strip() and _ < 3:
            if _ > 0:
                title = f" retry {_}: select another file"
            else:
                title = " select another file"
            logger.info("%s", "Select another file...")
            args["tgt_file"] = browse_filename(title=title)
            _ += 1
        if not args.get("tgt_file").strip():
            logger.warning(" Tried %s times, giving up", _)
            break

        # aligning and saving output
        src_file = args["src_file"]
        tgt_file = args["tgt_file"]

        # rest src_file tgt_file
        args["src_file"] = ""
        args["tgt_file"] = ""

        if not (Path(src_file).exists() and Path(src_file).is_file()):
            logger.waning("%s does not exist or is not a file", src_file)
            # get user input
            user_input = prompt(
                HTML(
                    "Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: "
                )
            )
            if user_input.lower().strip().startswith("q"):
                break
            else:
                continue

        if not (Path(tgt_file).exists() and Path(tgt_file).is_file()):
            logger.waning("%s does not exist or is not a file", tgt_file)
            # get user input
            user_input = prompt(
                HTML(
                    "Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: "
                )
            )
            if user_input.lower().strip().startswith("q"):
                break
            else:
                continue

        tgt_text = load_paras(tgt_file)
        logger.info("file 2: %s, ..., %s", tgt_text[0][:100], tgt_text[-1][:100])

        thr = args.get("thr")
        _ = args.get("debug")

        logger.debug(" args: %s", args)

        # --- align and save
        logger.debug(" starting light_aligner")
        p_list = light_aligner(src_text, tgt_text, thr=thr, debug=_,)
        parent = Path(src_file).absolute().parent
        src_stem = Path(src_file).stem
        suffix = ".xlsx"
        tgt_stem = Path(tgt_file).stem
        stem = common_prefix([src_stem, tgt_stem])
        # out_file = f'{parent / stem}-thr{thr}-tol{tol}{suffix}'
        out_file = f"{parent / stem}-p{suffix}"

        out_file = gen_filename(out_file)

        logger.debug(" out_file: %s", out_file)

        color_table_applymap(p_list, file=out_file)

        logger.info("\n\tFile written to **[%s]**", Path(out_file).absolute())

        logger.info("\n\t Opening **[%s]**", Path(out_file).absolute())

        # if args.get('startfile'):
        if sys.platform == "win32":
            os.startfile(out_file)

        # end of para align and save

        # +++++++++++++++
        # align sents ... get user input
        root = tk.Tk()
        root.withdraw()
        ans = messagebox.askyesno(
            " Align sents ",
            "We now proceed to aligning sentences. You may wish to edit %s and save before the next step. Continue?",
        )

        if ans:
            try:
                anchors = 0
                res = load_xlsx(out_file, anchors=anchors)
            except Exception as exc:
                logger.error(" load_xlsx: %s", exc)
                res = None

            if not (isinstance(res, int) or res is None):

                anchors = check_anchors(res)

                ans = True
                if anchors < 1:
                    root = tk.Tk()
                    root.withdraw()
                    ans = messagebox.askyesno(
                        " No anchors found!",
                        "This is likely invalid data. We can proceed. But the result may not be that good for long texts. Continue?",
                    )
                if ans:  # continue if anchors > 0 or anchors == 0 and ans == True
                    try:
                        # sents = align_sents(res)
                        slist = plist_to_slist(res)
                    except Exception as exc:
                        logger.error("align_sents: %s", exc)
                        slist = ""

                    if slist:
                        out_file_s = f"{Path(out_file).parent / stem}-s{suffix}"
                        out_file_s = gen_filename(out_file_s)
                        try:
                            writer = pd.ExcelWriter(out_file_s)
                            pd.DataFrame(slist).to_excel(
                                writer, index=None, header=None
                            )
                            writer.save()
                            flag = True
                        except Exception as exc:
                            logger.error(" save aligned sents exc: %s", exc)
                            flag = False
                        if flag:
                            logger.info(" aligned sents saved to *%s*", out_file_s)
            # ---
        else:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(" Next ", "Alrihgt, it's your choice.")

        # get user input
        # ---------------

        user_input = prompt(
            HTML(
                "Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: "
            )
        )
        if user_input.lower().strip().startswith("q"):
            break
        else:
            continue

    # ---
    # while 1 loop end

    # logger.info('versoin: %s', VERSION)
    # logger.info('\n\t encode [\'test\'], mean: %s', np.mean(encode(['test'])))

    _ = HTML(
        f"\n<u>light-aligner v.{__version__} brought to you by mu@qq41947782, join qq-group 316287378 to be kept updated.</u>"
    )
    print_formatted_text(_)
    print_formatted_text(
        "(click to join 316287378: https://jq.qq.com/?_wv=1027&k=5e7BThu)"
    )

    # (https://jq.qq.com/?_wv=1027&k=5e7BThu)
    # return


# if __name__ == '__main__': main()
if __name__ == "__main__":

    app.run(main)  # => sys.exit(main(sys.argv))
