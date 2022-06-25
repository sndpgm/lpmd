"""pytest for lpmd.core.untable.scrape."""

import os
import shutil

import numpy as np
import pandas as pd
import pytest
import yaml

from lpmd.core.scrape import (
    BaseScraper,
    ScraperCarcass,
    ScraperShipment,
    ScraperSlaughter,
)

# -------------------------
# BaseScraper pytest
# -------------------------

test_data_id = "shipment"
test_partition_id = "00.All"
test_url = "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032117924&fileKind=0"
test_error_url = "http://xxxxxx/dummy/test/xxxxxx.jp"


class TestBaseScraper:
    """pytest for lpmd.core.scrape.BaseScraper"""

    @pytest.fixture()
    def setup(self):
        self.base = BaseScraper(data_id=test_data_id)

    def test_init_property(self, setup):
        assert self.base.data_id == test_data_id

        with open("data_catalogue.yml", "r") as yml:
            data_catalogue = yaml.safe_load(yml)
        assert self.base.data_catalogue == data_catalogue[test_data_id]
        assert self.base.columns == data_catalogue[test_data_id]["columns"]

        assert self.base.datasets_path == "lpmd/datasets/{data_id}/".format(
            data_id=test_data_id
        )

    def test_get_scraped_data(self, setup):
        df = self.base.get_scraped_data(partition_id=test_partition_id)
        assert len(df) > 0

        self.base.data_catalogue["partition"][test_partition_id] = test_error_url
        df = self.base.get_scraped_data(partition_id=test_partition_id)
        assert df is None

        self.base.data_catalogue["partition"][test_partition_id] = test_url

    def test__cleanse_scraped_data(self, setup):
        df_scraped = pd.DataFrame(
            {
                "year": [
                    "平.13(2001)",
                    "平.14(2002)",
                    "平.15(2003)",
                    "平.16(2004)",
                    "平.17(2005）",
                    "平.18(2006）",
                ],
                "cattle": ["…", "-", "x", "35660", "35080", "33755"],
            }
        )

        df_scraped_exp = pd.DataFrame(
            {
                "year": [2001, 2002, 2003, 2004, 2005, 2006],
                "cattle": [np.nan, np.nan, np.nan, 35660.0, 35080.0, 33755.0],
            }
        )
        df_scraped_exp["year"] = df_scraped_exp["year"].astype(int)
        df_scraped_exp["cattle"] = df_scraped_exp["cattle"].astype(float)

        df_scraped_tgt = self.base._cleanse_scraped_data(df_scraped=df_scraped)

        pd.testing.assert_frame_equal(df_scraped_tgt, df_scraped_exp)


# -------------------------
# ScraperShipment pytest
# -------------------------

test_shipment_data_id = "shipment"
test_shipment_partition_id = "00.All"
test_shipment_url = "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032117924&fileKind=0"
test_shipment_error_url = "http://xxxxxx/dummy/test/xxxxxx.jp"


class TestScraperShipment:
    @pytest.fixture()
    def setup(self):
        self.scraper = ScraperShipment()

    def test_get_scraped_data(self, setup):
        df = self.scraper.get_scraped_data(partition_id=test_shipment_partition_id)
        assert len(df) > 0

        self.scraper.data_catalogue["partition"][
            test_shipment_partition_id
        ] = test_shipment_error_url
        df = self.scraper.get_scraped_data(partition_id=test_shipment_partition_id)
        assert df is None

        self.scraper.data_catalogue["partition"][
            test_shipment_partition_id
        ] = test_shipment_url

    def test_save_scraped_data(self, setup):
        # path を指定しない場合, save 場所に何もないことを確認.
        path = None
        file = test_shipment_data_id + "-" + test_shipment_partition_id + ".csv"
        path_file = os.path.join(".", test_shipment_data_id, file)
        assert not os.path.exists(path_file)

        # save されたことを確認する.
        has_saved = self.scraper.save_scraped_data(
            partition_id=test_shipment_partition_id, path=path
        )
        assert has_saved
        assert os.path.exists(path_file)

        # cleanup
        shutil.rmtree(test_shipment_data_id)

        # path を指定した場合, save 場所に何もないことを確認.
        path = "lpmd/tests/core/.tmp"
        path_file = os.path.join(path, test_shipment_data_id, file)
        assert not os.path.exists(path_file)

        # save されたことを確認する.
        has_saved = self.scraper.save_scraped_data(
            partition_id=test_shipment_partition_id, path=path
        )
        assert has_saved
        assert os.path.exists(path_file)

        # cleanup
        shutil.rmtree(path)

    def test_raise_save_scraped_data(self, setup):
        msg = "Specified path must be str."
        path = 1234567890
        with pytest.raises(TypeError, match=msg):
            self.scraper.save_scraped_data(
                partition_id=test_shipment_partition_id, path=path
            )

    def test_save_batch(self, setup):
        exp_dict_result = dict()
        for partition_id in self.scraper.data_catalogue["partition"].keys():
            exp_dict_result[partition_id] = True

        tgt_dict_result = self.scraper.save_batch()
        assert tgt_dict_result == exp_dict_result

        # cleanup
        shutil.rmtree(self.scraper.data_id)

    def test_aggregate(self, setup):
        df = self.scraper.aggregate()
        assert len(df) > 0

    def test_out_to_datasets(self, setup):
        original_datasets_path = self.scraper.datasets_path
        self.scraper.datasets_path = "lpmd/tests/core/.tmp/{data_id}/".format(
            data_id=self.scraper.data_id
        )
        file = "{data_id}.parquet.zstd".format(data_id=self.scraper.data_id)

        # 保存先パス文字列のテスト.
        exp_file_path = os.path.join(self.scraper.datasets_path, file)
        tgt_file_path = self.scraper.out_to_datasets()
        assert tgt_file_path == exp_file_path

        # 実際にファイルが保存されているか確認.
        assert os.path.exists(tgt_file_path)

        # cleanup
        shutil.rmtree("lpmd/tests/core/.tmp/")
        self.scraper.datasets_path = original_datasets_path


