"""lpmd.core.scrape."""

import os
import shutil

import dask.dataframe as dd
import pandas as pd
import yaml

import lpmd.utils.check as check
import lpmd.utils.format as fmt


class BaseScraper:
    """
    Base class for scraper.

    Other scraper classes should inherit from this class.
    The class has base methods for scraping data, and in other scraper subclass `get_scraped_data` should be customized.

    Parameters
    ----------
    data_id : str
        String expressing which data should be scraped in data_catalogue.yml.

    """

    def __init__(self, data_id):
        self.data_id = data_id

        # Read yml file on urls
        with open("data_catalogue.yml", "r") as yml:
            data_catalogue = yaml.safe_load(yml)
        self.data_catalogue = data_catalogue[self.data_id]
        self.columns = self.data_catalogue["columns"]
        self.datasets_path = "lpmd/datasets/{data_id}/".format(data_id=self.data_id)

    def get_scraped_data(self, partition_id):
        """
        Get scraped data corresponding to partition_id.

        Parameters
        ----------
        partition_id : str
            String expressing which partition data should be scraped in data_catalogue.yml.

        Returns
        -------
        df_scraped : pandas.core.frame.DataFrame
            Scraped data that are not cleansed.

        """
        url = self.data_catalogue["partition"][partition_id]
        columns = self.columns.keys()

        # Check whether url is effective
        if not check.check_url(url):
            # ToDo: change logger
            print("Specified url is not effective.")
            return None

        # Read and cleanse Excel file on specified url
        df_scraped = pd.read_excel(url)
        df_scraped.columns = columns

        return df_scraped

    def _cleanse_scraped_data(self, df_scraped):
        """
        Cleanse scraped data.

        The function is assumed to be added in `get_scraped_data` of the class that inherit from `BaseScraper`.

        Parameters
        ----------
        df_scraped : pandas.core.frame.DataFrame
            Scraped data.

        Returns
        -------
        df_scraped : pandas.core.frame.DataFrame
            Scraped data that are cleansed.

        """
        for col in df_scraped.columns:
            if col in self.columns.keys():
                column_type = self.columns[col]["column_type"]
                if column_type == "str_year":
                    df_scraped[col] = fmt.format_raw_str_year(df_scraped[col])
                elif column_type == "qty":
                    df_scraped[col] = fmt.format_raw_qty(df_scraped[col])
        return df_scraped

    def save_scraped_data(self, partition_id, path=None, **kwargs):
        """
        Save scraped data.

        Parameters
        ----------
        partition_id : str
            String expressing which partition data should be scraped in data_catalogue.yml.
        path : str, default None
            Sting expressing the path to save. If None, scraped data is stored at working current directory.
        kwargs
            Additional keyword arguments passed to ``pandas.DataFrame.to_csv``.

        Returns
        -------
        has_saved : bool
            If scraped data is successfully saved, True. Otherwise, False.

        """
        has_saved = False
        if path is None:
            path = "."
        else:
            if not isinstance(path, str):
                msg = "Specified path must be str."
                raise TypeError(msg)

        # データを取得し保存するディレクトリを作成.
        save_path = os.path.join(path, self.data_id)
        os.makedirs(save_path, exist_ok=True)

        df_scraped = self.get_scraped_data(partition_id)
        if df_scraped is not None:
            filename = self.data_id + "-" + partition_id + ".csv"
            df_scraped.to_csv(os.path.join(save_path, filename), **kwargs)
            has_saved = True
        return has_saved

    def save_batch(self, path=None, **kwargs):
        """
        Save scraped data in batches that are defined in partition section of data_catalogue.yml.

        Parameters
        ----------
        path : str, default None
            Sting expressing the path to save. If None, scraped data is stored at working current directory.
        kwargs
            Additional keyword arguments passed to ``pandas.DataFrame.to_csv``.

        Returns
        -------
        dict_result : dict
            Dict expressing whether partition_id in question is successfully saved.

        """
        dict_result = dict()
        partition_id_list = self.data_catalogue["partition"].keys()
        for partition_id in partition_id_list:
            dict_result[partition_id] = self.save_scraped_data(
                partition_id, path=path, **kwargs
            )
        return dict_result

    def aggregate(self):
        """
        Aggregate scraped data that are defined in partition section of data_catalogue.yml into a single data frame.

        Returns
        -------
        df : pandas.core.frame.DataFrame
            Aggregated data frame.

        """
        path = ".tmp/"
        self.save_batch(path=path, index=False, sep="\t")
        ddf = dd.read_csv(f"{path}/{self.data_id}/*.csv", sep="\t")
        df = ddf.compute()
        shutil.rmtree(path)
        return df.reset_index(drop=True)

    def out_to_datasets(self):
        """
        Write a DataFrame to the binary parquet format in `lpmd.datasets`.

        Returns
        -------
        file_path : str
            The file path to be saved.

        """
        file = "{data_id}.parquet.zstd".format(data_id=self.data_id)
        file_path = os.path.join(self.datasets_path, file)
        os.makedirs(self.datasets_path, exist_ok=True)
        df = self.aggregate()
        df.to_parquet(file_path, compression="zstd")
        return file_path


