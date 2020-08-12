'''
style/color a table (applymap)
    per cell
'''
import logging
from pathlib import Path
# import functools
import numpy as np
import pandas as pd
# import seaborn as sns

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())
N_COLORS = 8


def color_table_applymap(lst, lower=0, upper=1, file=None, reverse=False):
    '''

    color_table_applymap(resu, file='wu_ch2.xlsx')

    Style/color a table using applymap
        per cell

    refer to color_table.py

    palette = sns.blend_palette(
        # ["pink", "palegreen", 'green'], N_COLORS).as_hex()
        # ["pink", "palegreen"], N_COLORS).as_hex()
        ["red", "palegreen"], N_COLORS).as_hex()
    '''
    palette = [
        '#ff0000',
        '#f02315',
        '#e2482c',
        '#d36b41',
        '#c49057',
        '#b5b36c',
        '#a7d883',
        '#98fb98',
    ]
    if reverse:
        # palette = sns.blend_palette(
        #     ['green', "palegreen", "pink"], N_COLORS).as_hex()
        palette = palette[::-1]

    columns = [str(elm) for elm in list(range(np.array(lst).shape[1]))]
    # is isinstance(lst, pd.core.frame.DataFrame):
    #     df_lst = lst
    try:
        df_lst = pd.DataFrame(np.array(lst), columns=columns, dtype='object')
    except Exception as exc:
        LOGGER.error(exc)
        raise

    def _color_func_g(data, lower=lower, upper=upper):
        wth = upper - lower

        # convert to float if possible
        try:
            data = float(data)
        except Exception:
            pass

        if isinstance(data, (int, float)):
            if upper > data > lower:
                return 'background-color: %s' % palette[int((data - lower) / wth * N_COLORS)]
        # boundary case
        if data == upper:
            return 'background-color: %s' % palette[-1]

        return ''

    def _color_func(data):
        if isinstance(data, (int, float)):
            return 'background-color: %s' % palette[int(
                (data + 0.5) * N_COLORS)] if 0 > data > - 0.5 else ''
        return ''

    s_df = df_lst.style.applymap(
        lambda data: _color_func_g(data, lower, upper),
        subset=columns,
    )

    if file is not None:
        if Path(file).suffix != '.xlsx':
            file = file + '.xlsx'
        try:
            writer = pd.ExcelWriter(file)
            s_df.to_excel(writer)
            writer.save()
        except Exception as exc:
            LOGGER.error(exc)
            raise

    return s_df
