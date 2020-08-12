''' a light-weight aligner'''

import os
import sys
from pathlib import Path

# pylint: disable=unused-import
from jinja2 import (  # type: ignore  # noqa: F401
    PackageLoader, Environment, ChoiceLoader, FileSystemLoader
)
# pylint: enable=unused-import

# import torch
# import numpy as np
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

from light_aligner.load_paras import load_paras

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'src_file',
    '',
    'source file, browse to file location if left empty',
)
flags.DEFINE_string(
    'tgt_file',
    '',
    'target file, browse to file location if left empty',
)
flags.DEFINE_boolean(
    'version',
    False,
    f'light-aligner v.{__version__}',
)
flags.DEFINE_float(
    'thr',
    None,
    'a threhold (0. to 1.0), default to auto-adjust.',
)
flags.DEFINE_boolean('debug', False, 'display annoying debug messages.')

# pylint: disable=too-many-branches, too-many-statements, too-many-locals
def main(argv):
    ''' __main__ main '''

    del argv

    if FLAGS.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    _ = ['src_file', 'tgt_file', 'thr', 'version', 'debug', ]
    # args = CIMultiDict((elm, getattr(FLAGS, elm)) for elm in _)  # multidict._multidict.CIMultiDict  # noqa=E501

    args = dict((elm, getattr(FLAGS, elm)) for elm in _)
    logger.debug('\n\t args: %s', args)  # noqa=E501

    if args.get('version'):
        print(f'\t bumblebee-aligner v.{__version__} brought to you by mu@qq41947782, join qq-group 316287378 to be kept updated.')
        sys.exit(0)

    while 1:
        # try to load src_file 2 times
        _ = 0
        while not args.get('src_file').strip() and _ < 3:
            if _ > 0:
                title = f' retry {_}: select a file'
            else:
                title = 'Select a file'
            logger.info('%s', 'Select a file...')
            args['src_file'] = browse_filename(title=title)
            _ += 1
        if not args.get('src_file').strip():
            logger.warning(' Tried %s times, giving up', _)
            break

        # try to load tgt_file 2 times
        _ = 0
        while not args.get('tgt_file').strip() and _ < 3:
            if _ > 0:
                title = f' retry {_}: select another file'
            else:
                title = ' select another file'
            logger.info('%s', 'Select another file...')
            args['tgt_file'] = browse_filename(title=title)
            _ += 1
        if not args.get('tgt_file').strip():
            logger.warning(' Tried %s times, giving up', _)
            break

        # aligning and saving output
        src_file = args['src_file']
        tgt_file = args['tgt_file']

        # rest src_file tgt_file
        args['src_file'] = ''
        args['tgt_file'] = ''

        if not (Path(src_file).exists() and Path(src_file).is_file()):
            logger.waning('%s does not exist or is not a file', src_file)
            # get user input
            user_input = prompt(HTML('Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: '))
            if user_input.lower().strip().startswith('q'):
                break
            else:
                continue

        if not (Path(tgt_file).exists() and Path(tgt_file).is_file()):
            logger.waning('%s does not exist or is not a file', tgt_file)
            # get user input
            user_input = prompt(HTML('Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: '))
            if user_input.lower().strip().startswith('q'):
                break
            else:
                continue

        src_text = load_paras(src_file)
        logger.info('file 1: %s, ..., %s', src_text[0][:100], src_text[-1][:100])
        tgt_text = load_paras(tgt_file)
        logger.info('file 2: %s, ..., %s', tgt_text[0][:100], tgt_text[-1][:100])

        thr = args.get('thr')
        _ = args.get('debug')

        logger.debug(" args: %s", args)

        # --- align and save
        logger.debug(" starting light_aligner")
        p_list = light_aligner(
            src_text,
            tgt_text,
            thr=thr,
            debug=_,
        )
        parent = Path(src_file).absolute().parent
        src_stem = Path(src_file).stem
        suffix = '.xlsx'
        tgt_stem = Path(tgt_file).stem
        stem = common_prefix([src_stem, tgt_stem])
        # out_file = f'{parent / stem}-thr{thr}-tol{tol}{suffix}'
        out_file = f'{parent / stem}{suffix}'

        out_file = gen_filename(out_file)

        logger.debug(" out_file: %s", out_file)

        color_table_applymap(p_list, file=out_file)

        logger.info('\n\tFile written to **[%s]**', Path(out_file).absolute())

        logger.info('\n\t Opening **[%s]**', Path(out_file).absolute())

        # if args.get('startfile'):
        if sys.platform.startswith('win'):
            os.startfile(out_file)  # type: ignore

        # end of align and save

        # get user input
        user_input = prompt(HTML('Press <ansigreen>any key</ansigreen> then <ansigreen>Enter</ansigreen> to align other files, or press <ansired>q</ansired> then <ansired>Enter</ansired> to quit: '))
        if user_input.lower().strip().startswith('q'):
            break
        else:
            continue

    # ---
    # while 1 loop end

    # logger.info('versoin: %s', VERSION)
    # logger.info('\n\t encode [\'test\'], mean: %s', np.mean(encode(['test'])))

    _ = HTML(f'\n<u>light-aligner v.{__version__} brought to you by mu@qq41947782, join qq-group 316287378 to be kept updated.</u>')
    print_formatted_text(_)
    print_formatted_text('(click to join 316287378: https://jq.qq.com/?_wv=1027&k=5e7BThu)')

    # (https://jq.qq.com/?_wv=1027&k=5e7BThu)
    # return

# if __name__ == '__main__': main()
if __name__ == "__main__":

    app.run(main)  # => sys.exit(main(sys.argv))