class ScraperShipment(BaseScraper):
    """Scraper class for data on livestock products shipment."""

    _data_id = "shipment"

    def __init__(self):
        super(ScraperShipment, self).__init__(self._data_id)

    def get_scraped_data(self, partition_id):
        """
        Get scraped data corresponding to partition_id for livestock products shipment.

        Parameters
        ----------
        partition_id : str
            String expressing which partition data should be scraped in data_catalogue.yml.

        Returns
        -------
        df_scraped : pandas.core.frame.DataFrame
            Scraped data that are not cleansed.

        """
        df_scraped = super().get_scraped_data(partition_id)
        if df_scraped is not None:
            df_scraped = df_scraped[
                (df_scraped.index >= 7) & (~df_scraped["year"].isna())
            ]
            df_scraped = self._cleanse_scraped_data(df_scraped)
            df_scraped["data_source"] = self.data_catalogue["name"]
            df_scraped["prefecture"] = partition_id
            df_scraped["source_url"] = self.data_catalogue["partition"][partition_id]
            df_scraped.reset_index(drop=True, inplace=True)
        return df_scraped


class ScraperSlaughter(BaseScraper):
    """Scraper class for data on animals slaughtered and abattoirs."""

    _data_id = "slaughter"

    def __init__(self):
        super(ScraperSlaughter, self).__init__(self._data_id)

    def get_scraped_data(self, partition_id):
        """
        Get scraped data corresponding to partition_id for animals slaughtered and abattoirs.

        Parameters
        ----------
        partition_id : str
            String expressing which partition data should be scraped in data_catalogue.yml.

        Returns
        -------
        df_scraped : pandas.core.frame.DataFrame
            Scraped data that are not cleansed.

        """
        df_scraped = super().get_scraped_data(partition_id)
        if df_scraped is not None:
            df_scraped = df_scraped[
                (df_scraped.index >= 7) & (~df_scraped["year"].isna())
            ]
            df_scraped = self._cleanse_scraped_data(df_scraped)
            df_scraped["data_source"] = self.data_catalogue["name"]
            df_scraped["prefecture"] = partition_id
            df_scraped["source_url"] = self.data_catalogue["partition"][partition_id]
            df_scraped.reset_index(drop=True, inplace=True)
        return df_scraped


class ScraperCarcass(BaseScraper):
    """Scraper class for data on carcass."""

    _data_id = "carcass"

    def __init__(self):
        super(ScraperCarcass, self).__init__(self._data_id)

    def get_scraped_data(self, partition_id):
        """
        Get scraped data corresponding to partition_id for carcass.

        Parameters
        ----------
        partition_id : str
            String expressing which partition data should be scraped in data_catalogue.yml.

        Returns
        -------
        df_scraped : pandas.core.frame.DataFrame
            Scraped data that are not cleansed.

        """
        df_scraped = super().get_scraped_data(partition_id)
        if df_scraped is not None:
            df_scraped = df_scraped[
                (df_scraped.index >= 7) & (~df_scraped["year"].isna())
            ]
            df_scraped = self._cleanse_scraped_data(df_scraped)
            df_scraped["data_source"] = self.data_catalogue["name"]
            df_scraped["prefecture"] = partition_id
            df_scraped["source_url"] = self.data_catalogue["partition"][partition_id]
            df_scraped.reset_index(drop=True, inplace=True)
        return df_scraped
