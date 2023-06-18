import argparse
import logging
from solcx import (
    compile_files,
)
from parse_version import parse_version

from rattle.evmasm import EVMAsm
from rattle.recover import Recover
from symbolic_exe import Symbolic

from add_overflow import check_add_overflow


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "file", type=argparse.FileType("rb"), action="store")
    arg_parser.add_argument("-t", dest="target-file", action="store")
    args = arg_parser.parse_args()
    file = args.file
    filename = file.name

    byte_code = {}

    parse_version(file)

    contracts = compile_files([filename])

    for name, c in contracts.items():
        bin_runtime = c['bin-runtime']
        byte_code[name] = bin_runtime.encode('utf-8')
        # bin-runtime: 블록 체인에 실제로 올라가는 이진 코드
        # utf-8로 인코딩

    print("byte code:", byte_code)

    for name, byte in byte_code.items():
        print("evm disassembled: ")
        for r in EVMAsm.disassemble_all(byte):
            print(r.name, r.opcode, r.operand)
        # disassemble evm bytecode
        recover = Recover(byte, edges=[], optimize=True)
        sym = Symbolic(recover)
        traces = sym.run()
        print("traces:", traces)
        for trace in traces:
            for block in trace.blocks_checked:
                for inst in block.block.insns:
                    inst_name = inst.insn.name
                    # registers = block.state.registers
                    args = inst.arguments
                    print("instruction name:", inst_name)
                    if inst_name == "ADD":
                        print("check integer overflow...")
                        check_add_overflow(inst, block.block)


if __name__ == "__main__":
    main()
