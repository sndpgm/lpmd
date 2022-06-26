from importlib.resources import files

import pandas as pd


def _load(data_id):
    path = files("lpmd").joinpath(f"datasets/{data_id}/{data_id}.parquet.zstd")
    df = pd.read_parquet(path)
    return df


def load_shipment():
    return _load("shipment")


def load_slaughter():
    return _load("slaughter")


def load_carcass():
    return _load("carcass")
