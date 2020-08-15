"""
load an xlsx file.

check nxl, l > 2
3rd col contains at least one positive number for paras
                at least one or two positive numbers for sents
retry 3 times in case the file is open by another app

return numpy.array of (n, 3)
"""

from typing import Optional, Union

from pathlib import Path
from tkinter import messagebox

import numpy as np
import pandas as pd
import xlrd

from logzero import logger


# pylint: disable=invalid-name
# fmt: off
def load_xlsx(
        filepath: Union[str, Path],
        anchors: int = 1,
) -> Optional[Union[int, np.array]]:
    # fmt: on
    """
    load an xlsx file with checking and retries

    sum(pd.to_numeric(df.iloc[:, 2], errors='coerce').replace(np.nan, 0) > 0) < anchors:
        handle
    """

    try:
        anchors = int(anchors)
    except Exception:
        anchors = 1

    _ = """
    count = 0
    while 1 and count < 3:
        count += 1
        print(count)
        if count > 3:
            break
    else:
        print("+", count)
    # """

    # try  3 times
    count = 0
    while 1 and count < 3:
        count += 1
        if count > 1:
            ans = messagebox.askyesno(" Retry ", "Attempt #%s. Continue?" % count)
            if not ans:
                return None  # user terminates
        try:
            # df = pd.read_excel(filepath, header=None, names=[0, 1, 2])
            # df.replace(np.nan, "", inplace=True)

            # switch to xlrd, pandas has difficulties reading \ufeff
            workbook = xlrd.open_workbook(filepath)
            sheet = workbook.sheet_by_index(0)
            data = [sheet.row_values(rowx) for rowx in range(sheet.nrows)]
            break  # loading successful
        except Exception as exc:
            logger.error(" pd.read_excel exc: %s", exc)
    else:
        logger.warning(" Can't load %s ", filepath)
        return -1  # not able to load

    # loading (pd.read_excel) successful
    # check 3rd column, # of positive float

    try:
        df = pd.DataFrame(data)
    except Exception as exc:
        logger.error(" pd.DataFrame(data) exc: %s", exc)
        raise

    _ = sum(pd.to_numeric(df.iloc[:, 2], errors='coerce').replace(np.nan, 0) > 0)

    if _ < anchors:
        logger.info("actual anchors: %s <  required anchors: %s", _, anchors)
        return -2  # anchors not satisfied
    df = df.iloc[:, 0:3]  # first 3 clumns only

    # return df.copy()
    return df
