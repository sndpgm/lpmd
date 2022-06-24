import os
import yaml

import pandas as pd

import lpmd.utils.format as fmt


# 1.都道府県別出荷頭数累年統計: データカラム辞書
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


# URLリストymlファイルを読み取り.
with open('url.yml', 'r') as yml:
    url_dict = yaml.safe_load(yml)


def get_shipment_df(url):
    df_raw = pd.read_excel(url)
    df_raw.columns = DICT_COLUMN_SHIPMENT.keys()
    df_raw = df_raw[(df_raw.index >= 7) & (~df_raw["year"].isna())]
    df_raw["year"] = fmt.format_raw_year(df_raw["year"])
    qty_columns = list(DICT_COLUMN_SHIPMENT.keys())[1:]
    df_raw[qty_columns] = df_raw[qty_columns].apply(fmt.format_raw_qty, axis=1)
    return df_raw


def download_shipment_df(path=None):
    # 固定
    _target_data_label = "1.都道府県別出荷頭数累年統計"
    _data_category_number = "shipment"

    # path を指定されなければ lpmd.datasets に保存.
    if path is None:
        path = "lpmd/datasets/"
    else:
        if not isinstance(path, str):
            msg = "Specified path must be str."
            raise TypeError(msg)

    # URL リストの中で「1.都道府県別出荷頭数累年統計」だけ取得.
    target_url_dict = url_dict[_target_data_label]

    # データを取得し保存するディレクトリを作成.
    save_path = path + _data_category_number + "/"
    os.makedirs(save_path, exist_ok=True)

    # 各都道府県別に取得.
    index = 1
    for prefecture, url in target_url_dict.items():
        df = get_shipment_df(url)
        df["prefecture"] = prefecture
        df["source_url"] = url

        _data_subcategory_number = str(index).zfill(2)
        filename = _data_category_number + "-" + _data_subcategory_number + ".tsv"
        df.to_csv(save_path + filename, sep="\t", index=False)
        index += 1

    print("「都道府県別出荷頭数累年統計」データを全て取得しました.")
