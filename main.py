import argparse
import copy
import logging
import os
import pandas as pd
from sec_edgar_downloader import Downloader
import yaml

DEFAULT_SYMBOL_COLUMN_NAME = "Symbol"
LOGGER = logging.getLogger("Download_SEC")


def download_sec_files(out_dir: str,
                       symbol_list,
                       after_date,
                       before_date,
                       file_types,
                       **_kwargs
                       ):
    downloader = Downloader(out_dir)

    for symbol in symbol_list:
        LOGGER.info(f"{symbol}")

        for file_type in file_types:
            try:
                downloader.get(filing=file_type,
                               ticker_or_cik=symbol,
                               after=after_date,
                               before=before_date)
                LOGGER.info(f"  {file_type}")
            except Exception:
                LOGGER.debug(f"Exception raised during the download of {file_type} for {symbol}")
                continue


def get_symbol_list(file_path: str,
                     column=None):
    if column is None:
        column = DEFAULT_SYMBOL_COLUMN_NAME
    try:
        df = pd.read_csv(file_path, usecols=[column])
        return list(df[column])
    except Exception:
        raise RuntimeError


def get_config_data(config_path: str):
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


def preprocess_args(args):
    args_copy = copy.deepcopy(args)
    args_dict = vars(args_copy)
    assert args_dict.get("out_dir")
    assert args_dict.get("config")

    try:
        config_data = get_config_data(args.config)
        args_copy.after_date, args_copy.before_date = config_data["after"], config_data["before"]
        assert type(config_data["file_types"]) is list
        args_copy.file_types = config_data["file_types"]
        args_copy.symbol_list = get_symbol_list(**config_data["portfolio"])
    except Exception:
        raise Exception

    os.makedirs(args_copy.out_dir, exist_ok=False)
    return args_copy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download SEC filing")
    parser.add_argument("--out_dir", type=str, required=True)
    parser.add_argument("--config", type=str, default="config/example.yml")

    args = parser.parse_args()
    args = preprocess_args(args)
    download_sec_files(**vars(args))
