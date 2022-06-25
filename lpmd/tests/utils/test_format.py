"""pytest for lpmd.utils.format."""
import numpy as np
import pandas as pd
import pytest

import lpmd.utils.format as fmt

test_year_list = [
    "昭.60(1985)",
    "昭.61(1986)",
    "昭.62(1987)",
    "昭.63(1988)",
    "平.元(1989)",
    "平.2(1990)",
    "平.3(1991)",
    "平.4(1992)",
    "平.5(1993)",
    "平.6(1994)",
    "平.7(1995)",
    "平.8(1996)",
    "平.9(1997)",
    "平.10(1998)",
    "平.11(1999)",
    "平.12(2000)",
    "平.13(2001)",
    "平.14(2002)",
    "平.15(2003)",
    "平.16(2004)",
    "平.17(2005）",
    "平.18(2006）",
    "平.19(2007）",
    "平.20(2008）",
    "平.21(2009）",
]

test_year_series = pd.Series(test_year_list)

exp_year_series = pd.Series(
    [
        1985,
        1986,
        1987,
        1988,
        1989,
        1990,
        1991,
        1992,
        1993,
        1994,
        1995,
        1996,
        1997,
        1998,
        1999,
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
    ]
).astype(int)

test_qty_list = [
    "…",
    "-",
    "x",
    "35660",
    "35080",
    "33755",
    "32540",
]

test_qty_series = pd.Series(test_qty_list)

exp_qty_series = pd.Series([np.nan, np.nan, np.nan, 35660, 35080, 33755, 32540]).astype(
    float
)


class TestFormat:
    """pytest for lpmd.utils.format."""

    def test_format_raw_str_year(self):
        """Unit test for format_raw_year."""
        tgt_year_series = fmt.format_raw_str_year(test_year_series)
        pd.testing.assert_series_equal(tgt_year_series, exp_year_series)

    def test_raise_format_raw_year(self):
        """Raise test for format_raw_year."""
        msg = "Specified series must be `pandas.core.series.Series`."
        with pytest.raises(TypeError, match=msg):
            fmt.format_raw_str_year(test_year_list)

    def test_format_raw_qty(self):
        """Unit test for format_raw_qty."""
        tgt_qty_series = fmt.format_raw_qty(test_qty_series)
        pd.testing.assert_series_equal(tgt_qty_series, exp_qty_series)

    def test_raise_format_raw_qty(self):
        """Raise test for format_raw_qty."""
        msg = "Specified series must be `pandas.core.series.Series`."
        with pytest.raises(TypeError, match=msg):
            fmt.format_raw_qty(test_qty_list)