# -------------------------
# ScraperSlaughter pytest
# -------------------------

test_slaughter_data_id = "slaughter"
test_slaughter_partition_id = "00.All"
test_slaughter_url = "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032117992&fileKind=0"
test_slaughter_error_url = "http://xxxxxx/dummy/test/xxxxxx.jp"


class TestScraperSlaughter:
    @pytest.fixture()
    def setup(self):
        self.scraper = ScraperSlaughter()

    def test_get_scraped_data(self, setup):
        df = self.scraper.get_scraped_data(partition_id=test_slaughter_partition_id)
        assert len(df) > 0

        self.scraper.data_catalogue["partition"][
            test_slaughter_partition_id
        ] = test_slaughter_error_url
        df = self.scraper.get_scraped_data(partition_id=test_slaughter_partition_id)
        assert df is None

        self.scraper.data_catalogue["partition"][
            test_slaughter_partition_id
        ] = test_slaughter_url

    def test_out_to_datasets(self, setup):
        original_datasets_path = self.scraper.datasets_path
        self.scraper.datasets_path = "lpmd/tests/core/.tmp/{data_id}/".format(
            data_id=self.scraper.data_id
        )
        file = "{data_id}.parquet.zstd".format(data_id=self.scraper.data_id)

        # 保存先パス文字列のテスト.
        exp_file_path = os.path.join(self.scraper.datasets_path, file)
        tgt_file_path = self.scraper.out_to_datasets()
        assert tgt_file_path == exp_file_path

        # 実際にファイルが保存されているか確認.
        assert os.path.exists(tgt_file_path)

        # cleanup
        shutil.rmtree("lpmd/tests/core/.tmp/")
        self.scraper.datasets_path = original_datasets_path


# -------------------------
# ScraperCarcass pytest
# -------------------------

test_carcass_data_id = "carcass"
test_carcass_partition_id = "00.All"
test_carcass_url = "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032118040&fileKind=0"
test_carcass_error_url = "http://xxxxxx/dummy/test/xxxxxx.jp"


class TestScraperCarcass:
    @pytest.fixture()
    def setup(self):
        self.scraper = ScraperCarcass()

    def test_get_scraped_data(self, setup):
        df = self.scraper.get_scraped_data(partition_id=test_carcass_partition_id)
        assert len(df) > 0

        self.scraper.data_catalogue["partition"][
            test_carcass_partition_id
        ] = test_carcass_error_url
        df = self.scraper.get_scraped_data(partition_id=test_carcass_partition_id)
        assert df is None

        self.scraper.data_catalogue["partition"][
            test_carcass_partition_id
        ] = test_carcass_url

    def test_out_to_datasets(self, setup):
        original_datasets_path = self.scraper.datasets_path
        self.scraper.datasets_path = "lpmd/tests/core/.tmp/{data_id}/".format(
            data_id=self.scraper.data_id
        )
        file = "{data_id}.parquet.zstd".format(data_id=self.scraper.data_id)

        # 保存先パス文字列のテスト.
        exp_file_path = os.path.join(self.scraper.datasets_path, file)
        tgt_file_path = self.scraper.out_to_datasets()
        assert tgt_file_path == exp_file_path

        # 実際にファイルが保存されているか確認.
        assert os.path.exists(tgt_file_path)

        # cleanup
        shutil.rmtree("lpmd/tests/core/.tmp/")
        self.scraper.datasets_path = original_datasets_path
