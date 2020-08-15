""" save list np.ndarray pd.DataFrame as xlsx.

refer to color_table_applymap
"""

from typing import List, Optional, Union


from pathlib import Path
import numpy as np
import pandas as pd

from logzero import logger

from light_aligner.gen_filename import gen_filename


# fmt: off
def save_xlsx(
    lst: Union[np.ndarray, List[Union[str, float]], pd.core.frame.DataFrame],
    file: Optional[Union[str, Path]] = None,
) -> pd.core.frame.DataFrame:
    # fmt: on
    """ save list np.ndarray pd.DataFrame as xlsx.

    """
    columns = [str(elm) for elm in list(range(np.array(lst).shape[1]))]

    try:
        df_lst = pd.DataFrame(np.array(lst), columns=columns, dtype="object")
    except Exception as exc:
        logger.error(exc)
        raise
    if file is None:
        return df_lst

    if Path(file).suffix not in [".xlsx"]:
        file = f"{file}.xlsx"
    file = gen_filename(file)

    try:
        writer = pd.ExcelWriter(file)
        df_lst.to_excel(writer, index=None, header=None)
        writer.save()
    except Exception as exc:
        logger.error("Unable to save: %s", exc)
        raise

    return df_lst


def test_save_xlsx1():
    """ test save_xlsx Path. """
    filepath = Path("data/test.xlsx")
    lst = [[0, 1, "a"], [1, 1, 1]]
    res = save_xlsx(lst, filepath)
    assert Path(filepath).exists()
