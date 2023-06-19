from solcx import (set_solc_version_pragma, install_solc_pragma,
                   get_available_solc_versions,)
from solidity_parser.parser import parse
from solcx.exceptions import SolcNotInstalled


def parse_file(file):
    parsed_file = parse(file.read().decode("utf-8"))
    # 입력 파일 파싱 결과
    for children in parsed_file["children"]:
        if children["type"] == "PragmaDirective":
            return children["value"]
    # return get_available_solc_versions()[0]


def parse_version(file):
    parsed_file_version = parse_file(file)
    try:
        set_solc_version_pragma(parsed_file_version)
    except SolcNotInstalled:
        install_solc_pragma(parsed_file_version)
        set_solc_version_pragma(parsed_file_version)
