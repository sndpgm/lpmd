import sys

import pandas as pd


def _read_module(path):
    if sys.version_info >= (3, 9):
        from importlib.resources import files
    else:
        from importlib_resources import files
    return files(path)


def _load(data_id):
    path = _read_module("lpmd").joinpath(f"datasets/{data_id}/{data_id}.parquet.zstd")
    df = pd.read_parquet(path)
    return df


def load_shipment():
    return _load("shipment")


def load_slaughter():
    return _load("slaughter")


def load_carcass():
    return _load("carcass")
