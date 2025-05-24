#!/usr/bin/env python3

"""
Script to convert CSV files to JSON.
"""

import argparse
import collections
import csv
import json
import logging
import os
import common


log = logging.getLogger(__name__)


Config = collections.namedtuple('Config', [
    'file'
])


class Controller(object):
    """class that manages the functionality of the entire script."""

    def __init__(self, config):
        self.config = config

    def run(self):
        fpath = self.config.file
        if not os.path.isfile(fpath):
            raise common.ScriptException(f"invalid path: {fpath}")

        if not fpath.endswith(".csv"):
            raise common.ScriptException(f"file should be csv: {fpath}")

        log.info(f"reading rows from {fpath}")
        rows = []
        with open(fpath, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append({k.strip(): v.strip() for k, v in row.items()})

        json_path = fpath.replace(".csv", ".json")
        log.info(f"writing json to {json_path}")
        with open(json_path, "w") as jsonfile:
            json.dump(rows, jsonfile, indent=4, ensure_ascii=False)

        log.info("done.")


def handle_command_line():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file",
                        type=str, help="path to csv file",
                        default=None)

    args = parser.parse_args()
    return Config(**vars(args))


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s--: %(message)s',
                        level=logging.DEBUG)

    try:
        config = handle_command_line()
        controller = Controller(config)
        controller.run()
    except common.ScriptException as se:
        log.error(se)


if __name__ == '__main__':
    main()
