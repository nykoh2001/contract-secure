import argparse
import logging
from solcx import (
    compile_files,
)
from parse_version import parse_version
from solcx.install import get_executable

from disassembler.disassem import EVMDisassemble


logger = logging.getLogger()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "file", type=argparse.FileType("rb"), action="store")
    arg_parser.add_argument("-t", dest="target-file", action="store")
    args = arg_parser.parse_args()
    file = args.file
    filename = file.name
    logger.info(f"analyzing {filename}")

    byte_code = {}

    parse_version(file)

    contracts = compile_files([filename])
    logger.info(f"compiled {filename}")

    for name, c in contracts.items():
        bin_runtime = c['bin-runtime']
        byte_code[name] = bin_runtime.encode('utf-8')
        # bin-runtime: 블록 체인에 실제로 올라가는 이진 코드
        # utf-8로 인코딩

    print("byte code:", byte_code)

    for name, byte in byte_code.items():
        logger.info(f"Analyzing {name}")
        print("evm disassembled: ")
        for r in EVMDisassemble.disassem_evm(byte):
            print(r.name, r.opcode, r.operand)
        # disassemble evm bytecode


if __name__ == "__main__":
    main()
