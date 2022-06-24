"""pytest for lpmd.core.untable.scrape."""
import shutil

import pandas as pd
import pytest

import lpmd.core.unstable.scrape as scp

test_url = {
    "effective": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032117924&fileKind=0",
    "ineffective": "http://xxxxxx/dummy/test/xxxxxx.jp",
}

test_path = "lpmd/tests/utils/data/"


class TestScrape:
    """pytest for lpmd.core.unstable.scrape."""

    def test_get_shipment_df(self):
        """Unit test for get_shipment_df."""
        effective_url = test_url["effective"]
        df = scp.get_shipment_df(effective_url)
        assert isinstance(df, pd.DataFrame)

        ineffective_url = test_url["ineffective"]
        df = scp.get_shipment_df(ineffective_url)
        assert df is None

    def test_save_batch_shipment_df(self):
        """Unit test for save_batch_shipment_df."""
        url_dict = scp.url_dict["01.shipment"]
        exp_dict_result = dict()
        for value in url_dict.values():
            exp_dict_result[value] = True

        tgt_dict_result = scp.save_batch_shipment_df(test_path)
        assert tgt_dict_result == exp_dict_result

        # Clean up
        shutil.rmtree(test_path)

    def test_raise_save_batch_shipment_df(self):
        """Raise test for save_batch_shipment_df."""
        error_path = 123456789
        msg = "Specified path must be str."
        with pytest.raises(TypeError, match=msg):
            scp.save_batch_shipment_df(error_path)
