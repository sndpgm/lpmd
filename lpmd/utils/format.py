"""lpmd.utils.format."""
import re

import pandas as pd

LIST_NULL = ["…", "-", "x"]


def format_raw_str_year(series):
    """Format the series for "年次" column into integer one.

    Parameters
    ----------
    series : pandas.core.series.Series
        "年次" column series.

    Returns
    -------
    series_formatted : pandas.core.series.Series
        Formatted column series.

    """
    if not isinstance(series, pd.Series):
        msg = "Specified series must be `pandas.core.series.Series`."
        raise TypeError(msg)
    series_formatted = (
        series.str.replace("（", "(")
        .str.replace("）", ")")
        .replace(re.compile(r".*\("), "", regex=True)
        .replace(re.compile(r"\)"), "", regex=True)
        .astype(int)
    )
    return series_formatted


def format_raw_qty(series):
    """Format the series on quantities into float one.

    Parameters
    ----------
    series : pandas.core.series.Series
        Series on quantities.

    Returns
    -------
    series_formatted : pandas.core.series.Series
        Formatted column series.

    """
    if not isinstance(series, pd.Series):
        msg = "Specified series must be `pandas.core.series.Series`."
        raise TypeError(msg)

    series_formatted = series.copy()
    for val in LIST_NULL:
        series_formatted = series_formatted.replace(val, None)
    series_formatted = series_formatted.astype(float)
    return series_formatted
