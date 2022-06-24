import re

import pandas as pd


LIST_NULL = ["…", "-", "x"]


def format_raw_year(series):
    """「年次」カラムを整数型の年に変換する.

    Parameters
    ----------
    series : pandas.core.series.Series
        「年次」カラム series.

    Returns
    -------
    series_formatted : pandas.core.series.Series
        整数型の年に変換した series.

    """
    if not isinstance(series, pd.Series):
        msg = "Specified series must be `pandas.core.series.Series`."
        raise TypeError(msg)
    series_formatted = series.str.replace("（", "(").str.replace("）", ")").\
        replace(re.compile(r".*\("), "", regex=True).replace(re.compile(r"\)"), "", regex=True).astype(int)
    return series_formatted


def format_raw_qty(series):
    """数量に関するカラムについてデータとして扱いやすい形式に変換する.

    Parameters
    ----------
    series : pandas.core.series.Series
        数量カラム series.

    Returns
    -------
    series_formatted : pandas.core.series.Series
        変換した series.

    """
    if not isinstance(series, pd.Series):
        msg = "Specified series must be `pandas.core.series.Series`."
        raise TypeError(msg)

    series_formatted = series.copy()
    for val in LIST_NULL:
        series_formatted = series_formatted.replace(val, None)
    series_formatted = series_formatted.astype(float)
    return series_formatted
