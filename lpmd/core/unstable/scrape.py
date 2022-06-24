r"""lpmd.core.unstable.scrape.

Module to scrape files from the following URLs, which may not be available suddenly due to changes in file format.
    - https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00500227&tstat=000001044816&cycle=0&
    year=20200&month=0&tclass1=000001034718&tclass2val=0
"""

import os

import pandas as pd
import yaml

import lpmd.utils.check as check
import lpmd.utils.format as fmt

# Dict on the columns for statistics for the number of animals shipped by prefecture.
DICT_COLUMN_SHIPMENT = {
    "year": "年次",
    "pig": "豚(頭数)",
    "cattle": "牛計(頭数)",
    "adult_cattle": "成牛計(頭数)",
    "wagyu": "成牛・和牛小計(頭数)",
    "wagyu_heifer": "成牛・めす和牛(頭数)",
    "wagyu_steer": "成牛・去勢和牛(頭数)",
    "wagyu_bull": "成牛・おす和牛(頭数)",
    "dairy_cattle": "成牛・乳牛小計(頭数)",
    "dairy_cow": "成牛・乳用めす牛(頭数)",
    "dairy_fattening_bull": "成牛・乳用肥育おす牛(頭数)",
    "other": "成牛・その他の牛小計(頭数)",
    "other_cow": "成牛・その他の牛めす(頭数)",
    "other_bull": "成牛・その他の牛おす(頭数)",
    "calf_wagyu": "子牛・和子牛(頭数)",
    "calf_dairy": "子牛・乳子牛(頭数)",
    "calf_dairy_fattening_bull": "子牛・乳肥育おす牛(頭数)",
    "calf_other": "子牛・その他の子牛(頭数)",
    "horse": "馬・成馬(頭数)",
    "foal": "馬・子馬(頭数)",
    "sheep": "めん羊(頭数)",
    "goat": "やぎ(頭数)",
}


# Read yml file on urls
with open("url.yml", "r") as yml:
    url_dict = yaml.safe_load(yml)


def get_shipment_df(url):
    """Get dataframe on statistics for the number of animals shipped by prefecture.

    Parameters
    ----------
    url : str
        URL.

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Data frame on statistics for the number of animals shipped by prefecture.

    """
    # Check whether url is effective
    if not check.check_url(url):
        # ToDo: change logger
        print("Specified url is not effective.")
        return None

    # Read and cleanse Excel file on specified url
    df = pd.read_excel(url)
    df.columns = DICT_COLUMN_SHIPMENT.keys()
    df = df[(df.index >= 7) & (~df["year"].isna())]
    df["year"] = fmt.format_raw_year(df["year"])
    qty_columns = list(DICT_COLUMN_SHIPMENT.keys())[1:]
    df[qty_columns] = df[qty_columns].apply(fmt.format_raw_qty, axis=1)

    return df


def save_batch_shipment_df(path=None, **kwargs):
    """Save files on statistics data for the number of animals shipped by prefecture.

    Parameters
    ----------
    path : str, default None
        Path string. If None, files are saved in "lpmd/datasets/version/*"
    **kwargs : dict
        Keyword arguments for the module of saving files, that is through pandas.DataFrame.to_csv().

    Returns
    -------
    dict_result : dict[str, bool]
        Dict showing the results.

    """
    # Constant variables.
    _target_data_label = "01.shipment"
    _target_data_original_label = "1.都道府県別出荷頭数累年統計"

    # Result dict
    dict_result = dict()

    # path を指定されなければ lpmd/datasets/version/ に保存.
    if path is None:
        path = "lpmd/datasets/v0/"
    else:
        if not isinstance(path, str):
            msg = "Specified path must be str."
            raise TypeError(msg)

    # URL リストの中で「1.都道府県別出荷頭数累年統計」だけ取得.
    target_url_dict = url_dict[_target_data_label]

    # データを取得し保存するディレクトリを作成.
    save_path = os.path.join(path, _target_data_label)
    os.makedirs(save_path, exist_ok=True)

    # 各都道府県別に取得.
    for prefecture, url in target_url_dict.items():
        # Get data frame
        df = get_shipment_df(url)
        if df is not None:
            df["data_source"] = _target_data_original_label
            df["prefecture"] = prefecture
            df["source_url"] = url

            filename = _target_data_label + "-" + prefecture + ".tsv"
            df.to_csv(os.path.join(save_path, filename), **kwargs)
            dict_result[url] = True
        else:
            dict_result[url] = False

    # ToDo: change logger
    print("「都道府県別出荷頭数累年統計」データを全て取得しました.")
    return dict_result
