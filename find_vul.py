import argparse
import logging
from solidity_parser.parser import parse
from solcx import get_available_solc_versions


def parse_file(file):
    parsed_file = parse(file.read().decode("utf-8"))
    print("parse:", parsed_file)
    for children in parsed_file["children"]:
        if children["type"] == "PragmaDirective":
            return children["value"]
    return get_available_solc_versions()[0]


logger = logging.getLogger()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file", type=argparse.FileType("rb"), action="store")
    arg_parser.add_argument("-t", dest="target-file", action="store")
    args = arg_parser.parse_args()
    file = args.file
    filename = file.name
    logger.info(f"analyzing {filename}")

    byte_code = {}
    parsed_file = parse_file(file)


if __name__ == "__main__":
    main()
