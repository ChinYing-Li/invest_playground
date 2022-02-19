import argparse
import os
from sec_edgar_downloader import Downloader


def try_downloader(args):
    downloader = Downloader(args.out_dir)
    downloader.get("10-K", "MMM", after="2017-01-01")


def preprocess_args(args):
    args_dict = vars(args)
    assert args_dict.get("out_dir")
    os.makedirs(args.out_dir, exist_ok=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download SEC filing")
    parser.add_argument("--out_dir", type=str, required=True)
    parser.add_argument("--config", type=str, default="")

    args = parser.parse_args()
    try_downloader(args)
