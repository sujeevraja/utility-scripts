#!/usr/bin/env python3

"""
Script to format or unformat JSON files.
"""

import argparse
from . import common
import json
import logging
import typing


log = logging.getLogger(__name__)


class Config(typing.NamedTuple):
    file: str
    minify: bool


def get_data(fpath):
    log.info(f"loading data from {fpath}...")
    with open(fpath, "r") as infile:
        return json.load(infile)


def run(cfg: Config):
    fpath = cfg.file
    data = get_data(fpath)
    with open(fpath, "w") as outfile:
        if cfg.minify:
            log.info(f"writing minified JSON to {fpath}...")
            json.dump(data, outfile, ensure_ascii=False)
        else:
            log.info(f"writing prettified JSON to {fpath}...")
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    log.info("done")


def handle_command_line():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--file",
                        type=str, help="path to csv file",
                        default=None)

    parser.add_argument("-m", "--minify",
                        help="write JSON without whitespace",
                        action="store_true")

    args = parser.parse_args()
    return Config(**vars(args))


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s--: %(message)s',
                        level=logging.DEBUG)

    try:
        config = handle_command_line()
        run(config)
    except common.ScriptException as se:
        log.error(se)


if __name__ == '__main__':
    main()
