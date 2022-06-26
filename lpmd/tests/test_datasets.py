import pandas as pd

import lpmd.datasets as dt


class TestDatasets:
    """Unit test for lpmd.datasets."""

    def test__load(self):
        """Unit test for lpmd.datasets._load()."""
        data_id = "shipment"
        df = dt._load(data_id=data_id)
        assert len(df) > 0

    def test_load_shipment(self):
        df = dt.load_shipment()
        assert df.shape == tuple([1200, 25])

        exp_columns = pd.Index(
            [
                "year",
                "pig",
                "cattle",
                "adult_cattle",
                "wagyu",
                "wagyu_heifer",
                "wagyu_steer",
                "wagyu_bull",
                "dairy_cattle",
                "dairy_cow",
                "dairy_fattening_bull",
                "other",
                "other_cow",
                "other_bull",
                "calf_wagyu",
                "calf_dairy",
                "calf_dairy_fattening_bull",
                "calf_other",
                "horse",
                "foal",
                "sheep",
                "goat",
                "data_source",
                "prefecture",
                "source_url",
            ]
        )
        pd.testing.assert_index_equal(df.columns, exp_columns)

        assert isinstance(df.index, pd.RangeIndex)
        assert df.index[0] == 0
        assert df.iloc[0, 1] == 20638965.0

        for col in df.columns:
            if col == "year":
                assert pd.api.types.is_integer_dtype(df[col])
            elif col in ["data_source", "prefecture", "source_url"]:
                assert pd.api.types.is_string_dtype(df[col])
            else:
                assert pd.api.types.is_float_dtype(df[col])

    def test_load_slaughter(self):
        df = dt.load_slaughter()
        assert df.shape == tuple([1728, 39])

        exp_columns = pd.Index(
            [
                "year",
                "pig",
                "cattle",
                "adult_cattle",
                "wagyu",
                "wagyu_heifer",
                "wagyu_steer",
                "wagyu_bull",
                "dairy_cattle_including_f1",
                "dairy_cow_including_f1",
                "dairy_fattening_bull_including_f1",
                "dairy_cattle",
                "dairy_cow",
                "dairy_steer",
                "dairy_bull",
                "f1_cattle",
                "f1_cow",
                "f1_bull_including_steer",
                "f1_steer",
                "f1_bull",
                "other",
                "other_cow",
                "other_bull_including_steer",
                "other_steer",
                "other_bull",
                "calf",
                "calf_wagyu",
                "calf_dairy",
                "calf_dairy_fattening_bull",
                "calf_other",
                "horse_and_foal",
                "horse",
                "foal",
                "sheep",
                "goat",
                "abattoir",
                "data_source",
                "prefecture",
                "source_url",
            ]
        )
        pd.testing.assert_index_equal(df.columns, exp_columns)

        assert isinstance(df.index, pd.RangeIndex)
        assert df.index[0] == 0
        assert df.iloc[0, 1] == 20638965.0

        for col in df.columns:
            if col == "year":
                assert pd.api.types.is_integer_dtype(df[col])
            elif col in ["data_source", "prefecture", "source_url"]:
                assert pd.api.types.is_string_dtype(df[col])
            else:
                assert pd.api.types.is_float_dtype(df[col])

    def test_load_carcass(self):
        df = dt.load_carcass()
        assert df.shape == tuple([1728, 39])

        exp_columns = pd.Index(
            [
                "year",
                "pig",
                "cattle",
                "adult_cattle",
                "wagyu",
                "wagyu_heifer",
                "wagyu_steer",
                "wagyu_bull",
                "dairy_cattle_including_f1",
                "dairy_cow_including_f1",
                "dairy_fattening_bull_including_f1",
                "dairy_cattle",
                "dairy_cow",
                "dairy_steer",
                "dairy_bull",
                "f1_cattle",
                "f1_cow",
                "f1_bull_including_steer",
                "f1_steer",
                "f1_bull",
                "other",
                "other_cow",
                "other_bull_including_steer",
                "other_steer",
                "other_bull",
                "calf",
                "calf_wagyu",
                "calf_dairy",
                "calf_dairy_fattening_bull",
                "calf_other",
                "horse_and_foal",
                "horse",
                "foal",
                "sheep",
                "goat",
                "carcass",
                "data_source",
                "prefecture",
                "source_url",
            ]
        )
        pd.testing.assert_index_equal(df.columns, exp_columns)

        assert isinstance(df.index, pd.RangeIndex)
        assert df.index[0] == 0
        assert df.iloc[0, 1] == 1531913.8

        for col in df.columns:
            if col == "year":
                assert pd.api.types.is_integer_dtype(df[col])
            elif col in ["data_source", "prefecture", "source_url"]:
                assert pd.api.types.is_string_dtype(df[col])
            else:
                assert pd.api.types.is_float_dtype(df[col])
